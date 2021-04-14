from cryptek import *
import codecs
import random
import time

if __name__ == "__main__":
    # Seed for the PRNG
    seed = int(time.time())
    mt = MT19937_32(seed)
    out = mt() ## first 32 bit output
