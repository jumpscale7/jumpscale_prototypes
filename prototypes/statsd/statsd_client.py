
from JumpScale import j

import statsd
c = statsd.StatsClient('localhost', 8125)
# c.incr('foo')  # Increment the 'foo' counter.
# c.timing('stats.timed', 320)  # Record a 320ms 'stats.timed'.

import time

for ii in range(100000):
    for i in range(1000):
        c.gauge("nic.1.packets.%s"%i,20000+i)
    time.sleep(0.1)

