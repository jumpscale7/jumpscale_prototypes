import time


from JumpScale import j

j.application.start("youtrack")

import JumpScale.lib.youtrackclient

robot=j.tools.youtrack.getRobot("http://incubaid.myjetbrains.com/youtrack/")

txt="""
login=despiegk
passwd=

# help

#!proj.list

# !u.r

!story.new 
project=ops
name=atest
descr=...
this is a test

2 lines
#
prio=4
who=despiegk

# !p.r

# !story.l
# project=jumpscale
# state=open
# #start=0
# max=10
# #filter

!proj.del
id=atest

# !help.definition
# !help.cmds

"""

print robot.process(txt)

j.application.stop()
