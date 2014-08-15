from JumpScale import j

from lib.DigitalOcean import *
from lib.JobManager import *

q.application.appname = "cloudautomator"
q.application.start()

jm = JobManager()
jm.addLock("computenode.1", 1,)


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

image = "qb6_ub13_4"


do = DigitalOcean()

region = 2

key = do.getMainSSHKey()

# do.getALL()
# do.save()

# do.load()

do.deleteDroplets("test")

imageid = do.getImage('qb6_ub13_4').id

result = do.createMachines(nr=1, prefix="test", image=imageid, rootPasswd="Kds007")

# items=do.getDroplets(refresh=True)

# do.changeRootPasswd("tes","Kds007")


q.application.stop()
