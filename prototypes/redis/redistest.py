import time


from pprint import pprint
import cProfile
import pstats

from JumpScale import j

j.application.start("redistest")

import redis
r = redis.StrictRedis(host='localhost', port=7768, db=0)

ps = r.pubsub()
ps.subscribe([1])


# print "startlisten"
# while True:
    # info=ps.listen()

j.application.stop()
