'''

TEST FILE FOR CREATING A MEAN BLOCK HASH CIRCUIT IN LIBSCAPI FORMAT

'''

from hash_circuit_functions import *
import numpy as np
from random import choice

def writeCircuitFile(num_of_gates, party, p1_wires, gateList, output):
    with open('MPPH.txt','w') as f:
        s = str(num_of_gates) + '\n' + str(party) + '\n'
        s += '1 ' + str(p1_wires) + '\n\n'
        f.write(s)
        for i in range(2,524290):
            f.write(str(i))
            f.write('\n')

        f.write('\n2 2\n\n')
        f.write('0\n1\n\n')

        s = str(len(output)) + '\n\n'
        f.write(s)

        for o in output:
            f.write(str(o))
            f.write('\n')

        f.write('\n\n')
        for g in gateList:
            f.write(g)
            f.write('\n')

        f.close()

def writeInputFile():
    with open('MPPHPartyTwoInputs.txt', 'w') as t:
        t.write('2\n')
        for i in range(0,2):
            s = str(i) + '\n'
            t.write(s)
        t.close()

l=[]    #list to store the libscapi-formatted gates
result=[] #list to store output wires
zero=0  # 0-wire
one=1   # 1-wire
curr_wire = 1   # keep track of the last used label
gates = 0   # keep track of the number of gates in the circuit

# read the string
bits = [k for k in range(2, 524290)]
#bits = [k for k in range(2, 2049)]
input_arr = np.array(bits)
# divide into 16 blocks of 16 pixels (with 8b greyscale)
shape = (256, 256, 8)
tmp = input_arr.reshape(shape)

I = tmp.tolist()

''' reformat the bit by the order of blocks '''
temp = []
# row by row (vertical)
for r in range(0, 256, 16):
    # col by col (horizontal)
    for c in range(0, 256, 16):
        for i in range(r, r+16):
            for j in range(c, c+16):
                temp.append(I[i][j])

A = []
for i in range(0, len(temp), 256):
    block = []
    for j in range(i, i+256):
        block.append(temp[j])
    A.append(block)

curr_wire = 524290

# create M - list of means for each block (M[0]-M[16]) and the mean of the means(M[15])
M, curr_wire, gates = ALLMEANS(A, zero, one, curr_wire, gates, l)

# compare each block mean to the main mean and compute the hash
result, curr_wire, gates = BLKHASH(M, one, curr_wire, gates, l)

writeCircuitFile(gates, 2, 524288, l, result)
writeInputFile()
