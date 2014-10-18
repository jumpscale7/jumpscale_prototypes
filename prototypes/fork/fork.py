from JumpScale import j

j.application.start("fork")
import time
import psutil
import os


class WorkerProcess():
    def __init__(self):
        self.pid=os.fork()
        self.i=""
        if self.pid==0:
            self.do()
        else:
            self.refresh()
        

    def refresh(self):
        self.p= psutil.Process(self.pid)

    def kill(self):
        self.p.kill()

    def is_running(self):
        rss,vms=self.p.get_memory_info()
        return vms<>0

    def do(self):
        print 'A new child ',  os.getpid( )
        for t in range(20):
            for i in range(100):
                self.i+="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa"
            print t
        print "DONE:%s"%self
        time.sleep(0.1)
        os._exit(0)  

    def __str__(self):
        return "%s"%self.pid

    __repr__=__str__


class WorkerProcessManager():
    def __init__(self):
        self.processes={}

    def parent(self):        
        for i in range(100):
            p=WorkerProcess()            
            self.processes[p.pid]=p

        self.check()

    def check(self):
        i=0
        while True:
            i+=1
            print "NEXT:%s\n"%i    
            toremove=[]        
            for pid,p in self.processes.iteritems():
                # p.refresh()                
                if p.is_running():
                    pass
                else:
                    toremove.append(pid)
                    pass
                    # print "STOPPED:%s"%p
            for item in toremove:
                p=self.processes[item]
                #make sure you kill
                p.kill()
                self.processes.pop(item)
            time.sleep(1)
            if len(self.processes.keys())==0:
                print "no more children"
                # return
            print len(self.processes.keys())

        from IPython import embed
        print "DEBUG NOW ooo"
        embed()
        

pm=WorkerProcessManager()
pm.parent()

j.application.stop()
