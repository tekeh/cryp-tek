from cryptek import *

#python ex1p1.py 49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d

if __name__ == "__main__":

    ## Arg parser
    parser = argparse.ArgumentParser(description='Converts given hex to base64')
    parser.add_argument('hex_strs', metavar='hex', type=str, nargs='+',
                       help='Hex encoded string')
    args = parser.parse_args()
    ## Run
    b64_strs = []
    for h in args.hex_strs:
        b64_strs.append(hex2b64(h))
    print(b64_strs)
