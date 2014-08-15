import time


from JumpScale import j

j.application.start("youtrack")

import JumpScale.lib.youtrackclient



robot=j.tools.ms1.getRobot(cbip,cblogin,cbpasswd,spaceid)

robotdefinition="""

machine (m)
- list (l)

- new (create,c,n)
-- name
-- description (descr)
-- memsize  #size is 0.5,1,2,4,8,16 in GB
-- ssdsize  #10,20,30,40,100 in GB
-- type     #type:arch,fedora,ubuntu,centos,opensuse,zentyal,debian,ubuntu13.10,ubuntu14.04,w2012_std,w2012_ess
-- typeid   #id type id used, type cannot be used

- delete (del)
-- name (n)

- stop
-- name (n)

- start
-- name (n)

- snapshot
-- name (n)
-- snapshotname (sname)

- delete
-- name (n)

- tcpportforward
-- name (n)
-- machinetcpport
-- pubip
-- pubipport

- udpportforward
-- name (n)
-- machinetcpport
-- pubip
-- pubipport

- execssh
-- name (n)
-- script #predefined vars: $passwd,$ipaddr,$name

- setpasswd
-- name (n)
-- passwd (password)

- execcuisine (cuisine)
-- name (n)
-- script #predefined vars: $passwd,$ipaddr,$name

- execjs (execjumpscript,js,jumpscript)
-- name (n)
-- script #predefined vars: $passwd,$ipaddr,$name

- initjs (initjumpscale)
-- name (n)

- initjsdebug (initjumpscaledebug)
-- name (n)

####
global required variables
spacesecret=

example:

!machine.new
name=webserver
memsize=10
ssdsize=40
type=buntu14.04

!machine.execssh
name=webserver
script=...
echo $ipaddr > /etc/mytest/ipaddr
cat /etc/mytest/ipaddr
...

!machine.setpasswd
name=webserver
passwd=apasswd

!machine.cuisine
name=webserver
script=...
group_ensure("remote_admin")
user_ensure("admin")
group_user_ensure("remote_admin", admin")
...

!machine.initjsdebug
name=webserver

!machine.execjs
name=webserver
script=...
j.tools.startupmanager.startAll()
jp=j.packages.findByName("elasticsearch")
jp.install()
...

"""


txt="""
!machine.new
name=webserver
memsize=10
ssdsize=40
type=buntu14.04
"""

print robot.process(txt)

j.application.stop()
