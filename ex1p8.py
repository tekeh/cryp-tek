from cryptek import *

# python ex1p8.py ch8.txt

def main():
    ## Arg parser
    parser = argparse.ArgumentParser(description='Implements repeating-key XOR')
    parser.add_argument('fname', metavar='txt_file', type=str,
                       help='file to decrypt')
    args = parser.parse_args()

    fname       = args.fname
    block_size  = 16
    msg = []
    with open(fname,'r') as f:
        for line in f:
            msg.append( codecs.decode(line.strip(), 'hex' ))#.replace('\n',''))
            #print(len(line.strip()))
            #print(len(bytes.fromhex(line.strip())))
         #`print(msg)
        #msg_b = [codecs.decode(i, 'hex') for i in msg]
        #print(msg_b)
        #print(msg)
    for n, x in enumerate(msg):
        a = count_reps(x, block_size)[0] 
        if a !=0:
            print(f"Line {n} has {a} repeats")
    return 1

if __name__ == "__main__":
    main()

