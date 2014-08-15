
#build standallone
cython --embed hw.py
gcc $CFLAGS -I/usr/include/python2.7 -o hw hw.c -lpython2.7 -lpthread -lm -lutil -ldl
./hw

#build module
##python setup.py build_ext --inplace
