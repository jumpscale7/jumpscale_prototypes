
from JumpScale import j

j.application.start("perftest")  # md=metadata

j.logger.consoleloglevel = 6

nr = 1000000


class Obj():

    def __init__(self):
        self.name = "aname"
        self.cmd = "mycommand"
        self.args = {}
        self.args["parm1"] = "a parameter"
        self.args["parm2"] = 20
        self.nr = 0
obj = Obj()

import JumpScale.baselib.serializers

j.base.timer.start()
for i in range(nr):
    obj.nr = i
    data = j.db.serializers.ujson.dumps(obj.__dict__)
    j.db.serializers.ujson.loads(data)
j.base.timer.stop(nr)


j.application.stop()
