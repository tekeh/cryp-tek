from cryptek import *

# python ex1p7.py ch7.txt "YELLOW SUBMARINE"
 
def main():
    ## Arg parser
    parser = argparse.ArgumentParser(description='Implements repeating-key XOR')
    parser.add_argument('fname', metavar='txt_file', type=str,
                       help='file to decrypt')
    parser.add_argument('key', metavar='txt_key', type=str,
                       help='key to decrypt file')
    args = parser.parse_args()

    fname   = args.fname
    key     = args.key

    with open(fname,'rb') as f:
        msg_b     = f.read()
        msg_bin     = base64.b64decode(msg_b) ## decode contents of b64

    # Decode
    msg_txt = AES_decrypt(key.encode(), msg_bin)
    print(msg_txt)

if __name__ == "__main__":
    main()

