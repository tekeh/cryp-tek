from cryptek import *
import codecs
from random import choice, randint
import time
import string


if __name__=="__main__":
    msg_len = 14
    inj_b = b"A"*msg_len
    prefix = ''.join([choice(string.ascii_letters) for _ in range(randint(4,20))])
    prefix = prefix.encode()
    msg_b = prefix + inj_b
   
    ## Use random seed to encrypt
    seed = randint(0, 2**16)
    ct = MT_streamcipher(seed, msg_b)
    
    ## Brute forcing 16-bit is pretty fast
    for sg in range(2**16):
        mt = MT19937_32(sg)
        ct_g = MT_streamcipher(sg, b"A"*50) ## Attacker knows how it works afterall...
        out = bxor(ct, ct_g[:len(ct)]) 
        if out.count(bytes(1)) >= msg_len:
            print(f"Found. Seed = {sg}")
            break

    ## part b) seems quite similar
