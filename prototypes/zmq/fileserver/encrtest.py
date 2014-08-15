# File Transfer model #3
#
# In which the client requests each chunk individually, using
# command pipelining to give us a credit-based flow control.

import os
import time
import pysodium

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



def main():

    # writeBigFile()

    # Start child threads
    
    start=time.time()
    print "start"

    #1MB block
    block1MB=""
    for i in range(1024*1024):
        block1MB+="a"

    block1KB=""
    for i in range(1024):
        block1KB+="a"


    # loop until client tells us it's done
    nr=1000
    for i in range(nr):
        encode(block1MB)

    stop=time.time()
    # print "MB/sec:%s"%(float(size)/(stop-start))
    print "OPS/sec:%s"%(float(nr)/(stop-start))


if __name__ == '__main__':
    main()
