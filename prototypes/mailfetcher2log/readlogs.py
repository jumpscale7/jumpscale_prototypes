import time

from pprint import pprint
import cProfile
import pstats

from JumpScale import j

j.application.start("loadlogtest")


lhandler = j.apps.acloudops.actionlogger.extensions.loghandler

j.core.osis.destroy("acloudops")  # remove all existing objects & indexes

lhandler.readLogs("prod")


j.application.stop()
