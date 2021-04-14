from cryptek import *
import codecs
import string

def ascii_compliant(msg_b, key_b, IV):
    p_text_blocks = CBC_decrypt(key_b, IV, msg_b)
    txt = b''.join(p_text_blocks)
    for byte in txt: ## Timing attack also possible here
        if string.ascii_letters.encode().__contains__(byte):
            continue
        else:
            print("Ascii encoding error")
            return p_text_blocks
    print("The string is ascii compliant")
    return [0]

if __name__ == "__main__":
    ## Generate random key
    blocksize=16
    key_b = rand_bytes(blocksize)

    msg_b = b"Hello, hello, this is a test message which is at least 3 times the block length."
    ct = CBC_encrypt(key_b, key_b, msg_b)
    ct_blocks = [ct[i*blocksize:(i+1)*blocksize] for i in range(len(ct)//blocksize)]

    ## Attacker action - modify message midflight
    ct_blocks[2] = ct_blocks[0]
    ct_blocks[1] = bytes(blocksize)

    ## Reciever decrypts and raises error - returns decrypted pt to attacker
    pt_blocks = ascii_compliant(b''.join(ct_blocks), key_b, key_b)
    derived_key = bxor(pt_blocks[0], pt_blocks[2])
    print(derived_key == key_b)
