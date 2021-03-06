import codecs
import math
import argparse
import base64
from Crypto.Cipher import AES
from sha1_pp import sha1

## Class Definitions

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
        return ((1 << self.w) - 1) & z ## lowest w bits


#############################################################################################


def hex2b64(hex_str):
    """ 
    Converts given hex to base64 
    """
    b64_enc_str = codecs.encode(codecs.decode(hex_str, 'hex'), 'base64').decode()
    return b64_enc_str

def bxor(b1, b2):
    """
    XORS two equal length buffers (No input sanitation) 
    """
    result = bytearray(b1)
    for i, b in enumerate(b2):
        result[i] ^= b
    return bytes(result)

def plaintext_score(text):
    """
    Scores text on character frequencies, l1-distance
    """
    freq_dic = {'a':0.08498, 'b':0.01492, 'c': 0.02202, 'd':0.04253, 'e':0.11162, 'f':0.02228, 'g':0.02015, 'h':0.06094, 'i':0.07546, 'j':0.00153, 'k':0.01292, 'l':0.04025, 'm':0.02406, 'n':0.06749, 'o':0.07507, 'p':0.01929, 'q':0.00095, 'r':0.07587, 's':0.06327, 't':0.09356, 'u':0.02758, 'v':0.00978, 'w':0.02560, 'x':0.00150, 'y':0.01994, 'z':0.00077} ## Dictionary which has character frequencies from wiki:https://en.wikipedia.org/wiki/Letter_frequency
    score = 0
    text = ''.join(filter(str.isalpha, text))
    text = text.lower()
    num_letters = len(text)

    for char in freq_dic:
        emp_freq = text.count(char)/num_letters
        score += abs(emp_freq - freq_dic[char])

    return score/num_letters ## return average score per letter, to compare string of diffferent lengths

def xor_encrypt(buf, key):
    """
    implements repeating XOR with key on buf, Both must be binary
    """
    buffer_arr  = bytearray(buf)
    key_arr     = bytearray(key)
    len_buff    = len(buffer_arr)
    len_key     = len(key_arr)

    for i in range(len_buff):
        idx = i % len_key
        buffer_arr[i] ^= key_arr[idx]
    return bytes(buffer_arr)
        

def hamming_dist(b0, b1):
    """
    Computes the Hamming Distance between 2 bytes objects
    """
    buf0_bytes = bytearray(b0)
    buf1_bytes = bytearray(b1) ## in bytes
    buf0 = ''.join(['0'*(8 - len(bin(i).replace('0b',''))) + bin(i).replace('0b','') for i in buf0_bytes])
    buf1 = ''.join(['0'*(8 - len(bin(i).replace('0b',''))) + bin(i).replace('0b','') for i in buf1_bytes])
    edit_dis = [0 if i ==j else 1 for i, j in zip(buf0, buf1) ]

    return sum(edit_dis)

def AES_decrypt(key_b, msg_b):
    """
    Wrapper for Cryptography library's AES function
    """
    cipher = AES.new(key_b, AES.MODE_ECB)
    return cipher.decrypt(msg_b)

def AES_encrypt(key_b, msg_b):
    """
    Wrapper for Cryptography library's AES function
    """
    cipher = AES.new(key_b, AES.MODE_ECB)
    #msg_b = PKCSpad(msg_b, AES.block_size)
    return cipher.encrypt(msg_b)

def count_reps(x, bs):
    """
    x:  a bytearray
    bs: blocksize
    """
    chunks = [x[i:i+bs] for i in range(0, len(x), bs) ]
    return len(chunks) - len(set(chunks)), chunks

def PKCSpad(msg, blocklength):
    """
    Applies PKCS#7 padding to the msg (bytes object)
    """
    pad_num = (-len(msg)) % blocklength
    if pad_num == 0:
        pad_num = blocklength
    pad_msg = bytes([pad_num])*pad_num
    return msg + pad_msg

def PKCSstrip(msg):
    """
    Applies PKCS#7 padding to the msg (bytes object)
    """
    pad_num = msg[-1]
    msg = msg[:-pad_num]
    return msg

def PKCS_validation(str_b):
    """ 
    Validates whether given string has proper padding
    according to PKCS#7
    """
    pad_no = str_b[-1]
    byte_suffix = str_b[-pad_no:]
    unique_bytes = len(set(list(byte_suffix)))
    if unique_bytes != 1:
        raise Exception("Padding Error!")
    return PKCSstrip(str_b)

def CBC_mode(key_b, IV, msg_b):
    """ 16 byte key, and IV """
    msg_decrypt = []
    cipher = AES.new(key_b, AES.MODE_ECB)
    print(cipher)
    msg_chunks = [msg_b[i:i+16] for i in range(0, len(msg_b), 16)]
    ctext_blk = IV
    for ptext_blk in msg_chunks:
        if len(ptext_blk) !=16:
            PKCSpad(ptext_blk, 16)

        ctext_blk = cipher.encrypt(bxor(ctext_blk, ctext_blk))
        msg_decrypt.append(ctext_blk)
    return msg_decrypt

def CBC_encrypt(key_b, IV, msg_b):
    """ 16 byte key, and IV """
    msg_encrypt = []
    #cipher = AES.new(key_b, AES.MODE_ECB)
    #print(cipher)
    msg_chunks = [msg_b[i:i+16] for i in range(0, len(msg_b), 16)]
    #print([len(x) for x in msg_chunks])
    ctext_blk = IV
    for ptext_blk in msg_chunks:
        if len(ptext_blk) % 16 != 0:
            ptext_blk = PKCSpad(ptext_blk, 16)
        #print(len(ptext_blk), len(ctext_blk))
        ctext_blk = AES_encrypt(key_b, bxor(ptext_blk, ctext_blk))
        msg_encrypt.append(ctext_blk)
    return b''.join(msg_encrypt)

def CBC_decrypt(key_b, IV, msg_b):
    """ 16 byte key, and IV """
    msg_decrypt = []
    #cipher = AES.new(key_b, AES.MODE_ECB)
    #print(cipher)
    msg_chunks = [msg_b[i:i+16] for i in range(0, len(msg_b), 16)]
    ctext_blk0 = IV
    for ctext_blk1 in msg_chunks:
        if len(ctext_blk1) !=16:
            ctext_blk1 = PKCSpad(ctext_blk1, 16)
        ptext_blk = bxor( AES_decrypt(key_b, ctext_blk1), ctext_blk0 )
        ctext_blk0 = ctext_blk1
        msg_decrypt.append(ptext_blk)
    return msg_decrypt

def CTR_encrypt(key_b, msg_b, nonce = bytes(8)):
    blocksize=16
    blocks = math.ceil(len(msg_b)/blocksize)
    bytestream = b''
    for k in range(blocks):
        ctr = nonce + k.to_bytes(8, byteorder='little')
        bytestream += AES_encrypt(key_b, ctr)
    cipher = bxor(msg_b, bytestream[:len(msg_b)])
    return cipher

def rand_bytes(num):
    """ Returns $(num) random bytes, read from /dev/urandom. Not cryptographically secure."""
    buf = open("/dev/urandom", "rb").read(num)
    return buf

def ECB_CBC_oracle( bbox_fn ):
    """
    Oracle to detect whether a given ciphertext was encrypted using AES in CBC or ECB mode
    The idea here is to pass messages with a large number of repeating blocks, and look for repeats.
    """
    # Construct adverserial message
    blocksize=16
    adv_msg = b"\x00"*(3*blocksize)
    cipher = bbox_fn(adv_msg)

    for k in range(blocksize):
        cyclic_perm = cipher[k:] + cipher[:k]
        repeats, _ = count_reps(cyclic_perm, blocksize)
        if repeats > 0:
            bbox_fn.pred="ECB"
            return f"{repeats} repeats in ciphertext. ECB mode probable."

    
    bbox_fn.pred="CBC"
    return "CBC mode probable."

def untemper(z, mt):
    """
    Inverse of the temper function in the Mersenne Twister algorithm. Takes an MT PRNG object.
    Essentially reverses the (effective) Fiestel ciphers. Decode a block at a time
    """

    blocks_l = mt.w//mt.l
    blocks_t = mt.w//mt.t
    blocks_s = mt.w//mt.s
    blocks_u = mt.w//mt.u
    
    for k in range(blocks_l):
        bm = ((1 << mt.w) - 1) ^ ((1 << (mt.w-mt.l)) - 1) 
        bm = bm >> k*mt.l
        z = z ^ (  (z&bm) >> mt.l )
    for k in range(blocks_t):
        bm = ((1 << mt.t) - 1) << k*mt.t
        z = z ^ ( ( (z&bm) << mt.t) & mt.c)
    for k in range(blocks_s):
        bm = ((1 << mt.s) - 1) << k*mt.s
        z = z ^ ( ( (z&bm) << mt.s) & mt.b)
    for k in range(blocks_u):
        bm = ((1 << mt.w) - 1) ^ ((1 << (mt.w-mt.u)) - 1) 
        bm = bm >> k*mt.u
        z = z ^ ( ((z&bm) >> mt.u) & mt.d)
    return z

def MT_streamcipher(seed, msg_b):
    """Create a XOR cipher derived from 32-bit MT PRNG keystream"""
    ## Initialise PRNG
    mt = MT19937_32(seed)
    bytelength = len(msg_b)
    no_calls = bytelength//4 + 1
    ks = b''
    for i in range(no_calls):
        ks += mt().to_bytes(4, byteorder='little')
    ks = ks[:bytelength]
    return bxor(msg_b, ks)

def prefix_mac(key_b, msg_b):
    return sha1(key_b+msg_b)


def hmac_sha1(key_b, msg_b, blocksize=64):
    if len(key_b) > blocksize:
        key = codecs.decode(sha1(key_b), 'hex')
    elif len(key_b) < blocksize:
        key_b += bytes( (-len(key_b)) % blocksize)
    
    o_key_pad = bxor(key_b, bytes([0x5c])*blocksize) 
    i_key_pad = bxor(key_b, bytes([0x36])*blocksize) 
    return sha1(o_key_pad + codecs.decode(sha1(i_key_pad+msg_b), 'hex'))

if __name__ == "__main__":
    pass
