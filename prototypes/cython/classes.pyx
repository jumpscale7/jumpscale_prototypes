cdef class TestClass:

    cdef public int width, height
    cdef public char* name
    cdef public bytes bytes

    def __init__(self, w, h,name):
        self.width = w
        self.height = h
        self.name=name

    def describe(self):
        print "This shrubbery is", self.width, \
            "by", self.height, "cubits.",self.name