from cryptek import *
import codecs
import random
import time

def untemper(z, mt):
    """Inverse of the temper function in the Mersenne Twister algorithm. Takes an MT PRNG object"""
    z = z ^ (  z >> mt.l )
    z = z ^ ( (z << mt.t) & mt.c)
    z = z ^ ( (z << mt.s) & mt.b)
    y = z ^ ( (z >> mt.u) & mt.d)
    return y


    
    
