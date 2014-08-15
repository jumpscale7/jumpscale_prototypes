

from JumpScale import j

j.application.start("jumpscale:linker")

recipe="""
$JSAPPS/apps : Kingsoft,doublecmd,sublimetext : $HOME/apps
"""

JSAPPS="/BTSYNC/WINDOWS/JSAPPS"
HOME="/BTSYNC/isabelle"

recipe=recipe.replace("$JSAPPS",JSAPPS)
recipe=recipe.replace("$HOME",HOME)

def normalize(path):
    path=path.replace("'","\\'")
    path=path.replace("[","\\[")
    path=path.replace("]","\\]")
    return path

errors=[]

def do(sourcedir,parts,dest):
    sourcedir=sourcedir.strip()
    dest=dest.strip()
    if parts.find("*")<>-1:
        from IPython import embed
        print "DEBUG NOW id"
        embed()

    for sourcepart in parts.split(","):
        sourcepart=sourcepart.strip()
        srcfull=j.system.fs.joinPaths(sourcedir,sourcepart)
        if not j.system.fs.exists(path=srcfull):
            raise RuntimeError("Could not find %s"%srcfull)

        for item in j.system.fs.listFilesInDir(srcfull,True):
            destpart=j.system.fs.pathRemoveDirPart(item,sourcedir,True)
            srcpart2=j.system.fs.pathRemoveDirPart(item,srcfull,True)
            destfull=j.system.fs.joinPaths(dest,destpart)
            srcfull2=j.system.fs.joinPaths(srcfull,srcpart2)
            j.system.fs.createDir(j.system.fs.getDirName(destfull))
            print "link:%s %s"%(srcfull2,destfull)
            # j.system.fs.hardlinkFile(srcfull2,destfull)
            if j.system.fs.exists(path=destfull):
                stat=j.system.fs.statPath(destfull)
                if stat.st_nlink<2:                    
                    raise RuntimeError("only support linked files")
            else:

                cmd="ln '%s' '%s'"%(normalize(srcfull2),normalize(destfull))
                try:
                    j.system.process.execute(cmd)
                except Exception,e:
                    print "ERROR",
                    print cmd
                    print e
                    errors.append([cmd,e])
           

for line in recipe.split("\n"):
    if line.strip()=="" or line[0]=="#":
        continue
    source,sourceparts,dest=line.split(":")
    do(source,sourceparts,dest)

from IPython import embed
print "DEBUG NOW uuu"
embed()


# mount -o bind apps apps


j.application.stop()