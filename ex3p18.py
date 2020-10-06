from cryptek import *
import codecs
import math

encrypted_msg = b"L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="

def CTR_encrypt(key_b, msg_b, nonce = bytes(8)):
    blocks = math.ceil(len(msg_b)/blocksize)
    bytestream = b''
    for k in range(blocks):
        ctr = nonce + k.to_bytes(8, byteorder='little')
        bytestream += AES_encrypt(key_b, ctr)
    cipher = bxor(msg_b, bytestream[:len(msg_b)])
    return cipher


if __name__ == "__main__":
    blocksize = 16

    txt = codecs.decode(encrypted_msg, 'base64')
    key_b = b"YELLOW SUBMARINE"
    
    out = CTR_encrypt(key_b, txt)
    print(out)


