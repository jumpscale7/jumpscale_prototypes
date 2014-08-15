from JumpScale import j

# import zmq
import gevent
import gevent.monkey
# import zmo.green as zmq
import time
from gevent import Timeout

import JumpScale.grid

GeventLoopClass = j.core.grid.getGeventLoopClass()


class Lock():

    def __init__(self, name, concurrentMax=5, description="", timeout=60):
        self.concurrentMax = concurrentMax
        self.name = name
        self.description = description
        self.timeout = timeout
        self.greenletsActive = {}

    def checkCanExecute(self, id):
        if len(self.greenletsActive.keys()) < self.concurrentMax:
            self.greenletsActive[id] = True
            return True
        else:
            return False

    def __repr__(self):
        return "lock:%s" % self.name
    __str__ = __repr__


class JobManager(GeventLoopClass):

    def __init__(self):
        GeventLoopClass.__init__(self)
        # gevent.monkey.patch_all()
        gevent.monkey.patch_socket()
        gevent.monkey.patch_thread()
        gevent.monkey.patch_time()

        self.locks = {}
        self.locksActive = {}

    def addLock(self, name, concurrentMax=5, description="", timeout=60):
        lock = Lock(name, concurrentMax, description, timeout)
        self.locks[lock.name] = lock

    def getKey(self, stepname, jobid):
        key = "%s_%s" % (stepname, jobid)
        nr = 1
        while key in self.greenlets:
            nr += 1
            key = "%s_%s_%s" % (stepname, jobid, nr)
        return key

    def _methodExecute(self, method_, id_="", timeout_=0, **args):  # added the _ to make sure we have no conflicts with the code we execute
        timeoutObj = Timeout(timeout_)
        timeoutObj.start()

        if "lock_" in args:
            lock = args["lock_"]
            if lock != None:
                while not lock.checkCanExecute(id_):
                    # print "sleep for lock:%s for methodid:%s"% (lock,id_)
                    gevent.sleep(0.05)
            args.pop("lock_")

        try:
            result = method_(**args)
        except Exception as e:
            timeoutObj.cancel()
            self.methodError(id_, e)
            return None
        except Timeout as t:
            if t is not timeoutObj:
                raise RuntimeError("not my timeout")
            self.methodTimeout(id_)
            return None
        timeoutObj.cancel()
        if id_ in self.locksActive:
            self.locksActive.pop(id_)
            if lock != None:
                if id_ in lock.greenletsActive:
                    lock.greenletsActive.pop(id_)  # unlock the lock for this greenlet
            else:
                print "Could not find lock for id %s" % id_

        return result

    def do(self, jfunction, jname="", executorrole="*", jcategory="", jerrordescr="", jrecoverydescr="", jmaxtime=0,
           jwait=True, masterid=0, parentid=0, allworkers=None, lock="", **args):
        """
        @param allworkers if False then only one of the workers need to reply and execute the work (is of the role specified)
        """
        job = j.core.grid.zobjects.getZJobObject(
            executorrole=executorrole, actionid=action.id, args=args, jidmaster=masterid, jidparent=parentid, allworkers=allworkers)

    def do(self, stepname, method, timeout=600, lock="",    jobid=0, **args):
        """
        """
        id = self.getKey(stepname, jobid)
        print "do:%s %s" % (stepname, id)
        lockobj = None
        if lock != "":
            if lock in self.locks:
                lockobj = self.locks[lock]
                self.locksActive[id] = lockobj
        greenlet = self.schedule(id, self._methodExecute, id_=id, method_=method, timeout_=timeout, lock_=lockobj, **args)

    def methodTimeout(self, id):
        if id in self.locksActive:
            lock = self.locksActive[id]
            lock.greenletsActive.pop(id)  # unlock the lock for this greenlet
        if id in self.locksActive:
            self.locksActive.pop(id)
        print "method:%s timed out" % id

    def methodError(self, id, e):
        print "method:%s error, %s" % (id, e)
        if id in self.locksActive:
            lock = self.locksActive[id]
            lock.greenletsActive.pop(id)  # unlock the lock for this greenlet
        if id in self.locksActive:
            self.locksActive.pop(id)
