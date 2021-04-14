from cryptek import *
import codecs
import random

string_list = [ b"MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
        b"MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
        b"MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
        b"MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
        b"MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
        b"MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
        b"MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
        b"MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
        b"MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
        b"MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"
        ]

def encrypt_random_string():
    msg_b = codecs.decode(random.choice(string_list), 'base64')
    msg_b = PKCSpad(msg_b, blocksize)
    cipher = CBC_encrypt(key_b, IV, msg_b)
    return cipher

def padding_oracle(cipher):
    """
    Returns True if the decrypted message has a valid padding
    """
    msg_b = b''.join(CBC_decrypt(key_b, IV, cipher))
    try:
        PKCS_validation(msg_b)
        return True
    except:
        return False

if __name__ == "__main__":
    blocksize = 16

    ## random key and IV for global use
    key_b = rand_bytes(blocksize)
    IV = rand_bytes(blocksize)

    ## Set up string to append to
    msg_contents = b''
    ## tamper with the last byte until you get a valid padding
    cipher = bytearray(IV + encrypt_random_string())
    blocks = len(cipher)//blocksize
    correct_pad_bool = False
    for j in range(blocks, 1, -1):
        random_cipher = cipher[:j*blocksize]
        block_contents = b''
        for k in range(1, blocksize+1):
            correct_pad_bool = False
            i=255
            while not correct_pad_bool and i >=0: 
                ## modify the final byte on the last block
                for l in range(1,k):
                    random_cipher[(j-1)*blocksize - l] ^= k ^ block_contents[-l]
                random_cipher[(j-1)*blocksize - k] ^= i
                #print(f"(i, k, l) = {1}, {k}")
                correct_pad_bool = padding_oracle(random_cipher)
                for l in range(1,k):
                    random_cipher[(j-1)*blocksize - l] ^= k ^ block_contents[-l]
                random_cipher[(j-1)*blocksize - k] ^= i
                #random_cipher[(j-1)*blocksize - k)] ^= i
                i -= 1
            #print(i, k)
            block_contents = bytes([(i+1) ^ k]) + block_contents
            #print(block_contents)
        msg_contents = block_contents + msg_contents
    print(msg_contents)



