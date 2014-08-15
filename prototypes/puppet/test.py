from JumpScale import j
j.application.start('puppettest')

import JumpScale.lib.puppet

import JumpScale.baselib.remote.fabric

j.tools.puppet.install()


from IPython import embed
print "DEBUG NOW id"
embed()


j.application.stop()
