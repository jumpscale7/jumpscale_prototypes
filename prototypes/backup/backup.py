from JumpScale import j
import JumpScale.grid.zdaemon

import os
import lzma

j.application.start("jumpscale:backuptest")

import JumpScale.baselib.backup

def test0b():
    
    cl=j.clients.backup.get(backupname="sublime",blobstorAccount="default",blobstorNamespace="backups",gitlabAccount="lenoir1",\
        compress=False,fullcheck=False,servercheck=True,storpath="/mnt/STOR")    
    key=cl.backup("/opt/sublimetext/","")
    print key
    cl.getMDFromBlobStor(key)
    cl.restore("","/opt/sublimetextrestore",link=True)

def test0():
    
    # path="/var/lib/lxc/test2"
    path="/var/lib/lxc/saucy-amd64-base"
    restore_path="%s_restore"%path
    name="saucy-amd64-base"

    cl=j.clients.backup.get(backupname=name,blobstorAccount="default",blobstorNamespace="backups",gitlabAccount="lenoir1",\
        compress=True,fullcheck=False,servercheck=True)
    key=cl.backup(path,"")
    key=cl.sendMDToBlobStor()
    # cl.getMDFromBlobStor(key)
    # cl.restore("",restore_path,link=True)    

def test1():

    # recipe="""
    # /BTSYNC/WINDOWS/JSAPPS/ : apps,bin,clouddesktopagent,portapps : JSAPPS
    # /BTSYNC/WINDOWS/python27: : python27
    # """

    # recipe
    # src : parts : blobstor namespace: dest
    recipe="""
    /opt/sublimetext/ : * : sublimebk : sublimeroot/bk/
    """

    cl=j.clients.backup.get(backupname="test",blobclientName="default",gitlabName="incubaid",compress=True)
    cl.backupRecipe(recipe)

    j.application.stop()

    filemgr = JSFileMgr(MDPath=metadata_path, cachePath=link_path)
    filemgr.restore("sublimeroot/bk/", "/tmp/sublime_restored", "sublimebk")

    original_path = '/opt/sublimetext/'
    original_dirs = [j.system.fs.pathRemoveDirPart(item, original_path) for item in j.system.fs.listDirsInDir(original_path, recursive=True)]

    restore_path = '/tmp/sublime_restored'
    restore_dirs = [j.system.fs.pathRemoveDirPart(item, restore_path) for item in j.system.fs.listDirsInDir(restore_path, recursive=True)]
    assert restore_dirs == original_dirs , "Restore Failed!"
    
    # Linking
    filemgr = JSFileMgr(MDPath=metadata_path, cachePath=link_path)
    filemgr.linkRecipe("sublimeroot/bk/", "/tmp/sublime_link", "sublimebk")
    
    hardlink_path = '/tmp/sublime_link'
    restore_dirs = [j.system.fs.pathRemoveDirPart(item, hardlink_path) for item in j.system.fs.listDirsInDir(hardlink_path, recursive=True)]
    assert restore_dirs == original_dirs , "Hardlinking Failed!"


def test2():

    recipe="""
    /BTSYNC/WINDOWS/python27: : python27
    """
    filemgr=JSFileMgr(MDPath="/opt/backup/md_sublime")
    # filemgr.backupRecipe(recipe)

    filemgr.restore("python27","/tmp/python27")

    #do a test the dir is the same (can use blobstor code for that)

test0()

j.application.stop()


import JumpScale.baselib.performancetrace

p1=j.tools.performancetrace.profile('test0b()', globals=globals())

#TODO

j.application.stop()
