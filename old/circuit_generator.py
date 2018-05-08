# <<<<<<< HEAD:circuit_generator.py
# '''
# 4/24/2018 - Anastasiia Timashova github.com/timashana

# TEST FILE FOR CREATIN A MEAN BLOCK HASH CIRCUIT IN LIBSCAPI FORMAT

# '''

# from circuit_utility_functions import *
# import numpy as np
# from random import choice

# def writeCircuitFile(num_of_gates, party, p1_wires, gateList, output):
# ''' Write and store the circuit file '''
#     with open('MPPH.txt','w') as f:
#         s = str(num_of_gates) + '\n' + str(party) + '\n'
#         s += '1 ' + str(p1_wires) + '\n\n'
#         f.write(s)
#         for i in range(2,2050):
#             f.write(str(i))
#             f.write('\n')

#         f.write('\n2 2\n\n')
#         f.write('0\n1\n\n')

#         s = str(len(output)) + '\n\n'
#         f.write(s)
#         for o in output:
#             f.write(str(o))
#             f.write('\n')

#         f.write('\n\n')
#         for g in gateList:
#             f.write(g)
#             f.write('\n')

#         f.close()

# def writeInputFile():
# ''' Write and store the Party One and Party Two input files '''
#     with open('MPPHPartyOneInputs.txt', 'w') as f:
#         f.write('2048\n')
#         # One can change the input value by changing b in the following two for-loop
#         for i in range(1024):
#             b = 1
#             s = str(b) + '\n'
#             f.write(s)
#         for i in range(1024):
#             #b = randint(0,1)
#             b = 0
#             s = str(b) + '\n'
#             f.write(s)
#         f.close()
#     with open('MPPHPartyTwoInputs.txt', 'w') as t:
#         t.write('2\n')
#         for i in range(0,2):
#             s = str(i) + '\n'
#             t.write(s)
#         t.close()

# l=[]    #list to store the libscapi-formatted gates
# zero=0  # 0-wire
# one=1   # 1-wire
# curr_wire = 1   # keep track of the last used label
# gates = 0   # keep track of the number of gates in the circuit

# # test run on random 256px pic with 8b greyscale for ea pixel:

# # read the string
# bits = [k for k in range(2, 2050)]
# curr_wire = 2050
# input_arr = np.array(bits)
# # divide into 16 blocks of 16 pixels (with 8b greyscale)
# shape = (16, 16, 8)
# tmp = input_arr.reshape(shape)
# # go from numpy matrix to nested lists
# A = tmp.tolist()

# # create M - list of means for each block (M[0]-M[16]) and the mean of the means(M[15])
# M, curr_wire, gates = ALLMEANS(A, zero, curr_wire, gates, l)

# # compare each block mean to the main mean and compute the hash
# result, curr_wire, gates = BLKHASH(M, one, curr_wire, gates, l)

# print('Input wire labels:')
# #Uncomment to print the input wire labels
# '''
# print(0)
# print(1)
# for x in bits:
#     print(x)
# '''
# print('Gates:')
# for x in l:
#     print(x)

# print("The circuit has %d gates, the 16 output wires are"%(gates), result)
# writeCircuitFile(gates, 2, 2048, l, result)
# writeInputFile()
# =======
'''
4/24/2018 - Anastasiia Timashova github.com/timashana

TEST FILE FOR CREATIN A MEAN BLOCK HASH CIRCUIT IN LIBSCAPI FORMAT

'''

from circuit_utility_functions import *
import numpy as np
from random import choice

def writeCircuitFile(num_of_gates, party, p1_wires, gateList, output):
    # Write and store the circuit file
    with open('MPPH.txt','w') as f:
        s = str(num_of_gates) + '\n' + str(party) + '\n'
        s += '1 ' + str(p1_wires) + '\n\n'
        f.write(s)
        for i in range(2,2050):
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
    # Write and store the Party One and Party Two input files
    with open('MPPHPartyOneInputs.txt', 'w') as f:
        f.write('2048\n')
        # One can change the input value by changing b in the following two for-loop
        for i in range(1024):
            b = 1
            s = str(b) + '\n'
            f.write(s)
        for i in range(1024):
            #b = randint(0,1)
            b = 0
            s = str(b) + '\n'
            f.write(s)
        f.close()
    with open('MPPHPartyTwoInputs.txt', 'w') as t:
        t.write('2\n')
        for i in range(0,2):
            s = str(i) + '\n'
            t.write(s)
        t.close()

l=[]    #list to store the libscapi-formatted gates
zero=0  # 0-wire
one=1   # 1-wire
curr_wire = 1   # keep track of the last used label
gates = 0   # keep track of the number of gates in the circuit

# test run on random 256px pic with 8b greyscale for ea pixel:

# read the string
bits = [k for k in range(2, 2050)]
curr_wire = 2050
input_arr = np.array(bits)
# divide into 16 blocks of 16 pixels (with 8b greyscale)
shape = (16, 16, 8)
tmp = input_arr.reshape(shape)
# go from numpy matrix to nested lists
A = tmp.tolist()

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
for x in l:
    print(x)

print("The circuit has %d gates, the 16 output wires are"%(gates), result)
writeCircuitFile(gates, 2, 2048, l, result)
writeInputFile()
