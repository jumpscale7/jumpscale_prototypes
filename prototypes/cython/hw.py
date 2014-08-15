
from JumpScale import j
import sys
import time

def hello_world():
    print "Welcome to Python %d.%d!" % sys.version_info[:2]

if __name__ == '__main__':
    j.application.start("pytables")
    hello_world()
    j.console.echo("test")
    j.application.stop()
