from JumpScale import j

j.application.appname = "archinstaller"
j.application.start()

remote="192.168.248.113"
passwd="rooter"

import JumpScale.baselib.remote


### FIRST DO
help="""
#On a live system using systemd: (2012.10.06 or later) do
systemctl start sshd
rc.d start sshd
passwd
"""

print help

c=j.remote.cuisine.api
j.remote.cuisine.fabric.env["password"]=passwd
c.connect(remote)

cl=j.tools.expect.new("sh")
#login over ssh
cl.send("ssh root@%s"%remote)
result=cl.expect("password:")
if result<>0:
    raise RuntimeError("could not login over ssh, expect 'password:' as return when doing ssh")

result=cl.expect("password:")
if result<>0:
    raise RuntimeError("could not login over ssh, expect 'password:' as return when doing ssh")


cl.send(passwd)
result=cl.expect("#")
if result<>0:
    raise RuntimeError("could not login")

# cl.expect("#",timeout=0.5)

chroot=False

def pacmanInstall(name):
    if chroot:
        # cl.executeStep("echo Y | pacman -S %s\n"%name,"#",timeout=1200)
        c.run("echo Y | pacman -S %s\n"%name)
    else:
        # cl.executeStep("echo Y | pacstrap -i /mnt %s\n"%name,"#",timeout=1200)
        c.run("echo Y | pacstrap -i /mnt %s\n"%name)

def pacman(cmd):
    cl.executeStep("echo Y | pacman %s\n"%cmd,"#")


def createPartitionsGPT():

#check there is a sda disk
    if not c.run("sfdisk -l").find("/dev/sda")<>-1:
        raise RuntimeError("did not find /dev/sda")
    
    main=cl.executeStep("gdisk /dev/sda\n","Command",errormsg="",timeout=1)

    check =["MBR: not present","BSD: not present","APM: not present","GPT: not present"]
    test=True
    for item in check:
        if main[0].find(item)<>-1:
            test=False
    if test==False:
        raise RuntimeError("Cannot continue, there is something on disk, needs to be cleaned completely")

        #@todo need, jan to dothis

    #create new disk
    cl.executeStep("n\n","Partition number")
    cl.executeStep("1\n","First sector")
    cl.executeStep("\n","Last sector")
    cl.executeStep("\n","Hex code")
    cl.executeStep("\n","Command") #hexcode just enter

    cl.executeStep("w\n","Do you want to proceed",timeout=10) #write the done action
    cl.executeStep("y\n","#") #enter to confirm operation


def createPartitionsFDISK():

    #check there is a sda disk
    if not c.run("sfdisk -l").find("/dev/sda")<>-1:
        raise RuntimeError("did not find /dev/sda")
    
    main=cl.executeStep("fdisk /dev/sda\n","Command",errormsg="",timeout=1)

    cl.executeStep("o\n","Command") #created dos disklabel

    #create partition 1
    cl.executeStep("n\n","default p") #created dos disklabel
    cl.executeStep("\n","Partition number")
    cl.executeStep("\n","First sector")
    cl.executeStep("\n","Last sector")

    cl.executeStep("w\n","#") #write to disk

def unmountArch():

    #kill all processes using something on /mnt
    c.process_kill("pacman")
    c.process_kill("pacstrap")
    c.process_kill("chroot")

    #umount mounts on /mnt
    todo=[]
    for line in c.run("mount").split("\n"):     
        if line.find(" on /mnt")<>-1:
            toumount=line.split(" on ")[1].split(" type ")[0]
            todo.append(toumount)

    todo.sort(reverse=True)

    for item in todo:
        print "umount %s"%item
        c.run("umount %s"%item)

def prepareArch():
    unmountArch()
    cmd='mkfs.ext4 /dev/sda1'
    c.run(cmd)
    #print partition (good for logging)
    c.run("lsblk /dev/sda")

def mountArch():
    unmountArch()
    c.run("mount /dev/sda1 /mnt")
    #remove lock if any
    c.file_unlink("/mnt/var/lib/pacman/db.lck")    

def installArch():
    mountArch()

    basepackages=['bash', 'bzip2', 'coreutils', 'cronie', 'cryptsetup', 'device-mapper', 'dhcpcd', 'diffutils', 'e2fsprogs', 'file', 'filesystem', 'findutils', \
        'gawk', 'gcc-libs', 'gettext', 'glibc', 'grep', 'gzip', 'inetutils', 'iproute2', 'iputils', 'jfsutils', 'less', 'licenses', 'linux', 'logrotate', 'lvm2', \
        'man-db', 'man-pages', 'mdadm', 'nano', 'netctl', 'pacman', 'pciutils', 'pcmciautils', 'perl', 'procps-ng', 'psmisc', 'reiserfsprogs', 's-nail', 'sed', \
        'shadow', 'sysfsutils', 'systemd-sysvcompat', 'tar', 'texinfo', 'usbutils', 'util-linux', 'vi', 'which', 'xfsprogs']

    for item in ["bash","linux","glibc","grub","findutils","grep"]:
        pacmanInstall(item)

    c.run("genfstab -U -p /mnt >> /mnt/etc/fstab")


def post():

    # mountArch()

    # cl.executeStep("arch-chroot /mnt","sh-4.2#")
    # chroot=True

    from IPython import embed
    print "DEBUG NOW post"
    embed()
    

    #clean cache for pacman
    pacman("-Scc")
    

# createPartitionsFDISK()
# prepareArch()
installArch()
post()

from IPython import embed
print "DEBUG NOW oo"
embed()

# c.repository_ensure_pacman(


j.application.stop()
