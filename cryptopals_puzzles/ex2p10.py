from cryptek import *
import codecs

if __name__ == "__main__":
    IV = bytes([0]*16) ## initialization vector
    key_b = "YELLOW SUBMARINE".encode()
    with open('ch10.txt', 'rb') as f:
        msg_b = codecs.decode(f.read(), 'base64')
        
    a = CBC_decrypt(key_b, IV, msg_b)
    print(a)
