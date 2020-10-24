from cryptek import *
import codecs
from sha1_pp import sha1
import time

def hmac_sha1(key_b, msg_b, blocksize=64):
    if len(key_b) > blocksize:
        key = codecs.decode(sha1(key_b), 'hex')
    elif len(key_b) < blocksize:
        key_b += bytes( (-len(key_b)) % blocksize)
    
    o_key_pad = bxor(key_b, bytes([0x5c])*blocksize) 
    i_key_pad = bxor(key_b, bytes([0x36])*blocksize) 
    return sha1(o_key_pad + codecs.decode(sha1(i_key_pad+msg_b), 'hex'))

def insecure_compare(buf0, buf1):
    if len(buf0) != len(buf1):
        return False

    # Begin compare
    for i in range(len(buf0)):
        if buf0[i] != buf1[i]:
            return False
        time.sleep(0.001)
    return True

def server_compare(sig):
    if insecure_compare(hmac_key, sig):
        return 200
    else:
        return 500

if __name__ == "__main__":
    ## Choose random key and derive hmac key from it
    key_b = rand_bytes(16)
    fname = b"file_foo"
    hmac_key = codecs.decode(hmac_sha1(key_b, fname), 'hex')
    hmac_len = len(hmac_key)

    ## Abusing the timing leak guess a few bytes at a time so we can distinguish the times 
    sig = bytearray(hmac_len)
    for k in range(hmac_len):
        for byte in range(0,256):
            sig[k] = byte
            start = time.time()
            server_compare(sig)
            duration = time.time() - start
            if duration > (k+1)*0.001:
                #print(sig)
                break
    print(sig)

    
