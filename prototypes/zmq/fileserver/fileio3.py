# File Transfer model #3
#
# In which the client requests each chunk individually, using
# command pipelining to give us a credit-based flow control.

import os
from threading import Thread
import time
import zmq
import pysodium
from zhelpers import socket_set_hwm, zpipe

# CHUNK_SIZE = 250000 #250kbyte
CHUNK_SIZE = 64000 
#CHUNK_SIZE = 4000 


import nacl.secret
import nacl.utils

# This must be kept secret, this is the combination to your safe
key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)

# This is your safe, you can use it to encrypt or decrypt messages
box = nacl.secret.SecretBox(key)
# pysodium.randombytes(24)

# This is a nonce, it *MUST* only be used once, but it is not considered
#   secret and can be transmitted or stored alongside the ciphertext. A
#   good source of nonce is just 24 random bytes.
nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)

def encode(message):

    # This is our message to send, it must be a bytestring as SecretBox will
    #   treat is as just a binary blob of data.
    # message = b"The president will be exiting through the lower levels"

    # Encrypt our message, it will be exactly 40 bytes longer than the original
    #   message as it stores authentication information and nonce alongside it.
    encrypted = box.encrypt(message, nonce)
    # encrypted=pysodium.crypto_secretbox(message,nonce,key)

    # # Decrypt our message, an exception will be raised if the encryption was
    # #   tampered with or there was otherwise an error.
    # plaintext = box.decrypt(encrypted)

    return encrypted

def client_thread(ctx, pipe):
    dealer = ctx.socket(zmq.DEALER)
    socket_set_hwm(dealer, 1)
    dealer.connect("tcp://127.0.0.1:6000")

    total = 0       # Total bytes received
    chunks = 0      # Total chunks received

    while True:
        # ask for next chunk
        dealer.send_multipart([
            b"fetch",
            b"%i" % total,
            b"%i" % CHUNK_SIZE
        ])

        try:
            chunk = dealer.recv()
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                return   # shutting down, quit
            else:
                raise

        chunks += 1
        size = len(chunk)
        total += size
        if size < CHUNK_SIZE:
            break   # Last chunk received; exit

    print ("%i chunks received, %i bytes" % (chunks, total))
    pipe.send(b"%s"%chunks)

# .split File server thread
# The server thread waits for a chunk request from a client,
# reads that chunk and sends it back to the client:

def server_thread(ctx):
    file = open("testdata", "r")

    router = ctx.socket(zmq.ROUTER)

    router.bind("tcp://*:6000")

    while True:
        # First frame in each message is the sender identity
        # Second frame is "fetch" command
        try:
            msg = router.recv_multipart()
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                return   # shutting down, quit
            else:
                raise

        identity, command, offset_str, chunksz_str = msg

        assert command == b"fetch"

        offset = int(offset_str)
        chunksz = int(chunksz_str)

        # Read chunk of data from file
        file.seek(offset, os.SEEK_SET)
        data = file.read(chunksz)

        data=encode(data)

        # Send resulting chunk to client
        router.send_multipart([identity, data])

size=1024 #GB

def writeBigFile():
    file = open("testdata", "w")
    print "createblock"
    #1MB block
    block=""
    for i in range(1024*1024):
        block+="a"
    print "writeBigFile"
    
    for i in range(size):
        file.write(block)
    file.close()
    print "done"

# The main task is just the same as in the first model.
# .skip

def main():

    # writeBigFile()

    # Start child threads
    ctx = zmq.Context()
    a,b = zpipe(ctx)

    client = Thread(target=client_thread, args=(ctx, b))
    server = Thread(target=server_thread, args=(ctx,))
    
    client.start()
    start=time.time()
    print "start"
    server.start()

    # loop until client tells us it's done
    try:
        chunks= int(a.recv())
        stop=time.time()
        print "MB/sec:%s"%(float(size)/(stop-start))
        print "OPS/sec:%s"%(float(chunks)/(stop-start))

    except KeyboardInterrupt:
        pass
    del a,b
    ctx.term()

if __name__ == '__main__':
    main()
