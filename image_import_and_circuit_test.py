import cv2
import numpy as np

##replace "filename" input parameter with actual input name
img = cv2.imread('img.jpg',0)

block_side_length = 4
img_side_length = 16
last = img_side_length - block_side_length

pi_list = []
bin_pi_list = []
bm_list = []

# In this nested for loop, I am iterating through a 2-d matrix of 2-d matrices.
# By dividing the image into blocks, each block itself is a 2d matrix of grayscale intensity values.

init_row = 0
while init_row <= last:

    init_col = 0
    while init_col <= last:

        block_row = init_row
        while block_row % 4 != 0 or block_row == init_row:

            block_col = init_col
            while block_col % 4 != 0 or block_col == init_col:


                pixel_intensity = img[block_row, block_col] #find out the filetype of the image, it matters for this step. Might need to replace uchar with something else.
                pi_list.append(pixel_intensity)
                block_col+=1

            block_row+=1
        
        pi_sum = 0
        for pi in pi_list:
            pi_sum += pi

        pi_list_length = len(pi_list)
        block_mean = pi_sum // pi_list_length
        bm_list.append(block_mean)

        init_col+=block_side_length

    init_row+=block_side_length

# This is to compute the median of the block mean values.
# We're going to use the mean instead.
# sorted_bm_list = bm_list.sort()
# median = sorted_bm_list[len(sorted_bm_list)//2]

bm_sum = 0
for bm in bm_list:
    bm_sum += pi

bm_list_length = len(bm_list)
mean_of_block_means = bm_sum // bm_list_length

h_list = []

for bm in bm_list:
    if bm >= mean_of_block_means:
        h_list.append('1')
    else:
        h_list.append('0')

#ret_hash = ''.join(h_list)
#ret_pi = ''.join(pi_list)
ret_pi = ''.join(["{0:b}".format(pi) for pi in pi_list])
print(ret_pi)

with open('bin_img.txt','w') as f:
    f.write(ret_pi)
    f.close() 

# TODOs
#     1.[Later] Take input image and reduce to 256x256 (with cropping). This step, though it comes first in the 
#         algorithm, can be implemented after May 9th.
#     2.[DONE] Convert image to grayscale.
#     3.[DONE] Divide image into 256 row-major blocks.
#     4.[DONE]For each of the blocks, calculate the mean intensity and put that mean into a vector of means 
#         after it's computed.
#     5.[DONE] Sort the vector of means and find the median.
#     6.Convert the median (of the block-means) into a binary number.
#     7.somehow obtain the hash from the binary number (not too sure about this step)

#     -implment mean instead of median
#     -normalize the hash value

# TODO(later)
#     8. Address comments and questions about type to skeith.
#     9. get filename from std::in, make a command line interface to this application.
#     10. find out how to compile with the OpenCV lbrary. 
#     11. On about libscapi. Do Bon and Anastasia need me to incorporate their circuit into some c++ code, or will
#     will they be using the example test script with a different circuit file. (The test script is in 
#     libraries/libscapi/samples/Yao

#     Ask Rosario after 9th/10th to bring up the things.