from cryptek import *
import codecs

if __name__ == "__main__":

    ## Teste
    str_0 = b"ICE ICE BABY\x04\x04\x04\x04"
    str_1 = b"ICE ICE BABY\x01\x02\x03\x04"

    out_0 = PKCS_validation(str_0)
    out_1 = PKCS_validation(str_1)
