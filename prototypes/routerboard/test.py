import os
import struct

from JumpScale import j

import JumpScale.lib.routerboard

j.application.start("routerboard")

# rb=j.clients.routerboard.get("192.168.56.2","vscalers","")
rb=j.clients.routerboard.get("192.168.56.2","admin","")

# r1=rb.ipaddr_getall()
# r2=rb.interface_getall()
# r3=rb.interface_getnames()

#carefull if single==True other ip addr will be removed
r4=rb.ipaddr_set("ether2","192.168.7.1/24",single=True)

# r4=rb.ipaddr_remove("10.3.3.3")

rb.backup("test","/tmp/")



j.application.stop()
