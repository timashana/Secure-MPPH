from random import choice
import numpy as np

def AND(a, b, c):
    return(['2', '1', a, b, c, '0001'])

def XOR(a, b, c):
    return(['2', '1', a, b, c, '0110'])

def NOT(a, b):
    return(['1', '1', a, b, '10'])

def ADD(l_a, l_b, l_cin, l):
    ladd=[XOR(l_a, l_b, l_cin+1), AND(l_a, l_b, l_cin+2), XOR(l_cin, l_cin+1, l_cin+3), AND(l_cin, l_cin+1, l_cin+4), XOR(l_cin+2, l_cin+4, l_cin+5), AND(l_cin+2, l_cin+4, l_cin+6), XOR(l_cin+5, l_cin+6, l_cin+7)]
    l+=ladd
    return l_cin+3, l_cin+7

def SUBCARRY(l_a, l_b, curr_wire, cin, l):
    lsub=[XOR(l_b, cin, curr_wire + 1), XOR(curr_wire + 1, l_a, curr_wire + 2), AND(curr_wire + 1, l_a, curr_wire + 3), AND(curr_wire + 2, curr_wire, curr_wire + 4), XOR(curr_wire + 3, curr_wire + 4, curr_wire + 5), AND(curr_wire + 3, curr_wire + 4, curr_wire + 6), XOR(curr_wire + 5, curr_wire + 6, curr_wire + 7)]
    l+=lsub
    return curr_wire + 7

def BINADDER(A, B, curr_wire, gates, l):
    A.append(zero)
    B.append(zero)
    size=len(A)
    lhalfadd=[XOR(A[0], B[0], curr_wire + 1), AND(A[0], B[0], curr_wire + 2)]
    l+=lhalfadd
    sum = [curr_wire + 1]
    curr_wire+=2
    for i in range(1, size):
        currsum, curr_wire=ADD(A[i], B[i], curr_wire, l)
        gates+=7
        sum.append(currsum)
    return sum, curr_wire, gates

def BLKMEAN(A, curr_wire, gates, l):
    '''A is an array of 16 arrays(12b(8bEXT) numbers)'''
    for lvl in range(1, 5):
        sum = []
        for i in range(0, len(A), 2):
            currsum, curr_wire, gates = BINADDER(A[i], A[i + 1], curr_wire, gates, l)
            sum.append(currsum)
        A = sum
    return A[0], curr_wire, gates

def ALLMEANS(A, curr_wire, gates, l):
    '''A is an array of 16 blocks (Array A descried in BLKMEAN)'''
    means = []
    for i in A:
        currmean, curr_wire, gates = BLKMEAN(i, curr_wire, gates, l)
        means.append(currmean)
    prime_mean, curr_wire, gates = BLKMEAN(means, curr_wire, gates, l)
    means.append(prime_mean)
    return means, curr_wire, gates

def COMPARATOR(A, B, curr_wire, gates, l):
    for i in range(8):
        curr_wire=SUBCARRY(A[i], B[i], curr_wire, one, l)
        gates+=7
    return curr_wire, gates

def BLKHASH(M, curr_wire, gates, l):
    size = len(M)
    hash=[]
    for i in range(size-1):
        curr_wire, gates = COMPARATOR(M[i], M[size-1], curr_wire, gates, l)
        hash.append(curr_wire)
    return hash, curr_wire, gates

l=[]    #list to store the libscapi-formatted gates
zero=0  # 0-wire
one=1   # 1-wire
curr_wire = 1   # keep track of the last used label
gates = 0   # keep track of the number of gates in the circuit

# test run on random 256px pic with 8b greyscale for ea pixel:

# read the string
input = np.array([zero, one]+[choice([0, 1]) for k in range(2048)])
# divide into 16 blocks of 16 pixels (with 8b greyscale)
shape = (16, 16, 8)
tmp = input[2::].reshape(shape)
# go from numpy matrix to nested lists
A = tmp.tolist()

# create M - list of means for each block (M[0]-M[16]) and the mean of the means(M[15])
M, curr_wire, gates = ALLMEANS(A, curr_wire, gates, l)

# compare each block mean to the main mean and compute the hash
result, curr_wire, gates = BLKHASH(M, curr_wire, gates, l)

print('Gates:')
for x in range(len(l)):
    print(' '.join([str(i) for i in l[x]]))

print("The circuit has %d gates, the 16 output wires are"%(gates), result)
