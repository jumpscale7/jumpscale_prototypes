from JumpScale import j
import JumpScale.baselib.key_value_store
import marisa_trie  # https://github.com/kmike/marisa-trie
import os
import tarfile
import struct

def marisa_test():
    inn = []
    for i in range(1000000):
        # if i/1000==round(i/1000,0):
        #   print i
        # inn.append((u"%s"%j.tools.hash.md5_string(str(i)),(1,5)))
        inn.append(u"%s" % j.tools.hash.md5_string(str(i)))
    #trie = marisa_trie.RecordTrie("<HH",inn)
    trie = marisa_trie.Trie(inn)
    trie.save("data")
    del(inn)


from cStringIO import StringIO
#from tarfile import open, TarInfo


#$length,$crc,$type,[$namespaceids]
# NOT NEEDED, OVERENGINEERING
# def serPrefix(type=1,namespaceids=[]):
#   out=struct.pack("H",type)
#   for nsid in namespaceids:
#       out+=struct.pack("H",nsid)
#   out=struct.pack("I",len(out))+out
#   return out
# def unserPrefix(content):
#   l=content[0:4]
#   length=struct.unpack("I",l)[0]
#   type=struct.unpack("H",content[4:6])[0]
#   namespaceids=[]
#   md=content[6:length+4]
#   for i in range(len(md)/2):
#       namespaceids.append(struct.unpack("H",md[i*2:i*2+2])[0])
#   content=content[6+len(md):]
#   return type,namespaceids,content
# e=serPrefix(99,[1,2,3,4])
# type,namespaceids,content=unserPrefix(e)
# import zfec
# encoder=zfec.Encoder(10,14)
# filename="/var/lib/libvirt/images/Ubuntu.img"
# counter=0
# def ecode(counter,series):
#   counter+=1
#   counterSeries=0
#   seriesOut=encoder.encode(series)
#   for out in seriesOut:
#       counterSeries+=1
#       pathout="out/Ubuntu.img.%s_%s"%(counter,counterSeries)
#       j.system.fs.writeFile(pathout,out)
#       print "%s_%s"%(counter,counterSeries)
#   return counter
# size=0
# series=[]
# block="start"
# with open(filename) as fp:
#   while block<>False:
#       block=fp.read(5000000)
#       size+=len(block)
#       series.append(block)
#       print size/1024/1024
#       if len(series)>9:
#           counter=ecode(counter,series)
#           series=[]
# from pylabs.Shell import ipshellDebug,ipshell
# print "DEBUG NOW jjj"
# ipshell()
if __name__ == '__main__':

    j.application.start("bloomfiltertest")

    trie = marisa_trie.Trie()

    root = "/mnt/2"
    root = "/usr/bin"

    items = j.system.fs.listFilesInDir(root, True, exclude=["*.pyc", "recovery-mode", "*/usr/src*", "*/var/log/*", "*/dev/*"], followSymlinks=False)

    FILE = "testtar2.tar"
    tar = tarfile.open(FILE, "w")
    #tar = tarfile.open("sample.tar.bz2", "w:bz2")
    uncompr = 0
    compr = 0
    start = j.base.time.getTimeEpoch()
    for path in items:
        patharc = path[len(root):]
        print "compress:%s" % patharc
        C = j.system.fs.fileGetContents(path)
        md5 = j.tools.hash.md5_string(C)
        # CC=j.db.serializers.snappy.dumps(C)
        CC = j.db.serializers.blosc.dumps(C)
        compr += len(CC)
        uncompr += len(C)
        ti = tarfile.TarInfo(patharc)
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
