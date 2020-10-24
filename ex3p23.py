from cryptek import *
import codecs
import random
import time


if __name__=="__main__":
    mt = MT19937_32(int(time.time()))
    state_size = 624
    original_state = mt.state.copy()
    
    cloned_state = []
    prng_output = []
    for k in range(state_size):
        prng_val = mt()
        state_val = untemper(prng_val, mt)
        cloned_state.append(state_val)
        prng_output.append(prng_val)
    
    mt_clone = MT19937_32(0) ## arb seed
    mt_clone.state = cloned_state

    ## Check it reproduces the same values
    prng_clone_output = []
    for k in range(state_size):
        prng_val = mt_clone()
        prng_clone_output.append(prng_val)

    print(prng_clone_output == prng_output)
    ## It should also give us all future values of the original object



