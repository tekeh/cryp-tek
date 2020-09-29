from cryptek import *

# python ex1p5.py ch5.txt ICE

def main():
    ## Arg parser
    parser = argparse.ArgumentParser(description='Implements repeating-key XOR')
    parser.add_argument('fname', metavar='txt_file', type=str,
                       help='file to encrypt')
    parser.add_argument('key', metavar='txt_key', type=str,
                       help='file to encrypt')
    args = parser.parse_args()

    ## Run
    file_name   = args.fname
    key         = args.key
    with open(file_name, 'r') as f:
        line = f.read()[:-1] ## remove last newline/EOF char
        buf0 = codecs.encode(line)
        buf1 = codecs.encode(key) ## encode both into bytes
        encrypted_line = xor_encrypt(buf0, buf1)
        print(line, codecs.encode(encrypted_line, 'hex'))
    return encrypted_line

if __name__ == "__main__":
    main()
