'''
4/24/2018 Anastasiia Timashova github.com/timashana

FUNCTIONS MODULE CREATING LIBSCAPI-FORMAT CIRCUIT FILE FOR BLOCK MEAN VALUE YAO CIRCUIT

In below code:
curr_wire last used label in the circuit
gates current number of gates in the circuit
l a list of libscapi-format gate declarations for the circuit
one 1-wire label
zero 0-wire label

All lists representing binary numbers are enumerated from LSB to MSB.
That is, A = [A0, A1, ..., An] represents binary number An..A2A1A0
For example, 12345 -> [5, 4, 3, 2, 1]

Unless specified, all variables are not actual values, but labels to the corresponding wires
'''

from math import log
from copy import deepcopy

def AND(a, b, c):
    '''PRE: a, b input labels, c output label
        POST: libscapy-format string for AND gate with specified labels'''
    return('2 1 '+str(a)+' '+str(b)+' '+str(c)+' 0001')

def XOR(a, b, c):
    '''PRE: a, b input labels, c output label
            POST: libscapy-format string for XOR gate with specified labels'''
    return('2 1 '+str(a)+' '+str(b)+' '+str(c)+' 0110')

def NOT(a, b):
    '''PRE: a input label, b output label
            POST: libscapy-format string for NOT gate with specified labels'''
    return('1 1 '+str(a)+' '+str(b)+' 10')

def ADD(a, b, c_in, l):
    '''PRE: a, b labels for the two addends, c_in label for carry-in
        POST: l contains all gates for the binary full-adder, returned are labels for sum and carry-out'''
    ladd=[XOR(a, b, c_in + 1), AND(a, b, c_in + 2), XOR(c_in, c_in + 1, c_in + 3), AND(c_in, c_in + 1, c_in + 4), XOR(c_in + 2, c_in + 4, c_in + 5), AND(c_in + 2, c_in + 4, c_in + 6), XOR(c_in + 5, c_in + 6, c_in + 7)]
    l+=ladd
    sum, c_out = c_in + 3, c_in + 7
    return sum, c_out

def TWOCOMPARATOR(a, b, curr_wire, one, l):
    '''PRE: labels: a minuend, b subtrahend,  one 1-wire
        POST: l contains all gates for the 2-bit comparator, returned is the label for result (w/values: 1 => A>=B, 0 => A<B)'''
    lsub=[XOR(b, one, curr_wire + 1), XOR(curr_wire + 1, a, curr_wire + 2), AND(curr_wire + 1, a, curr_wire + 3), AND(curr_wire + 2, curr_wire, curr_wire + 4), XOR(curr_wire + 3, curr_wire + 4, curr_wire + 5), AND(curr_wire + 3, curr_wire + 4, curr_wire + 6), XOR(curr_wire + 5, curr_wire + 6, curr_wire + 7)]
    l+=lsub
    l_cout = curr_wire+7
    return l_cout

def COMPARATOR(A, B, one, curr_wire, gates, l):
    '''PRE: A, B n-bit binary lists (|A|=|B|)
        POST: l contains all gates for the n-bit comparator, returned are result wire label (w/values: 1 => A>=B, 0 => A<B) and updated gates number'''

    # OR curr_wire and one to make curr_wire carry value of 1
    l_curr_wire_to_one = [XOR(one, curr_wire, curr_wire+1), AND(one, curr_wire, curr_wire+2), XOR(curr_wire+1, curr_wire+2, curr_wire+3)]
    l+=l_curr_wire_to_one
    curr_wire+=3
    gates+=3

    for i in range(8):
        curr_wire=TWOCOMPARATOR(A[i], B[i], curr_wire, one, l)
        gates+=7
    return curr_wire, gates

def BINADDER(A, B, zero, curr_wire, gates, l):
    '''PRE: A, B two n-bit binary lists
        POST: l contains all gates for the n-bit ripple-carry adder, returned are sum wire label, updated curr_wire and gates'''

    # the following copies are needed to prevent the original lists from being modified
    A_copy = deepcopy(A)
    B_copy = deepcopy(B)
    # extend A, B by 0-valued bit on the left to account for overflow in the sum
    A_copy.append(zero)
    B_copy.append(zero)
    size=len(A_copy)
    # use half-adder for the LSB's (no carry-in for LSB)
    lhalfadd=[XOR(A_copy[0], B_copy[0], curr_wire + 1), AND(A_copy[0], B_copy[0], curr_wire + 2)]
    l+=lhalfadd
    sum = [curr_wire + 1]
    curr_wire+=2
    gates+=2
    # use chained full-adders for the other bits
    for i in range(1, size):
        curr_sum, curr_wire=ADD(A_copy[i], B_copy[i], curr_wire, l)
        gates+=7
        sum.append(curr_sum)
    return sum, curr_wire, gates

def BLKMEAN(A, zero, one, curr_wire, gates, l):
    '''PRE: A a (2D)list of a block's pixels' grayscale lists ( n 8-bit binary numbers of block pixels)
        POST: l contains all the gates for finding the mean of the n numbers, returned are the 8b mean and updated curr-wire, gates'''
    #the following copy is needed to prevent the original list from being modified
    A_copy = deepcopy(A)
    lvls = int(log(len(A_copy), 2))
    # use cascading approach to find the sum of all n numbers by adding two at a time => log(n) "levels":
    for lvl in range(1, lvls+1):
        # on each level, calculate sum = list of pairwise sums
        sum = []
        for i in range(0, len(A_copy), 2):
            currsum = 0
            currsum, curr_wire, gates = BINADDER(A_copy[i], A_copy[i + 1], one, curr_wire, gates, l)
            sum.append(deepcopy(currsum))
        # set A = sum since it contains the addends for the next "level"
        A_copy = deepcopy(sum)
    # A is now a list containing a single list(the (n+log(n))-bit sum), chop off log(n) LSB's to find mean (divide by n)
    return A_copy[0][lvls::], curr_wire, gates

def ALLMEANS(A, zero, one, curr_wire, gates, l):
    '''PRE: A a (3D)list of blocks (block is a list A descried in BLKMEAN)
        POST: l contains all the gates for finding all blocks' means and the mean of the means, ..
            ..returned are the list containing the block means and the main mean as its last element, ..
            ..updated curr_wire and gates'''
    means = []
    # for each block, calculate the mean and add it to the list

    for i in A:
        currmean, curr_wire, gates = BLKMEAN(i, zero, one,curr_wire, gates, l)
        means.append(currmean)
    # calculate the mean of the means and add it to the same list
    prime_mean, curr_wire, gates = BLKMEAN(means, zero, one, curr_wire, gates, l)
    means.append(prime_mean)
    return means, curr_wire, gates

def BLKHASH(M, one, curr_wire, gates, l):
    '''PRE: M list of n+1 means: M[0]..M[n] blk means, M[n+1] - main mean
        POST: l contains all gates for finding the (n)-bit hash, returned are the list of hash labels, updated curr_wire and gates '''
    size = len(M)-1
    hash=[]
    # for the block means, compare them to the main one and return the result (0 if less, 1 if gte), add the result to hash
    for i in range(size):
        curr_wire, gates = COMPARATOR(M[i], M[size], one, curr_wire, gates, l)
        hash.append(curr_wire)
    return hash, curr_wire, gates
