'''
Anastasiia Timashova github.com/timashana

This is a tester program to evaluate ALLMEANS function part of the circuit
    by creating the libscapi format circuit for calculationg list of means
    for 4 blocks of 4 pixels that can be controlled manually (every pixel value is hardcoded)
    or automatically (blocks are identical).
    The result is a binary string of 5 means: 4  - for every block and the last value
    is the mean of the previous 4 - the main mean
'''

from hash_circuit_functions import *

def writeCircuitFile(num_of_gates, parties, p2_wires, gateList, output):
    with open('MPPH.txt','w') as f:
        s1 = str(num_of_gates) + '\n' + str(parties) + '\n'
        s1 += '1 ' + str(2) + '\n\n'
        f.write(s1)
        # Party one provides only the 0 and 1 wires
        for i in range(0, 2):
            f.write(str(i))
            f.write('\n')

        input_size = len(p2_wires)*len(p2_wires[0])*len(p2_wires[0][0])
        s2 = '2 ' + str(input_size) + '\n\n'
        f.write(s2)
        for i in range(2, input_size + 2):
            f.write(str(i))
            f.write('\n')

        s = '\n'+ str(len(output)*len(output[0]))+'\n\n'
        f.write(s)
        for i in output:
            for j in i:
                f.write(str(j))
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
        for i in range(0,2):
            s = str(i) + '\n'
            t.write(s)
        t.close()

def writePartyTwoInputFile(p2):
    with open('MPPHPartyTwoInputs.txt', 'w') as t:
        input_size = len(p2)*len(p2[0])*len(p2[0][0])
        s = str(input_size)+'\n'
        t.write(s)
        for i in p2:
            for j in i:
                for k in j:
                    s = str(k) + '\n'
                    t.write(s)
        t.close()

l=[]    #list to store the libscapi-formatted gates
zero=0  # 0-wire
one=1   # 1-wire
gates = 0   # keep track of the number of gates in the circuit
curr_wire = 2   # keep track of the last used label

''' BELOW ALL 4 BLOCKS ARE IDENTICAL FOR SIMPLICITY OR CHOSE ONE AFTER FOR MANUAL CONTROL OF EVERY PIXEL'''

'''all numbers are represented in [LSB...MSB] format
        for example, 123 -> [3, 2, 1]'''
# A = [0, 0, 0, 0, 0, 0, 0, 0]
# B = [1, 1, 1, 1, 1, 1, 1, 1]
# C = [0, 0, 0, 0, 0, 0, 0, 0]
# D = [1, 1, 1, 1, 1, 1, 1, 1]
#
# A_labels = [i for i in range(curr_wire, curr_wire + len(A))]
# curr_wire += len(A)
# B_labels = [i for i in range(curr_wire, curr_wire + len(B))]
# curr_wire += len(B)
# C_labels = [i for i in range((curr_wire), curr_wire + len(C))]
# curr_wire += len(C)
# D_labels = [i for i in range((curr_wire), curr_wire + len(D))]
# curr_wire += len(D)
#
# # 1 block of 4 pixels
# block = [A, B, C, D]
#
# # 4 identical blocks as above
# blocks = [block[::], block[::], block[::], block[::]]
#
# nums = [A_labels, B_labels, C_labels, D_labels]
# blocks_labels = [nums[::], [[i + len(nums)*len(nums[0]) for i in j] for j in nums], [[i + len(nums)*len(nums[0])*2 for i in j] for j in nums], [[i + len(nums)*len(nums[0])*3 for i in j] for j in nums]]
# curr_wire = 2 + (curr_wire-2)*4

''' END OF IDENTICAL BLOCKS SECTION '''


''' MANUAL BLOCK ASSIGNMENT TO CONTROL EVERY PIXEL'''

'''all numbers are represented in [LSB...MSB] format
        for example, 123 -> [3, 2, 1]'''
A_1 = [0, 0, 0, 0, 0, 0, 0, 0]
B_1 = [0, 0, 0, 0, 0, 0, 0, 0]
C_1 = [0, 0, 0, 0, 0, 0, 0, 0]
D_1 = [0, 0, 0, 0, 0, 0, 0, 0]

A_1_labels = [i for i in range(curr_wire, curr_wire + len(A_1))]
curr_wire += len(A_1)
B_1_labels = [i for i in range(curr_wire, curr_wire + len(B_1))]
curr_wire += len(B_1)
C_1_labels = [i for i in range((curr_wire), curr_wire + len(C_1))]
curr_wire += len(C_1)
D_1_labels = [i for i in range((curr_wire), curr_wire + len(D_1))]
curr_wire += len(D_1)

# 1 block of 4 pixels
block_1 = [A_1, B_1, C_1, D_1]

A_2 = [0, 0, 0, 0, 0, 0, 0, 0]
B_2 = [1, 0, 1, 0, 1, 0, 1, 0]
C_2 = [0, 0, 0, 0, 0, 0, 0, 0]
D_2 = [1, 0, 1, 0, 1, 0, 1, 0]

A_2_labels = [i for i in range(curr_wire, curr_wire + len(A_2))]
curr_wire += len(A_2)
B_2_labels = [i for i in range(curr_wire, curr_wire + len(B_2))]
curr_wire += len(B_2)
C_2_labels = [i for i in range((curr_wire), curr_wire + len(C_2))]
curr_wire += len(C_2)
D_2_labels = [i for i in range((curr_wire), curr_wire + len(D_2))]
curr_wire += len(D_2)

# 1 block of 4 pixels
block_2 = [A_2, B_2, C_2, D_2]

A_3 = [1, 1, 1, 1, 1, 1, 1, 1]
B_3 = [0, 1, 0, 1, 0, 1, 0, 1]
C_3 = [1, 1, 1, 1, 1, 1, 1, 1]
D_3 = [0, 1, 0, 1, 0, 1, 0, 1]

A_3_labels = [i for i in range(curr_wire, curr_wire + len(A_3))]
curr_wire += len(A_3)
B_3_labels = [i for i in range(curr_wire, curr_wire + len(B_3))]
curr_wire += len(B_3)
C_3_labels = [i for i in range((curr_wire), curr_wire + len(C_3))]
curr_wire += len(C_3)
D_3_labels = [i for i in range((curr_wire), curr_wire + len(D_3))]
curr_wire += len(D_3)

# 1 block of 4 pixels
block_3 = [A_3, B_3, C_3, D_3]

A_4 = [1, 1, 1, 1, 1, 1, 1, 1]
B_4 = [1, 1, 1, 1, 1, 1, 1, 1]
C_4 = [1, 1, 1, 1, 1, 1, 1, 1]
D_4 = [1, 1, 1, 1, 1, 1, 1, 1]

A_4_labels = [i for i in range(curr_wire, curr_wire + len(A_4))]
curr_wire += len(A_4)
B_4_labels = [i for i in range(curr_wire, curr_wire + len(B_4))]
curr_wire += len(B_4)
C_4_labels = [i for i in range((curr_wire), curr_wire + len(C_4))]
curr_wire += len(C_4)
D_4_labels = [i for i in range((curr_wire), curr_wire + len(D_4))]
curr_wire += len(D_4)

# 1 block of 4 pixels
block_4 = [A_4, B_4, C_4, D_4]

# 4 blocks as above
blocks = [block_1[::], block_2[::], block_3[::], block_4[::]]

# labels of the first block
nums = [A_1_labels, B_1_labels, C_1_labels, D_1_labels]
# the other 3 blocks' labels follow right after each other

blocks_labels = [nums[::], [[i + len(nums)*len(nums[0]) for i in j] for j in nums], [[i + len(nums)*len(nums[0])*2 for i in j] for j in nums], [[i + len(nums)*len(nums[0])*3 for i in j] for j in nums]]

''' END OF MANUAL CONTROL SECTION '''

result3, curr_wire, gates = ALLMEANS(blocks, zero, one, curr_wire, gates, l)
writeCircuitFile(gates, 2, blocks_labels, l, result3)
writePartyOneInputFile()
writePartyTwoInputFile(blocks)
