from cryptek import *
import codecs
import random
import time
from ex3p21 import *

def time_stamped():
    ini_stall = random.randint(40,1000)
    seed = int(time.time()) + ini_stall
    mt = MT19937_32(seed)
    return mt, ini_stall

def find_seed(output, ini_time=0):
    """ 'output' is the initial output of the PRNG"""
    tf = int(time.time()) + ini_time + random.randint(40,1000)
    for dt in range(0,2001):
        mt = MT19937_32(tf - dt)
        if mt() == output:
            return tf-dt
    print("Seed not found")
    return -1

if __name__ == "__main__":
    mt_time_stamped, t0 = time_stamped()
    out = mt_time_stamped()
    seed = find_seed(out, ini_time = t0)

    print(f"{mt_time_stamped.seed == seed}")
