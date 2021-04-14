from cryptek import *
from math import ceil, log2
import random

def modexp(base, exponent, modulus):
    bitlength = ceil(log2(exponent))
    result = 1
    z = base % modulus
    for k in range(bitlength):
        if (exponent >> k) % 2:
            result = (result * z ) % modulus
        z = (z*z) % modulus
    return result

def diffie_hellman(g, p):
    ## Generate a and A
    a = random.randint(0, p-1)
    A = modexp(g, a, p)

    ## Generate b and B
    b = random.randint(0, p-1)
    B = modexp(g, b, p)

    ## Generate sesion key
    sb = modexp(B, a, p)
    sa = modexp(A, b, p)
    print(sa==sb)   ## should be true
    return (a, b, g, sa)
    
g_long = 2
p_long = int("ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff", 16)

if __name__ == "__main__":
    p = 37
    g = 5

    ## Test phase 1
    secret1 = diffie_hellman(g, p)

    ## Test phase 2
    secret2 = diffie_hellman(g_long, p_long)
    


