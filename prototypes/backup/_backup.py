

from JumpScale import j

j.application.start("jumpscale:backup")

recipe="""
$JSAPPS/apps : * : $DEST/apps
"""

JSAPPS="/BTSYNC/WINDOWS/JSAPPS"
DEST="/opt/backup/md_jsapps/"
STOR="/opt/backup/stor"

recipe=recipe.replace("$JSAPPS",JSAPPS)
recipe=recipe.replace("$DEST",DEST)

excludes=["*.pyc"]

def normalize(path):
    path=path.replace("'","\\'")
    path=path.replace("[","\\[")
    path=path.replace("]","\\]")
    return path

class Item():
    def __init__(self,data=""):
        state="start"
        self.hash=""
        self.text=""        
        if data<>"":
            for line in data.split("\n"):
                if line.strip()=="" or line[0]=="#":
                    continue
                if line.find("#######")<>-1:
                    state="text"
                    continue
                if state=="start": 
                    key,value=line.split(":")
                    self.__dict__[key.strip()]=value.strip()                
                if state=="text":
                    self.text+="%s\n"%line

    def __repr__(self):
        out=""
        for key,value in self.__dict__.iteritems():
            if key<>"text":
                out+="%s:%s\n"%(key,value)
        out+="####################################################\n"
        out+=self.text
        return out

    __str__=__repr__

errors=[]

def link(src,dest):
    j.system.fs.createDir(j.system.fs.getDirName(dest))
    print "link:%s %s"%(src,dest)
    # j.system.fs.hardlinkFile(srcfull2,dest)
    if j.system.fs.exists(path=dest):
        stat=j.system.fs.statPath(dest)
        if stat.st_nlink<2:                    
            raise RuntimeError("only support linked files")
    else:
        cmd="ln '%s' '%s'"%(normalize(src),normalize(dest))
        try:
            j.system.process.execute(cmd)
        except Exception,e:
            print "ERROR",
            print cmd
            print e
            errors.append(["link",cmd,e])


def backup(src,dest):
    j.system.fs.createDir(j.system.fs.getDirName(dest))
    print "backup:%s %s"%(src,dest)
    # j.system.fs.hardlinkFile(srcfull2,dest)
    if j.system.fs.exists(path=dest):
        stat=j.system.fs.statPath(dest)
        if not stat.st_nlink==1:
            raise RuntimeError("cannot be linked")
    item=Item()    
    item.hash=j.tools.hash.md5(src)
    j.system.fs.writeFile(str(item),dest)
    from IPython import embed
    print "DEBUG NOW uuu"
    embed()
    o



def do(sourcedir,parts,dest,action):
    sourcedir=sourcedir.strip()
    dest=dest.strip()
    if parts.find("*")<>-1:
        parts=",".join(j.system.fs.listDirsInDir(sourcedir, recursive=False, dirNameOnly=True, findDirectorySymlinks=True))

    for sourcepart in parts.split(","):
        sourcepart=sourcepart.strip()
        srcfull=j.system.fs.joinPaths(sourcedir,sourcepart)
        if not j.system.fs.exists(path=srcfull):
            raise RuntimeError("Could not find %s"%srcfull)

        for item in j.system.fs.listFilesInDir(srcfull,True,exclude=excludes):
            destpart=j.system.fs.pathRemoveDirPart(item,sourcedir,True)
            srcpart2=j.system.fs.pathRemoveDirPart(item,srcfull,True)
            destfull=j.system.fs.joinPaths(dest,destpart)
            srcfull2=j.system.fs.joinPaths(srcfull,srcpart2)

            action(srcfull2,destfull)
           

for line in recipe.split("\n"):
    if line.strip()=="" or line[0]=="#":
        continue
    source,sourceparts,dest=line.split(":")
    do(source,sourceparts,dest,backup)

if len(errors)>0:
    print "#############ERRORS###################"
    print "\n".join(errors)

# mount -o bind apps apps


j.application.stop()