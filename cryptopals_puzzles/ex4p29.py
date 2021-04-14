from cryptek import *
import codecs
from sha1_pp import sha1
import struct

def prefix_mac(key_b, msg_b, reg_overwrite=None):
    return sha1(key_b+msg_b, reg_overwrite=reg_overwrite)

def compute_md_pad(msg_b, prelen=16):
    ml_bytes = len(msg_b) + prelen
    ml_bits = 8 * ml_bytes
    ## Append bit '1' to the message
    pad=b''
    pad += b'\x80'
    pad += b'\x00' * ((56 - (ml_bytes + 1) % 64) % 64)    
    pad += struct.pack(b'>Q', ml_bits)    
    return pad 


if __name__ == "__main__":
    ## Can make key length random and then iterate, for added complexity.

    ## Generate random key
    key_s =16
    key_b = rand_bytes(key_s)
    msg = b"ICE, ICE, BABY"

    ## Hash to forge
    hash_b = prefix_mac(key_b, msg)

    ## Copy state of the registers
    sha_reg =  [int(hash_b[i*8:(i+1)*8], 16) for i in range(0, 5)] 
    
    ##
    added_data = b"DUNDUNDUN DUN DUHDUH DUN" 
    total_prefix_len = 16 + len(msg) + len(compute_md_pad(msg, prelen=16))
    hash_forge = sha1(added_data, reg_overwrite=sha_reg, length =(total_prefix_len + len(ext)) )

    ## Compare to true extended message
    extended_msg = msg + compute_md_pad(msg) + ext
    true_hash = prefix_mac(key_b, extended_msg)

    print(f"True sig: {true_hash}\nForgery: {hash_forge}")
    

