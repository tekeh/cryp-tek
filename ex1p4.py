from cryptek import *

# python ex1p4.py ch4.txt

def main():
    ## Arg parser
    parser = argparse.ArgumentParser(description='Does a single char XOR search on each line of an file, returning the one most likely to be English plaintext')
    parser.add_argument('fname', metavar='hex', type=str,
                       help='file containing hex code on each line')
    args = parser.parse_args()

    ## Run
    file_name = args.fname
    winner = ''
    winner_score = 1
    with open(file_name, 'r') as f:
        for k, line in enumerate(f):
            line = line.replace('\n','')
            buf0 = codecs.decode(line, 'hex')
            for c in [n for n in range(256)]:
                buf1 = [c]*len(buf0)
                xor = bxor(buf0, buf1)
                try:
                    d_line = xor.decode()
                    score = plaintext_score(d_line)
                    if score < winner_score:
                        winner = d_line
                        winner_score = score
                except UnicodeDecodeError as e:
                    pass

    return winner, winner_score

if __name__ == "__main__":
    w, w_sco = main()
    print(f"{w} \t {w_sco}")
