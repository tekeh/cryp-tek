from cryptek import *
import codecs
import random
import time

class PRNG:
    def __init__(self, seed):
        self.seed = seed
    

class MT19937_32(PRNG):
    def __init__(self, seed):
        PRNG.__init__(self, seed)
        ## Fixed parameters of the implementation
        self.w = 32 
        self.n = 624
        self.m = 397
        self.r = 31
        self.a = int("9908B0DF", 16)
        self.b = int("9D2C5680", 16)
        self.s = 7
        self.t = 15
        self.u = 11
        self.d = int("FFFFFFFF", 16)
        self.l = 18
        self.c = int("EFC60000", 16)
        self.f = 1812433253

        self.index = 0
        self.state = [0]*self.n
        self.lower_mask =  (1 << self.r) - 1 ## lower r bits = 1
        self.upper_mask = ((1 << self.w) - 1) ^ self.lower_mask ## upper w-r bit = 1

        ## initialise the state and twist
        self.initialise_state()
        #self.twist()

    def __call__(self):
        if self.index >= self.n:
            self.twist()
            self.index = 0
        rand_word = self.temper(self.index)
        self.index += 1
        return rand_word

    def initialise_state(self):
        self.state[0] = self.seed
        for i in range(1,self.n):
            xim1 = self.state[i-1]
            self.state[i] = ((1 << self.w) - 1) & ( self.f * (xim1 ^ ( xim1 >> (self.w-2) ) ) + i ) ## lowest w bits 
        
    def twist(self):
        """Twist transformation"""
        self.state += [0]*self.n
        for k in range(self.n):
            concat = (self.upper_mask & self.state[k]) | (self.lower_mask & self.state[k+1])
            xA = concat >> 1
            if (xA & 1): # True is LSB is 1
                xA = xA ^ self.a
            self.state[self.n+k] = self.state[self.m+k] ^ xA
        self.state = self.state[self.n:]

    def temper(self, index):
        x = self.state[index]
        y = x ^ ( (x >> self.u) & self.d )
        y = y ^ ( (y << self.s) & self.b )
        y = y ^ ( (y << self.t) & self.c )
        z = y ^   (y >> self.l)
        return z



if __name__ == "__main__":
    # Seed for the PRNG
    seed = int(time.time())
    mt = MT19937_32(seed)
    out = mt() ## first 32 bit output
