from cryptek import *
import codecs

def encryption_fun(msg_b):
    prepend = b"comment1=cooking%20MCs;userdata="
    append  = b";comment2=%20like%20a%20pound%20of%20bacon"
    msg_b = prepend + msg_b.replace(b";",b"").replace(b"=",b"") + append
    #msg_b = PKCSpad(msg_b, blocksize)
    return CTR_encrypt(key_b, msg_b)

def is_admin(cipher):
    ptext = CTR_encrypt(key_b, cipher)
    print(ptext)
    for pair in ptext.split(b";"):
        key, val = pair.split(b"=")
        if key == b'admin' and val == b'true':
            return True

    return False

if __name__ == "__main__":
    ## Generate random key
    blocksize=16
    key_b = rand_bytes(blocksize)
    
    out = encryption_fun(bytes(blocksize))
    injected_txt = b"xxxxx;admin=true"

    buf = bytes(32) + injected_txt + bytes(len(out) - 32 - len(injected_txt) )
    out_mod = bxor(buf, out)

    print(is_admin(out))
    print(is_admin(out_mod))
