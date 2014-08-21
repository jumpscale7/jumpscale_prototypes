from JumpScale import j
j.application.start('puppettest')

import JumpScale.lib.puppet

import JumpScale.baselib.remote.fabric

j.tools.puppet.install()


##TODO


j.application.stop()
