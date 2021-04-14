from cryptek import *

#python ex1p6.py ch6.txt

def main():
    ## Arg parser
    parser = argparse.ArgumentParser(description='Implements repeating-key XOR')
    parser.add_argument('fname', metavar='txt_file', type=str,
                       help='file to encrypt')
    args = parser.parse_args()

    ## Run
    ## Find probable eysize
    k_best = 0
    best_norm_hd = 8 ## max ?
    KEYSIZE     = [i for i in range(2,40)]
    file_name   = args.fname

    with open(file_name, 'r') as f:
        msg_b64 = f.read().encode('ascii')
        msg     = base64.decodebytes(msg_b64)

    # Fine probable keysize
    for k in KEYSIZE:
        norm_hd=0
        num, num_blocks= 0, 5
        for i in range(num_blocks):
            for j in range(i, num_blocks):
                norm_hd += hamming_dist(msg[i*k:(i+1)*k], msg[j*k:(j+1)**k])/k
                num +=1
        if norm_hd/num < best_norm_hd:
            k_best = k
            best_norm_hd = norm_hd/num

    keysize = k_best
    print(f"Most probable KEYSIZE is {keysize}")

    # Transpose into blocks of KEYSIZE length
    msg_blocks = [msg[keysize*i:keysize*(i+1)] for i in range(len(msg)//keysize)]

    ## carry out single char XOR analysis
    KEY = []
    for i in range(keysize):
        ith_letters = bytes([x[i] for x in msg_blocks])
        winner = ''
        winner_score = 1
        for m in range(256):
            c = chr(m)
            buf1 = [ord(c)]*len(ith_letters)
            try:
                xor = bxor(ith_letters, buf1)
                score = plaintext_score(xor.decode())
                if score < winner_score:
                    winner = c
                    winner_score = score
            except UnicodeDecodeError as e:
                pass

        KEY.append(winner)
    print(f"Using this, key is probably, {''.join(KEY)}")
    decrypt_msg = xor_encrypt(msg, codecs.encode(''.join(KEY)))
    print(decrypt_msg.decode())


if __name__ == "__main__":
    main()
