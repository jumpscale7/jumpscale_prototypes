import os
import struct

from JumpScale import j

j.application.start("taralternative")

import JumpScale.baselib.serializers

from StringIO import StringIO
from tarfile import open, TarInfo
import tarfile

root = "/usr/bin"

items = j.system.fs.listFilesInDir(root, True, exclude=["*.pyc", "recovery-mode", "*/usr/src*", "*/var/log/*", "*/dev/*"], followSymlinks=False)

# remove links
items2 = []
for item in items:
    if not j.system.fs.isLink(item):
        items2.append(item)
items = items2

print "classic TAR will be slow because of slow bz2 compression"
tar = tarfile.open("/tmp/sample.tar.bz2", "w:bz2")
#tar = tarfile.open("sample.tar.gz", "w:gz")
for path in items:
    patharc = path[len(root):]
    print "compress:%s" % patharc
    tar.add(path, patharc)
tar.close()


print "this is a much faster compression tool, but lot less compression"

FILE = "/tmp/sample.tar.blosc"
tar = open(FILE, "w")
#tar = tarfile.open("sample.tar.bz2", "w:bz2")
uncompr = 0
compr = 0
start = j.base.time.getTimeEpoch()
for path in items:
    patharc = path[len(root):]
    print "compress:%s" % patharc
    C = j.system.fs.fileGetContents(path)
    CC = j.db.serializers.blosc.dumps(C)
    compr += len(CC)
    uncompr += len(C)
    ti = TarInfo(patharc)
    ti.size = len(CC)
    tar.addfile(ti, StringIO(CC))

tar.close()
stop = j.base.time.getTimeEpoch()
dur = stop - start
print "compression:%s" % (float(compr) / float(uncompr))
if dur > 0:
    print "MB/sec:%s" % (uncompr / dur / 1024 / 1024)

out = "/tmp/1"
start = j.base.time.getTimeEpoch()
uncompr = 0
compr = 0
tar = tarfile.open(FILE, "r")
for tarinfo in tar:
    ti = tar.extractfile(tarinfo)
    CC = ti.read(ti.size)
    C = j.db.serializers.blosc.loads(CC)
    compr += len(CC)
    uncompr += len(C)
    dest = "%s/%s" % (out, tarinfo.path)
    print dest
    j.system.fs.createDir(j.system.fs.getDirName(dest))
    j.system.fs.writeFile(dest, C)
    # j.system.fs.remove(dest)

tar.close()
stop = j.base.time.getTimeEpoch()
dur = stop - start
print "compression:%s" % (float(compr) / float(uncompr))
if dur > 0:
    print "MB/sec:%s" % (uncompr / dur / 1024 / 1024)

j.application.stop()
