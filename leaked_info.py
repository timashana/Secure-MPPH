import cv2
import numpy as np #imported numpy because cv2 uses numpy data structures/data types like uint8

## NOTE NEED A 255*256 resolution image as input
##replace "filename" input parameter with actual input name
img2 = cv2.imread('img2.jpg',0)

block_side_length = 16
img2_side_length = 256
last = img2_side_length - block_side_length

pi_list = []
pi_list_export = []
bin_pi_list = []
bm_list = []

# In this nested for loop, I am iterating through a 2-d matrix of 2-d matrices.
# By dividing the image into blocks, each block itself is a 2d matrix of grayscale intensity values.

init_row = 0
while init_row <= last:

    init_col = 0
    while init_col <= last:

        block_row = init_row
        while block_row % block_side_length != 0 or block_row == init_row:

            block_col = init_col
            while block_col % block_side_length != 0 or block_col == init_col:


                pixel_intensity = img2[block_row, block_col] #find out the filetype of the image, it matters for this step. Might need to replace uchar with something else.
                pi_list.append(pixel_intensity)
                block_col+=1

            block_row+=1
        
        pi_sum = 0
        for pi in pi_list:
            pi_sum += pi

        pi_list_length = len(pi_list)
        block_mean = pi_sum // pi_list_length
        bm_list.append(block_mean)
        pi_list.clear()

        init_col+=block_side_length

    init_row+=block_side_length

leaked_side_length = 16
leaked = np.zeros((leaked_side_length,leaked_side_length), np.uint8)
i = 0
row = 0
while row < leaked_side_length:
    col = 0
    while col < leaked_side_length:
        leaked[row,col] = bm_list[i]
        col+=1
        i+=1
    row+=1

cv2.imwrite("leaked.jpg", leaked)