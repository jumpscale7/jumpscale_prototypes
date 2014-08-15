import time

from pprint import pprint
import cProfile
import pstats

from JumpScale import j

j.application.start("querytest")

# lh = j.apps.acloudops.actionlogger.extensions.loghandler
# lh.loadTypes()

es = j.clients.elasticsearch.get()

j.application.stop()
