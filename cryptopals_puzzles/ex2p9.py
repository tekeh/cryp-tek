from cryptek import *

# python ex2p9.py "YELLOW SUBMARINE"

if __name__ == "__main__":
    a = PKCSpad(b"YELLOW SUBMARINE", 20)
    print(a)
