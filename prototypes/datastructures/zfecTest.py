import os
import struct

from JumpScale import j

j.application.start("zfectest")

#@todo NOT WORKING, need to  implement

import zfec
encoder = zfec.Encoder(10, 14)

filename = "/var/lib/libvirt/images/Ubuntu.img"

counter = 0


def encode(counter, series):
    counter += 1
    counterSeries = 0
    seriesOut = encoder.encode(series)
    for out in seriesOut:
        counterSeries += 1
        pathout = "out/Ubuntu.img.%s_%s" % (counter, counterSeries)
        j.system.fs.writeFile(pathout, out)
        print "%s_%s" % (counter, counterSeries)
    return counter


size = 0
series = []
block = "start"
with open(filename) as fp:
    while block != False:
        block = fp.read(5000000)
        size += len(block)
        series.append(block)
        print size / 1024 / 1024
        if len(series) > 9:
            counter = ecode(counter, series)
            series = []

j.application.stop()
