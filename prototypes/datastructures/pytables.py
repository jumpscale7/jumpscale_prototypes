from JumpScale import j

j.application.start("pytables")

import sys
import time

#@todo example no longer working,test & fix

# huge table, ideal for lots of analytics data processing

try:
    import tables
except:
    print "Try to install tables"
    j.system.process.executeWithoutPipe("apt-get install python-numexpr cython python-tables", True, True)
    # j.system.process.executeWithoutPipe("easy_install tables",True,True)
    import tables

from tables import IsDescription, StringCol, Int64Col, UInt16Col, UInt8Col, Int32Col, Float32Col, Float64Col, openFile


class Particle(IsDescription):
    name = StringCol(16)   # 16-character String
    idnumber = Int64Col()      # Signed 64-bit integer
    ADCcount = UInt16Col()     # Unsigned short integer
    TDCcount = UInt8Col()      # unsigned byte
    grid_i = Int32Col()      # 32-bit integer
    grid_j = Int32Col()      # 32-bit integer
    pressure = Float32Col()    # float  (single-precision)
    energy = Float64Col()    # double (double-precision)

m = 1000000


def create():

    h5file = openFile("/tmp/tutorial1.h5", mode="w", title="Test file")

    group = h5file.createGroup("/", 'detector', 'Detector information')
    table = h5file.createTable(group, 'readout', Particle, "Readout example")

    particle = table.row

    print "populate db"

    for i in xrange(m):
        particle['name'] = 'Particle: %6d' % (i)
        particle['TDCcount'] = i % 256
        particle['ADCcount'] = (i * 256) % (1 << 16)
        particle['grid_i'] = i
        particle['grid_j'] = 10 - i
        particle['pressure'] = float(i * i)
        particle['energy'] = float(particle['pressure'] ** 4)
        particle['idnumber'] = i * (2 ** 34)
        # Insert a new particle record
        particle.append()

    table.flush()

    table.close()

    h5file.close()


def oopen():
    f = openFile("/tmp/tutorial1.h5")
    return f.root.detector.readout

# create()
particle = oopen()

print "start query test"
for i in range(10000):
    rnd = j.base.idgenerator.generateRandomInt(1, m - 1)
    w = particle[rnd]

print "done query test"

time.sleep(100)

return particle

j.application.stop()
