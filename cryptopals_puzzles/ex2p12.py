from cryptek import *
import codecs

def ECB_oracle(msg_b):

    ## Pre and append random number of bytes to message
    append_b = b"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\naGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\ndXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\nYnkK\n"

    msg_b = msg_b + codecs.decode(append_b, 'base64')
    return AES_encrypt(key_b, msg_b)

if __name__ == "__main__":
    ## Generate fixed random key
    key_b = rand_bytes(16)
    
    ## Discover blocksize
    cipher_len = len(ECB_oracle(b''))
    i=1
    while True:
       new_len = len(ECB_oracle(b'A'*i))
       if new_len > cipher_len:
           blocksize = new_len - cipher_len
           break
       i = i+1

    print(f"The blocksize is {blocksize}")

    ## Detect that the oracle is using ECB
    ECB_CBC_oracle( ECB_oracle )
    print(f"{ECB_oracle.pred} Detected")

    ## Determine bytes
    blocks = cipher_len//blocksize
    reconstructed_msg= b''
    for j in range(blocks):
        unknown_b = b''
        for k in range(blocksize-1,-1,-1):
            prepend_b = b"A"*k
            msg_b = ECB_oracle(prepend_b)
            msg_b_block_j =  msg_b[j*blocksize:(j+1)*blocksize]
            for m in range(256):
                byte_m = bytes([m])
                out = ECB_oracle(prepend_b + reconstructed_msg + unknown_b + byte_m)[j*blocksize:(j+1)*blocksize]
                if out == msg_b_block_j:
                    unknown_b = unknown_b + byte_m
                    break
        reconstructed_msg += unknown_b

    print(reconstructed_msg)


    
    
