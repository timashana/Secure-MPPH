'''This is is tester program to evaluate comparator part of the circuit by creating the libscapi format circuit for comparing two 8-bit values A and B and outputting 1 bit, s.t.
    1 means A>=B and 0 means A < B'''

from big_hash_circuit_functions import *
from copy import deepcopy

A = [0, 0, 1, 0, 0, 1, 0, 1]

block = []

curr_wire = 1

for i in range(256):
    block.append(A)

block_labels = []
for i in range(256):
    block_labels.append([])
    for j in range(8):
        block_labels[i].append(i*8+j+2)
        curr_wire += 1

def writeCircuitFile(num_of_gates, gateList, output):
    with open('MPPH.txt','w') as f:
        s1 = str(num_of_gates) + '\n' + str(2) + '\n'
        s1 += '1 ' + str(2) + '\n\n'
        f.write(s1)
        # party one provides the 0 and 1 wires
        for i in range(0, 2):
            f.write(str(i))
            f.write('\n')

        # party 2 provides the actual input (2d array of block pixel values
        s2 = '2 ' + '2048' + '\n\n'
        f.write(s2)
        for i in range(2, 2050):
            f.write(str(i))
            f.write('\n')

        s = '8\n\n'
        f.write(s)
        for i in output:
            f.write(str(i))
            f.write('\n')

        f.write('\n\n')
        for g in gateList:
            f.write(g)
            f.write('\n')

        f.close()

def writePartyOneInputFile():
    with open('MPPHPartyOneInputs.txt', 'w') as t:
        s = str(2)+'\n'
        t.write(s)
        for i in range(2):
            s = str(i) + '\n'
            t.write(s)
        t.close()

def writePartyTwoInputFile(B):
    with open('MPPHPartyTwoInputs.txt', 'w') as t:
        s = str(2048)+'\n'
        t.write(s)
        for i in B:
            for j in i:
                t.write(str(j))
                t.write('\n')
        t.close()

l=[]    #list to store the libscapi-formatted gates
zero=0  # 0-wire
one=1   # 1-wire
gates = 0   # keep track of the number of gates in the circuit

result, curr_wire, gates = BLKMEAN(block_labels, zero, curr_wire, gates, l)

writeCircuitFile(gates, l, result)
writePartyOneInputFile()
writePartyTwoInputFile(block_labels)
