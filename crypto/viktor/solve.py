# Original code source - https://gist.github.com/LiveOverflow/104adacc8af7895a4c14cea4a5236ecc

## Basically you need to find 160 linearly independent vectors since XOR is addition in GF(2)
## and a SHA1 hash is 160 bits. Then do a Linalg solver and get the ones which are needed and QED.

## Ironically the numbers 0 -> 160 act as a very good set and I believe all but 1's hashes are lin ind
## So it ends up being like 50 or so numbers, line by line, then QED
from sage.all import *
import hashlib

# prepare a table of bits
def bits_of(x):
    bits = []
    for c in "{:08b}".format(x):
        bits += [int(c)]
    return bits

# list of 8bit arrays/vectors
# bits_table[ 0] = [0,0,0,0, 0,0,0,0]
# bits_table[ 3] = [0,0,0,0, 0,0,1,1]
# bits_table[86] = [0,1,0,1, 0,1,1,0]
bits_8_table = [bits_of(x) for x in range(256)] 

def mk_vector(line):
    bits_160 = []
    # sha256 of the filename+"\0"
    result = hashlib.sha1(line.encode())
    # for each byte of the hash we get each bit
    for byte in result.digest():
        # add the next 8 bits to the bits vector
        bits_160 += bits_8_table[int(byte)]
    # return the bit vector
    return bits_160

GF2 = Zmod(2)

vectors = []
lines = []
# loop over some numbers
for x in range(99999):
    # generate a 160bit vector from a possible filename
    line = f"{x}"
    new_160_vector = mk_vector(line)
    # create a matrix of all old vectors + the potential new one in GF(2)
    m = matrix(GF2, vectors + [new_160_vector]).transpose()
    # check the rank of this matrix
    rank = m.rank()
    # if rank increased, keep this file and vector because it's linear independent
    if rank > len(vectors):
        print(f"line {x} is linear independent")
        vectors += [new_160_vector]
        lines += [line]
    else:
        print(f"line {x} is NOT linear independent")
    if len(vectors)==160:
        break

GOAL = []
# the signed hash is the "point" that we want to get to in the vector space
for c in "\x66\x7a\x32\x13\x2b\xaf\x41\x1e\xbf\x34\xc8\x1a\x24\x2d\x9e\xf4\xbf\x72\xe2\x88":
    GOAL += bits_8_table[ord(c)]


# create the whole matrix in GF(2) with all 256 bit vectors
m = matrix(GF2, vectors).transpose()
solved_equation = m.solve_right(vector(GOAL))
print(solved_equation)
for x, s in zip(solved_equation, lines):
    #print x, s
    if x:
        print(s)
