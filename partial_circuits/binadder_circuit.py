'''
Anastasiia Timashova github.com/timashana

This is a tester program to evaluate BINADDER part of the circuit by creating
    the libscapi format circuit for adding two arbitrary long values A and B
    where |A|=|B|=n - arbitraty.
'''

from hash_circuit_functions import *

def writeCircuitFile(num_of_gates, parties, p1_wires, p2_wires, gateList, output):
    with open('MPPH.txt','w') as f:
        s1 = str(num_of_gates) + '\n' + str(parties) + '\n'
        s1 += '1 ' + str(2 + p1_wires) + '\n\n'
        f.write(s1)
        # Party one provides the 0 and 1 wire before providing it's 8-bit number
        for i in range(0, p1_wires + 2):
            f.write(str(i))
            f.write('\n')

        s2 = '2 ' + str(p2_wires) + '\n\n'
        f.write(s2)
        for i in range(p1_wires + 2, p1_wires + p2_wires + 2):
            f.write(str(i))
            f.write('\n')

        s = '\n'+ str(len(output))+'\n\n'
        f.write(s)
        for i in output:
            f.write(str(i))
            f.write('\n')

        f.write('\n\n')
        for g in gateList:
            f.write(g)
            f.write('\n')

        f.close()

def writePartyOneInputFile(A):
    with open('MPPHPartyOneInputs.txt', 'w') as t:
        s = str(len(A)+2)+'\n'
        t.write(s)
        for i in range(0,2):
            s = str(i) + '\n'
            t.write(s)
        for i in A:
            s = str(i) + '\n'
            t.write(s)
        t.close()

def writePartyTwoInputFile(B):
    with open('MPPHPartyTwoInputs.txt', 'w') as t:
        s = str(len(B))+'\n'
        t.write(s)
        for i in B:
            s = str(i) + '\n'
            t.write(s)
        t.close()

l=[]    #list to store the libscapi-formatted gates
zero=0  # 0-wire
one=1   # 1-wire
gates = 0   # keep track of the number of gates in the circuit
curr_wire = 2   # keep track of the last used label

'''all numbers are represented in [LSB...MSB] format
        for example, 123 -> [3, 2, 1]'''
A = [1, 1, 1, 1, 1, 1, 1, 1, 1]
B = [0, 0, 0, 0, 0, 0, 0, 0, 1]

A_labels = [i for i in range(curr_wire, curr_wire + len(A))]
curr_wire += len(A)
B_labels = [i for i in range(curr_wire, curr_wire + len(B))]
curr_wire += len(B)


result, curr_wire, gates = BINADDER(A_labels, B_labels, one, curr_wire, gates, l)
# Uncomment below to return the mean of the 2 numbers
# result = result[1::]

writeCircuitFile(gates, 2, len(A), len(B), l, result)
writePartyOneInputFile(A)
writePartyTwoInputFile(B)
