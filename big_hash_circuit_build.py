'''
4/24/2018 - Anastasiia Timashova github.com/timashana

TEST FILE FOR CREATING A MEAN BLOCK HASH CIRCUIT IN LIBSCAPI FORMAT

'''

# HASH fFOR THE 256x256 IMAGE:

# Test result:
# 0010111111111100001111111111110000111111111111100011111111101111001011100111111100111111111111110011100111110111001100001111001100010000111100110001101101100111000111100000010100011100000001110001100000000111000110000000111100011000000000111111000000000000

#Circuit results:

# direct hash
# 0000011111100000001000010000110000011111111100000011111111101100001001000110111000111111000111110011000110000111000100010000001100000000000000110000000000000001000100000000000100010000000000000001000000000000000100000000000000010000000000000111000000000000

# revesed bits hash
# 0110101110101011001001010100000000001011000111000000000000000101010100111000010000001101110111000011000010010000010110000000000100000110110000100101000010110100100110101000000011001000101000100000000010000010001010000000000000001001100000001000001000011010
 
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
    # with open('MPPHPartyOneInputs.txt', 'w') as f:
    #     f.write('2048\n')
    #     for i in range(1024):
    #         b = 1
    #         s = str(b) + '\n'
    #         f.write(s)
    #     for i in range(1024):
    #         #b = randint(0,1)
    #         b = 0
    #         s = str(b) + '\n'
    #         f.write(s)
    #     f.close()
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

# test run on random 256px pic with 8b greyscale for ea pixel:

# read the string
bits = [k for k in range(2, 524290)]
#bits = [k for k in range(2, 2049)]
input_arr = np.array(bits)
# divide into 16 blocks of 16 pixels (with 8b greyscale)
shape = (256, 256, 8)
tmp = input_arr.reshape(shape)
# go from numpy matrix to nested lists
A = tmp.tolist()
'''
for i in range(len(A)):
    for j in range(len(A[0])):
        A[i][j].reverse()
'''
curr_wire = 524290

# create M - list of means for each block (M[0]-M[16]) and the mean of the means(M[15])
M, curr_wire, gates = ALLMEANS(A, zero, curr_wire, gates, l)

# compare each block mean to the main mean and compute the hash
result, curr_wire, gates = BLKHASH(M, one, curr_wire, gates, l)

print('Input wire labels:')
#Uncomment to print the input wire labels
'''
print(0)
print(1)
for x in bits:
    print(x)
'''
print('Gates:')
#for x in l:
#    print(x)
writeCircuitFile(gates, 2, 524288, l, result)
writeInputFile()

print("The circuit has %d gates, the %d output wires are"%(gates, len(result)), result)
