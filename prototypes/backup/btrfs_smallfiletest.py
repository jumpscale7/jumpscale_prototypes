from JumpScale import j

j.application.start("jumpscale:btrfstest")

a="aabbccddeeffgghcdd"
patha="a dir certain l"
pathb="this is a name"

content=[]

def test0():
    for i in range(10000):
        print i
        for i2 in range(100):
            p=j.system.fs.joinPaths("/mnt","btrfs","1",patha+str(i),pathb+str(i2))
            j.system.fs.createDir(j.system.fs.getDirName(p))
            j.system.fs.writeFile(p,a+str(i)+str(i2))

test0()

j.application.stop()
