from cryptek import *
import codecs
from sha1_pp import sha1
import time

def insecure_compare(buf0, buf1):
    if len(buf0) != len(buf1):
        return False

    # Begin compare
    for i in range(len(buf0)):
        if buf0[i] != buf1[i]:
            return False
        time.sleep(0.05)
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

    ## Abusing the timing leak -this may take a while
    sig = bytearray(hmac_len)
    for k in range(hmac_len):
        for byte in range(0,256):
            sig[k] = byte
            start = time.time()
            server_compare(sig)
            duration = time.time() - start
            if duration > (k+1)*0.05:
                #print(sig)
                break
    print(sig)

    
