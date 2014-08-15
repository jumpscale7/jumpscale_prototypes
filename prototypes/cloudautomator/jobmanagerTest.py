
from JumpScale import j

from lib.JobManager import *

j.application.start("jobmanager")


def testBasicTimeOut():
    """
    one job will timeout, 10 will be ok
    """
    jm = JobManager()

    def start(machineName):
        print "start:%s" % machineName
        time.sleep(10)
        # raise RuntimeError("testerror")
        print "started:%s" % machineName

    def start2(machineName):
        print "start:%s" % machineName
        time.sleep(5)
        print "started:%s" % machineName

    jm.do(10, "start", start, timeout=5, lock="", machineName="test.1")
    for i in range(10):
        jm.do(i, "start2", start2, timeout=20, lock="", machineName="test.%s" % i)

    jm.start()

# testBasicTimeOut()


def testLocking():

    jm = JobManager()
    jm.addLock("computenode.1.startvm", concurrentMax=1)  # means only 1 with that lock request can execute at same time

    def start(machineName, computenode):
        print "start:%s on computenode:%s" % (machineName, computenode)
        time.sleep(2)
        # raise RuntimeError("testerror")
        print "started:%s" % machineName

    nrcomputenodes = 3
    for computenodeid in range(1, 1 + nrcomputenodes):  # computenodes
        for i in range(5):
            jm.do("start_%s_%s" % (computenodeid, i), start, timeout=40,
                  lock="computenode.%s.startvm" % computenodeid, machineName="test.%s" % i, computenode=computenodeid)

    jm.start()

testLocking()

j.application.stop()
