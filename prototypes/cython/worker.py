class HardWorker(object):

    u"Almost Sisyphos"

    def __init__(self, task):
        self.task = task

    def work_hard(self, repeat=100):
        for i in range(repeat):
            self.task()
        print "1"


def add_simple_stuff():
    x = 1 + 1

HardWorker(add_simple_stuff).work_hard()
