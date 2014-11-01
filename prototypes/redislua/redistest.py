import time


from pprint import pprint
import cProfile
import pstats

from JumpScale import j

j.application.start("redistest")


r= j.clients.redis.getRedisClient("localhost",9999)

def perftest():
    lua = """
    local value = redis.call('GET', KEYS[1])
    value = tonumber(value)
    return value * ARGV[1]
    """
    multiply = r.register_script(lua)
    r.set('foo', 2)

    print "start"
    for i in range(1000):
        multiply(keys=['foo'], args=[5])
    print "stop"

# perftest()

lua=j.system.fs.fileGetContents("logs.lua")
tolog=r.register_script(lua)

print tolog(keys=["logs.test"],args=["test"])

j.application.stop()
