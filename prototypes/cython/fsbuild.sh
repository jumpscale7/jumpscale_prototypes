
#build standallone
cython --embed -2 -v fstest2.py
gcc $CFLAGS -I/usr/include/python2.7 -o fstest2 fstest2.c -lpython2.7 -lpthread -lm -lutil -ldl
./fstest2

#build module
##python setup.py build_ext --inplace
