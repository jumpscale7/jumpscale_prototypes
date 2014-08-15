import os
import struct

from JumpScale import j

j.application.start("tartest")


from StringIO import StringIO
#from tarfile import open, TarInfo
import tarfile

root = "/usr/bin"

items = j.system.fs.listFilesInDir(root, True, exclude=["*.pyc", "recovery-mode", "*/usr/src*", "*/var/log/*", "*/dev/*"], followSymlinks=False)


tar = tarfile.open("/tmp/sample.tar.bz2", "w:bz2")
#tar = tarfile.open("sample.tar.gz", "w:gz")
for path in items:
    patharc = path[len(root):]
    print "compress:%s" % patharc
    tar.add(path, patharc)
tar.close()

j.application.stop()
