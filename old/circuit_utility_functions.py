<<<<<<< HEAD
# <<<<<<< HEAD:circuit_utility_functions.py
# '''
# 4/24/2018 - Anastasiia Timashova github.com/timashana

# FUNCTIONS MODULE CREATING LIBSCAPI-FORMAT CIRCUIT FILE FOR BLOCK MEAN VALUE YAO CIRCUIT

# In below code:
# curr_wire - last used label in the circuit
# gates - current number of gates in the circuit
# l - a list of libscapi-format gate declarations for the circuit
# one - 1-wire label
# zero - 0-wire label

# All lists representing binary numbers are enumerated from LSB to MSB.
# That is, A = [A0, A1, ..., An] represents binary number An..A2A1A0

# Unless specified, all variables are not actual values, but labels to the corresponding wires
# '''

# def AND(a, b, c):
#     '''PRE: a, b - input labels, c - output label
#         POST: libscapy-format string for AND gate with specified labels'''
#     return('2 1 '+str(a)+' '+str(b)+' '+str(c)+' 0001')

# def XOR(a, b, c):
#     '''PRE: a, b - input labels, c - output label
#             POST: libscapy-format string for XOR gate with specified labels'''
#     return('2 1 '+str(a)+' '+str(b)+' '+str(c)+' 0110')

# def NOT(a, b):
#     '''PRE: a - input label, b - output label
#             POST: libscapy-format string for NOT gate with specified labels'''
#     return('1 1 '+str(a)+' '+str(b)+' 10')

# def ADD(a, b, c_in, l):
#     '''PRE: a, b - labels for the two addends, c_in - label for carry-in
#         POST: l contains all gates for the binary full-adder, returned are labels for sum and carry-out'''
#     ladd=[XOR(a, b, c_in + 1), AND(a, b, c_in + 2), XOR(c_in, c_in + 1, c_in + 3), AND(c_in, c_in + 1, c_in + 4), XOR(c_in + 2, c_in + 4, c_in + 5), AND(c_in + 2, c_in + 4, c_in + 6), XOR(c_in + 5, c_in + 6, c_in + 7)]
#     l+=ladd
#     sum, c_out = c_in + 3, c_in + 7
#     return sum, c_out

# def TWOCOMPARATOR(a, b, curr_wire, one, l):
#     '''PRE: labels: a - minuend, b - subtrahend,  one - 1-wire
#         POST: l contains all gates for the 2-bit comparator, returned is the label for result (w/values: 1 => A>=B, 0 => A<B)'''
#     lsub=[XOR(b, one, curr_wire + 1), XOR(curr_wire + 1, a, curr_wire + 2), AND(curr_wire + 1, a, curr_wire + 3), AND(curr_wire + 2, curr_wire, curr_wire + 4), XOR(curr_wire + 3, curr_wire + 4, curr_wire + 5), AND(curr_wire + 3, curr_wire + 4, curr_wire + 6), XOR(curr_wire + 5, curr_wire + 6, curr_wire + 7)]
#     l+=lsub
#     l_cout = curr_wire+7
#     return l_cout

# def COMPARATOR(A, B, one, curr_wire, gates, l):
#     '''PRE: A, B - 8-bit binary lists
#         POST: l contains all gates for the 8-bit comparator, returned are result wire label (w/values: 1 => A>=B, 0 => A<B) and updated gates number'''

#     # OR curr_wire and one to make curr_wire carry value of 1
#     l_curr_wire_to_one = [XOR(one, curr_wire, curr_wire+1), AND(one, curr_wire, curr_wire+2), XOR(curr_wire+1, curr_wire+2, curr_wire+3)]
#     l+=l_curr_wire_to_one
#     curr_wire+=3
#     gates+=3

#     for i in range(8):
#         curr_wire=TWOCOMPARATOR(A[i], B[i], curr_wire, one, l)
#         gates+=7
#     return curr_wire, gates

# def BINADDER(A, B, zero, curr_wire, gates, l):
#     '''PRE: A, B - two n-bit binary lists
#         POST: l contains all gates for the n-bit ripple-carry adder, returned are sum wire label, updated curr_wire and gates'''

#     # extend A, B by 0-valued bit on the left to account for overflow in the sum
#     A.append(zero)
#     B.append(zero)
#     size=len(A)
#     # use half-adder for the LSB's (no carry-in for LSB)
#     lhalfadd=[XOR(A[0], B[0], curr_wire + 1), AND(A[0], B[0], curr_wire + 2)]
#     l+=lhalfadd
#     sum = [curr_wire + 1]
#     curr_wire+=2
#     gates+=2
#     # use chained full-adders for the other bits
#     for i in range(1, size):
#         curr_sum, curr_wire=ADD(A[i], B[i], curr_wire, l)
#         gates+=7
#         sum.append(curr_sum)
#     return sum, curr_wire, gates

# def BLKMEAN(A, zero, curr_wire, gates, l):
#     '''PRE: A - a (2D)list of 16 lists(16 8-bit binary numbers - sums of block pixels)
#         POST: l contains all the gates for finding the sum of the 16 number, returned are the 8b mean and updated curr-wire, gates'''

#     # use cascading approach to find the sum of all 16 numbers by adding two at a time => 4 "levels":
#     for lvl in range(1, 5):
#         # on each level, calculate sum = list of pairwise sums
#         sum = []
#         for i in range(0, len(A), 2):
#             currsum, curr_wire, gates = BINADDER(A[i], A[i + 1], zero, curr_wire, gates, l)
#             sum.append(currsum)
#         # set A = sum since it contains the addends for the next "level"
#         A = sum
#     #A is now a list containing a single list(the 12-bit sum), chop off 4 LSB's to find mean (divide by 16)
#     return A[0][4::], curr_wire, gates

# def ALLMEANS(A, zero, curr_wire, gates, l):
#     '''PRE: A - a (3D)list of 16 blocks (block is a list A descried in BLKMEAN)
#         POST: l contains all the gates for finding all 16 blocks' means and the mean of the means, ..
#             ..returned are the list containing the 16 block means and the main mean, updated curr_wire and gates'''
#     means = []
#     # for each block, calculate the mean and add it to the list
#     for i in A:
#         currmean, curr_wire, gates = BLKMEAN(i, zero, curr_wire, gates, l)
#         means.append(currmean)
#     # calculate the mean of the means and add it to the same list
#     prime_mean, curr_wire, gates = BLKMEAN(means, zero, curr_wire, gates, l)
#     means.append(prime_mean)
#     return means, curr_wire, gates

# def BLKHASH(M, one, curr_wire, gates, l):
#     '''PRE: M - list of 17 means: M[0]..M[15] - blk means, M[15] - main mean
#         POST: l contains all gates for finding the 16-bit hash, returned are the list of hash labels, updated curr_wire and gates '''
#     size = len(M)
#     hash=[]
#     # for the block means, compare them to the main one and return the result (0 if less, 1 if gte), add the result to hash
#     for i in range(size-1):
#         curr_wire, gates = COMPARATOR(M[i], M[size-1], one, curr_wire, gates, l)
#         hash.append(curr_wire)
#     return hash, curr_wire, gates
# =======
=======
>>>>>>> dcf7f5733df26b0a567a793219831cf2f63d3a88
'''
4/24/2018 - Anastasiia Timashova github.com/timashana

FUNCTIONS MODULE CREATING LIBSCAPI-FORMAT CIRCUIT FILE FOR BLOCK MEAN VALUE YAO CIRCUIT

In below code:
curr_wire - last used label in the circuit
gates - current number of gates in the circuit
l - a list of libscapi-format gate declarations for the circuit
one - 1-wire label
zero - 0-wire label

All lists representing binary numbers are enumerated from LSB to MSB.
That is, A = [A0, A1, ..., An] represents binary number An..A2A1A0

Unless specified, all variables are not actual values, but labels to the corresponding wires
'''

from math import log

def AND(a, b, c):
    '''PRE: a, b - input labels, c - output label
        POST: libscapy-format string for AND gate with specified labels'''
    return('2 1 '+str(a)+' '+str(b)+' '+str(c)+' 0001')

def XOR(a, b, c):
    '''PRE: a, b - input labels, c - output label
            POST: libscapy-format string for XOR gate with specified labels'''
    return('2 1 '+str(a)+' '+str(b)+' '+str(c)+' 0110')

def NOT(a, b):
    '''PRE: a - input label, b - output label
            POST: libscapy-format string for NOT gate with specified labels'''
    return('1 1 '+str(a)+' '+str(b)+' 10')

def ADD(a, b, c_in, l):
    '''PRE: a, b - labels for the two addends, c_in - label for carry-in
        POST: l contains all gates for the binary full-adder, returned are labels for sum and carry-out'''
    ladd=[XOR(a, b, c_in + 1), AND(a, b, c_in + 2), XOR(c_in, c_in + 1, c_in + 3), AND(c_in, c_in + 1, c_in + 4), XOR(c_in + 2, c_in + 4, c_in + 5), AND(c_in + 2, c_in + 4, c_in + 6), XOR(c_in + 5, c_in + 6, c_in + 7)]
    l+=ladd
    sum, c_out = c_in + 3, c_in + 7
    return sum, c_out

def TWOCOMPARATOR(a, b, curr_wire, one, l):
    '''PRE: labels: a - minuend, b - subtrahend,  one - 1-wire
        POST: l contains all gates for the 2-bit comparator, returned is the label for result (w/values: 1 => A>=B, 0 => A<B)'''
    lsub=[XOR(b, one, curr_wire + 1), XOR(curr_wire + 1, a, curr_wire + 2), AND(curr_wire + 1, a, curr_wire + 3), AND(curr_wire + 2, curr_wire, curr_wire + 4), XOR(curr_wire + 3, curr_wire + 4, curr_wire + 5), AND(curr_wire + 3, curr_wire + 4, curr_wire + 6), XOR(curr_wire + 5, curr_wire + 6, curr_wire + 7)]
    l+=lsub
    l_cout = curr_wire+7
    return l_cout

def COMPARATOR(A, B, one, curr_wire, gates, l):
    '''PRE: A, B - 8-bit binary lists
        POST: l contains all gates for the 8-bit comparator, returned are result wire label (w/values: 1 => A>=B, 0 => A<B) and updated gates number'''

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
    '''PRE: A, B - two n-bit binary lists
        POST: l contains all gates for the n-bit ripple-carry adder, returned are sum wire label, updated curr_wire and gates'''

    # extend A, B by 0-valued bit on the left to account for overflow in the sum
    A.append(zero)
    B.append(zero)
    size=len(A)
    # use half-adder for the LSB's (no carry-in for LSB)
    lhalfadd=[XOR(A[0], B[0], curr_wire + 1), AND(A[0], B[0], curr_wire + 2)]
    l+=lhalfadd
    sum = [curr_wire + 1]
    curr_wire+=2
    gates+=2
    # use chained full-adders for the other bits
    for i in range(1, size):
        curr_sum, curr_wire=ADD(A[i], B[i], curr_wire, l)
        gates+=7
        sum.append(curr_sum)
    return sum, curr_wire, gates

def BLKMEAN(A, zero, curr_wire, gates, l):
    '''PRE: A - a (2D)list of 16 lists(16 8-bit binary numbers - sums of block pixels)
        POST: l contains all the gates for finding the sum of the 16 number, returned are the 8b mean and updated curr-wire, gates'''

    # use cascading approach to find the sum of all 16 numbers by adding two at a time => 4 "levels":
    block_size = len(A)
    num_of_lvl = int(log(block_size,2)+1)
    for lvl in range(1, num_of_lvl):
        # on each level, calculate sum = list of pairwise sums
        sum = []
        for i in range(0, len(A), 2):
            currsum, curr_wire, gates = BINADDER(A[i], A[i + 1], zero, curr_wire, gates, l)
            sum.append(currsum)
        # set A = sum since it contains the addends for the next "level"
        A = sum
    #A is now a list containing a single list(the 12-bit sum), chop off 4 LSB's to find mean (divide by 16)
    return A[0][4::], curr_wire, gates

def ALLMEANS(A, zero, curr_wire, gates, l):
    '''PRE: A - a (3D)list of 16 blocks (block is a list A descried in BLKMEAN)
        POST: l contains all the gates for finding all 16 blocks' means and the mean of the means, ..
            ..returned are the list containing the 16 block means and the main mean, updated curr_wire and gates'''
    means = []
    # for each block, calculate the mean and add it to the list
    for i in A:
        currmean, curr_wire, gates = BLKMEAN(i, zero, curr_wire, gates, l)
        means.append(currmean)
    # calculate the mean of the means and add it to the same list
    prime_mean, curr_wire, gates = BLKMEAN(means, zero, curr_wire, gates, l)
    means.append(prime_mean)
    return means, curr_wire, gates

def BLKHASH(M, one, curr_wire, gates, l):
    '''PRE: M - list of 17 means: M[0]..M[15] - blk means, M[15] - main mean
        POST: l contains all gates for finding the 16-bit hash, returned are the list of hash labels, updated curr_wire and gates '''
    size = len(M)
    hash=[]
    # for the block means, compare them to the main one and return the result (0 if less, 1 if gte), add the result to hash
    for i in range(size-1):
        curr_wire, gates = COMPARATOR(M[i], M[size-1], one, curr_wire, gates, l)
        hash.append(curr_wire)
<<<<<<< HEAD
    return hash, curr_wire, gates
=======
    return hash, curr_wire, gates
>>>>>>> dcf7f5733df26b0a567a793219831cf2f63d3a88
