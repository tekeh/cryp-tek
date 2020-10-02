from cryptek import *
import codecs
from random import randint

def random_encryption(msg_b):

    ## Pre and append random number of bytes to message
    prepend_num = randint(5,10)
    append_num  = randint(5,10)
    msg_b = rand_bytes(prepend_num) + msg_b + rand_bytes(append_num)

    ##generate random key
    key_b = rand_bytes(16)

    ## Choose mode
    mode = randint(0,1)
    if mode:
        random_encryption.actual="ECB"
        return AES_encrypt(key_b, msg_b)
    else:
        random_encryption.actual="CBC"
        IV = rand_bytes(16)
        return CBC_encrypt(key_b, IV, msg_b)

if __name__ == "__main__":
     
    errors = 0
    for k in range(1000):
        ECB_CBC_oracle(random_encryption)
        if random_encryption.actual != random_encryption.pred:
            errors += 1
    print(f"Finished with {errors} incorrect predictions")
