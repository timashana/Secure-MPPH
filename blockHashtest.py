'''
4/24/2018 - Anastasiia Timashova github.com/timashana

TEST FILE FOR CREATIN A MEAN BLOCK HASH CIRCUIT IN LIBSCAPI FORMAT

'''

import meanBlockHash
import numpy as np
from random import choice

l=[]    #list to store the libscapi-formatted gates
zero=0  # 0-wire
one=1   # 1-wire
curr_wire = 1   # keep track of the last used label
gates = 0   # keep track of the number of gates in the circuit

# test run on random 256px pic with 8b greyscale for ea pixel:

# read the string
bits = [k for k in range(2, 2050)]
input_arr = np.array(bits)
# divide into 16 blocks of 16 pixels (with 8b greyscale)
shape = (16, 16, 8)
tmp = input_arr.reshape(shape)
# go from numpy matrix to nested lists
A = tmp.tolist()

# create M - list of means for each block (M[0]-M[16]) and the mean of the means(M[15])
M, curr_wire, gates = meanBlockHash.ALLMEANS(A, zero, curr_wire, gates, l)

# compare each block mean to the main mean and compute the hash
result, curr_wire, gates = meanBlockHash.BLKHASH(M, one, curr_wire, gates, l)

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
