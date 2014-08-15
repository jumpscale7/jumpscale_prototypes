# import pybloom
import struct

from JumpScale import j
import JumpScale.portal

j.application.start("bloomfilter")

# a bloomfilter is a very sparse datastructure to test if item is present or not
# be carefull, there can be false positives but never false negatives.

nritems = 1000 * 1000
nrtest = 100000

f = pybloom.BloomFilter(capacity=10000000, error_rate=0.001)


def populate(f):
    for i in range(nritems):
        f.add(j.tools.hash.md5_string(str(i)))
    return f


def test(f):
    success = 0
    for i in range(100000):
        r = j.base.idgenerator.generateRandomInt(nritems / 2, int(nritems * 1.5))
        # r=j.base.idgenerator.generateRandomInt(nritems+1,nritems*3)
        md5 = j.tools.hash.md5_string(str(r))
        if md5 in f:
            success += 1
    print "nrmatches:%s" % success

populate(f)
test(f)


j.application.stop()
