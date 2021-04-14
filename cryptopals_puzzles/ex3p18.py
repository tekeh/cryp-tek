from cryptek import *
import codecs
import math

encrypted_msg = b"L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="

if __name__ == "__main__":
    blocksize = 16

    txt = codecs.decode(encrypted_msg, 'base64')
    key_b = b"YELLOW SUBMARINE"
    
    out = CTR_encrypt(key_b, txt)
    print(out)


