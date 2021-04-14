from cryptek import *
import codecs
from sha1_pp import sha1
import time
from itertools import product

## to be complete

def insecure_compare(buf0, buf1):
    if len(buf0) != len(buf1):
        return False

    # Begin compare
    for i in range(len(buf0)):
        if buf0[i] != buf1[i]:
            return False
        time.sleep(0.005)
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

    guess_size = 1 # 3 bytes at a time
    print(hmac_key)

    ## Abusing the timing leak guess a few bytes at a time so we can distinguish the times 
    sig = bytearray(hmac_len)
    best_time = 0
    for k in range(0, hmac_len, guess_size):
        best_chunk = (b"a", b"a")
        for byte_chunk in product(range(256), repeat=guess_size):
            sig[k:k+guess_size] = byte_chunk
            start = time.time()
            server_compare(sig)
            duration = time.time() - start
            if duration > best_time:
                best_chunk = byte_chunk
                best_time = duration 
        sig[k:k+guess_size] = best_chunk
        print(k, "\t", duration, "\n", sig)

