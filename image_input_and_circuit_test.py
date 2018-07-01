import cv2
from math import sqrt
import numpy as np #imported numpy because cv2 uses numpy data structures/data types like uint8

img = cv2.imread('img.jpg',0) # Load a color image in grayscale. Grayscale pixel values go from 0 to 255 inclusive.

# img_side_length = 16
# block_side_length = 4

img_side_length = len(img.columns)
block_side_length = sqrt(img_side_length)

last_row_of_block = img_side_length - block_side_length
last_col_of_block = last_row_of_block

# lists I'll be appending to throughout the function
block_pi_list = [] #this pixel intensity list is overwritten for each block and helps calculate the mean pixel intensity
block_mean_list = [] #Block mean list holds the block
hash_as_list = [] #calulate the hash digit for each block mean and then put it here


# In this nested for loop, I am iterating through a sort of 2-d matrix of 2-d matrices. 
    # it isn't really a 4d matrix because I only have two coordinates for the dataframe
    # it's really a 2d matrix for which I make reference to submatrices within it (which are also 2d)
# By dividing the image into blocks, each block itself is a 2d matrix of grayscale intensity values.
# the row_of_block and col_of_block variables represent the row,col values for the top left hand corner of each block relative to other blocks within the image
# the row_inside_block and col_inside_block variables represent the rows and columns within the blocks themselves.

for row_of_block in range(0,last_row_of_block,block_side_length):

    for col_of_block in range(0,last_col_of_block,block_side_length):

        row_inside_block = row_of_block
        while row_inside_block % 4 != 0 or row_inside_block == row_of_block:

            col_inside_block = col_of_block
            while col_inside_block % 4 != 0 or col_inside_block == col_of_block:

                pixel_intensity = img[row_inside_block, col_inside_block] #find out the filetype of the image, it matters for this step. Might need to replace uchar with something else.
                block_pi_list.append(pixel_intensity)
                col_inside_block+=1

            row_inside_block+=1
        
        pi_sum = sum(block_pi_list)
        block_pi_list_length = len(block_pi_list)
        block_mean = pi_sum // block_pi_list_length

        block_mean_list.append(block_mean)
        block_pi_list.clear()

bm_sum = sum(block_mean_list)
block_mean_list_length = len(block_mean_list)
mean_of_block_means = bm_sum // block_mean_list_length

for bm in block_mean_list:
    if bm >= mean_of_block_means:
        hash_as_list.append('1')
    else:
        hash_as_list.append('0')

hash_as_string = ''.join(hash_as_list)
print("image hash: ",hash_as_string)



# this should be a separate function for generating the bin_img.txt file that's binary grayscale values of the image 
img_pi_list = [] #pixel intensity list for whole image
for pixel_row in range(img_side_length):
    for pixel_col in range(img_side_length):
        img_pi_list.append(pixel_intensity)

#old img_pi_string returned pixel intensities in msb to lsb order
img_pi_string = ''.join(["{:08b}".format(pi) for pi in img_pi_list]) #creates boolean string from uint8 values in pixel intesnity list (block_pi_list) 

#write single-line output of image
with open('bin_img.txt','w') as f:
    f.write(img_pi_string)
    f.close()



# the code below writes the bin_img.txt file to a format readable by libscapi's Yao test 
s = ''
with open('bin_img.txt','r') as d:
    s = d.read()
d.close()
print(len(s))

with open('MPPHPartyOneInputs.txt','w') as x:
    x.write('2048\n')
    # for i in range(len(s)):
    #     x.write(s[i])
    #     x.write('\n')
    for i in range(1,257):
        for j in range(8*i-1,8*(i-1)-1,-1):
            # print(j)
            x.write(s[j])
            x.write('\n')
    x.close()