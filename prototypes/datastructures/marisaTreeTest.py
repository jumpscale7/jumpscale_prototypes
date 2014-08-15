import marisa_trie  # https://github.com/kmike/marisa-trie
import os
import struct

from JumpScale import j

j.application.start("marisa-trie")

nritems = 1000 * 1000


def marisa_create():
    inn = []
    rt = []
    for i in range(nritems):
        # if i/1000==round(i/1000,0):
        # 	print i
        # inn.append((u"%s"%j.tools.hash.md5_string(str(i)),i))  #for recordtree
        # key=struct.pack("<I",i)
        key = str(i).encode('utf-8')
        # key=j.base.byteprocessor.hashTiger160(str(i))
        rt.append((u"%s" % key, (4, 4, 4)))  # for recordtree
        # inn.append(u"%s"%j.tools.hash.md5_string(str(i)))  #for std tree
    trie = marisa_trie.RecordTrie("<HHH", rt)
    # trie=marisa_trie.Trie(inn)
    trie.save("/tmp/data")
    del(inn)


def populateTree(keys, name):
    trie = marisa_trie.Trie(keys)
    trie.save("%s.tree" % name)


marisa_create()

trie = marisa_trie.Trie()
trie.load("/tmp/data")

j.application.stop()
