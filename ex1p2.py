from cryptek import *

# python ex1p2.py 1c0111001f010100061a024b53535009181c 686974207468652062756c6c277320657965

if __name__ == "__main__":

    ## Arg parser
    parser = argparse.ArgumentParser(description='Converts given hex to base64')
    parser.add_argument('buffs', metavar='hex', type=str, nargs='+',
                       help='Hex encoded string')
    args = parser.parse_args()

    ## Run
    buf0 = codecs.decode(args.buffs[0], 'hex')
    buf1 = codecs.decode(args.buffs[1], 'hex')
    xor = bxor(buf0, buf1)
    
    print(codecs.encode(xor, 'hex'))
