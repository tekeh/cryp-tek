from cryptek import *
import base64
import codecs

def edit(ciphertxt, key_b, offset, newmsg):
    msg_b = bytearray(CTR_encrypt(key_b, ciphertxt))
    if offset+len(newmsg) > len(ciphertxt):
        print("Injected message too long")
        return 0
    else:
        msg_b[offset:offset+len(newmsg)] = newmsg
        return CTR_encrypt(key_b, msg_b)

if __name__=="__main__":
    # Encrypt under random key
    key_b = rand_bytes(16)
    msg_b = open("ch7.txt", "rb").read() 
    msg_b = base64.b64decode(msg_b)
    msg_txt = AES_decrypt(b"YELLOW SUBMARINE", msg_b)

    ct = CTR_encrypt(key_b, msg_txt)
    ks = edit(ct, key_b, 0, bytes(len(ct)))

    original_txt = bxor(ks, ct)
