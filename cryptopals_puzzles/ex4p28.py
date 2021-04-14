from cryptek import *
import codecs
from sha1_pp import sha1


if __name__ == "__main__":
    ## Generate random key
    blocksize=16
    key_b = rand_bytes(blocksize)
    print( prefix_mac(key_b, b"Hello Hello I'm the message") ) 
