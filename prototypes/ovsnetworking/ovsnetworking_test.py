from JumpScale import j

j.application.start("jumpscale:ovsNetConfigexamples")

import JumpScale.lib.ovsnetconfig

nc=j.system.ovsnetconfig
nc.removeOldConfig()

nc.setBackplaneDhcp(interfacename="eth0",backplaneId=1)
# nc.setBackplane(interfacename="eth0",backplaneId=1,ipaddr="192.168.10.10/24",gw="192.168.10.1")

# layout=nc.getConfigFromSystem()
# print j.system.ovsnetconfig.getType("test")


# nc.newBridge(name="test",interface="dummy0")
# j.system.process.execute("modprobe dummy")


j.application.stop()