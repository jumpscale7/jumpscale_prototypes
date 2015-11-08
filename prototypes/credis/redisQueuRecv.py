import time

from pprint import pprint
# import cProfile
# import pstats

from JumpScale import j
# import JumpScale.baselib.redis2

j.application.start("redistest")

from Redis import *
from RedisQueue import *


redis=Redis(port=9999)

q=RedisQueue("work","queues",redis)
q2=RedisQueue("return","queues",redis)


# q=j.clients.redis.getRedisQueue("127.0.0.1", 9999, 'work')
# q2=j.clients.redis.getRedisQueue("127.0.0.1", 9999, 'return')

print "start recv"
while True:
    data=q.get()
    # res = float(data)    
    # if int(res) == int(round(res / 1000, 0) * 1000):
    #     print res
    q2.put(data)



j.application.stop()
