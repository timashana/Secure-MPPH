'''
Anastasiia Timashova github.com/timashana

This is a tester program to evaluate the level-based binary addition logic
    by manually compute the means of 4 binary numbers using the levels method
    implemented in BLKMEAN function without calling it.
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

def writePartyOneInputFile(in1):
    with open('MPPHPartyOneInputs.txt', 'w') as t:
        s = str(len(in1)+2)+'\n'
        t.write(s)
        for i in range(0,2):
            s = str(i) + '\n'
            t.write(s)
        for i in in1:
            s = str(i) + '\n'
            t.write(s)
        t.close()

def writePartyTwoInputFile(in2):
    with open('MPPHPartyTwoInputs.txt', 'w') as t:
        s = str(len(in2))+'\n'
        t.write(s)
        for i in in2:
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
A = [1, 1, 1, 1, 1, 1, 1, 1]
B = [0, 0, 0, 0, 0, 0, 0, 0]
C = [1, 1, 1, 1, 1, 1, 1, 1]
D = [0, 0, 0, 0, 0, 0, 0, 0]

A_labels = [i for i in range(curr_wire, curr_wire + len(A))]
curr_wire += len(A)
B_labels = [i for i in range(curr_wire, curr_wire + len(B))]
curr_wire += len(B)
in1 = A[::] + B[::]
C_labels = [i for i in range((curr_wire), curr_wire + len(C))]
curr_wire += len(C)
D_labels = [i for i in range((curr_wire), curr_wire + len(D))]
curr_wire += len(D)
in2 = C[::] + D[::]

result1, curr_wire, gates = BINADDER(A_labels, B_labels, one, curr_wire, gates, l)
result2, curr_wire, gates = BINADDER(C_labels, D_labels, one, curr_wire, gates, l)
result3, curr_wire, gates = BINADDER(result1, result2, one, curr_wire, gates, l)
result3 = result3[2::]

writeCircuitFile(gates, 2, len(in1), len(in2), l, result3)
writePartyOneInputFile(in1)
writePartyTwoInputFile(in2)
