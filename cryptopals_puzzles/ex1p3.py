from cryptek import *

# python ex1p3.py 1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736

def main():
    ## Arg parser
    parser = argparse.ArgumentParser(description='Converts given hex to base64')
    parser.add_argument('buff', metavar='hex', type=str, nargs='+',
                       help='Hex encoded string')
    args = parser.parse_args()

    ## Run
    buf0 = codecs.decode(args.buff[0], 'hex')
    winner = ''
    c_winner = ''
    winner_score = 1
    for c in 'abcdefghijjklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
        buf1 = [ord(c)]*len(buf0)
        xor = bxor(buf0, buf1)
        score = plaintext_score(xor.decode())
        if score < winner_score:
            winner = xor.decode()
            winner_score = score
            c_winner = c
    return c, winner, winner_score

if __name__ == "__main__":
    print(main())
