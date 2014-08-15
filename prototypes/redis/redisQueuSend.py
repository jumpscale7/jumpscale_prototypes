import time

from pprint import pprint
import cProfile
import pstats

from JumpScale import j

import JumpScale.baselib.redis

j.application.start("redistest")

q=j.clients.redis.getRedisQueue("127.0.0.1", 7768, 'work')
q2=j.clients.redis.getRedisQueue("127.0.0.1", 7768, 'return')

nr=10000
j.base.timer.start()
print "start send"
for i in range(nr):
    q.put(i)
    i2=int(q2.get())
    assert i==i2    

j.base.timer.stop(nr)

j.application.stop()
