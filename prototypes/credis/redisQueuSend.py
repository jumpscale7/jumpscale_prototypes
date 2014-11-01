import time

from Redis import *
from RedisQueue import *

from pprint import pprint
# import cProfile
# import pstats

from JumpScale import j

# import JumpScale.baselib.redis

j.application.start("redistest")

redis=Redis(port=9999)

redis.delete("queues:work")
redis.delete("queues:return")


q=RedisQueue("work","queues",redis)
q2=RedisQueue("return","queues",redis)

# q=RedisQueue("127.0.0.1", 9999, 'work')
# q2=j.clients.redis.getRedisQueue("127.0.0.1", 9999, 'return')

block=""
for i in range(1024*1):
    block+="a"

script="return {KEYS[1],KEYS[2],ARGV[1],ARGV[2]}"
script2="""

"""

sha=redis.scriptload(script)


def luatest():
    nr=10000
    j.base.timer.start()
    print "start send"
    for i in range(nr):
        result=redis.evalsha(sha,2,"akey","anotherkey","1",block)
    j.base.timer.stop(nr)
    return result

# result=luatest()

# print result

# j.application.stop()


nr=10000
j.base.timer.start()
print "start send"
for i in range(nr):
    q.put(block)
    result=q2.get()
    assert block==result    

j.base.timer.stop(nr)

j.application.stop()
