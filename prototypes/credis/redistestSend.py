import time

from pprint import pprint
import cProfile
import pstats

from JumpScale import j

j.application.start("redistest")

import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

print "start send"
for i in range(10000):
    r.publish(1, "a test")


j.application.stop()
