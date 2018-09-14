import cv2
from math import sqrt
import numpy as np #imported numpy because cv2 uses numpy data structures/data types like uint8

#input image must be square (n by n resolution)
def blockMeanHash(imgFileName):
    img = cv2.imread(imgFileName,0) # Load a color image in grayscale. Grayscale pixel values go from 0 to 255 inclusive.

    img_side_length = img.shape[0]
    block_side_length = int(sqrt(img_side_length))

    # lists I'll be appending to throughout the function
    block_pi_list = [] #this pixel intensity list is overwritten for each block and helps calculate the mean pixel intensity
    block_mean_list = [] #Block mean list holds the block
    hash_as_list = [] #calulate the hash digit for each block mean and then put it here


    # In this nested for loop, I am iterating through a (kind of) of 2-d matrix of 2-d matrices. 
        # it isn't really a 4d matrix because I only have two coordinates for the dataframe
        # it's really a 2d matrix for which I make reference to submatrices within it (which are also 2d)
    # By dividing the image into blocks, each block itself is a 2d matrix of grayscale intensity values.
    # the row_of_block and col_of_block variables represent the row,col values for the top left hand corner of each block relative to other blocks within the image
    # the row_inside_block and col_inside_block variables represent the rows and columns within the blocks themselves.

    # these two outermost for loops move from block to block within the image (if it's a 256x256 image, then there are 16 16x16 blocks)
    for row_of_block in range(0,img_side_length,block_side_length): #range(start,stop,step) start is included, stop is excluded, new index =  old index + step

        for col_of_block in range(0,img_side_length,block_side_length):

            # these two innermost loops cycle through the contents inside each block (each 16x16 block, in the case of 256x256 image)
            row_inside_block = row_of_block
            while row_inside_block % block_side_length != 0 or row_inside_block == row_of_block:

                col_inside_block = col_of_block
                while col_inside_block % block_side_length != 0 or col_inside_block == col_of_block:

                    #inside each block, all we're doing is transferring each pixel intensity in the block to a list

                    pixel_intensity = img[row_inside_block, col_inside_block]
                    block_pi_list.append(pixel_intensity)
                    #print("Row/Col Coordinates: (", row_inside_block, col_inside_block, ")") #this is troubleshooting code that prints in what order the pixels are traversed
                    col_inside_block+=1

                row_inside_block+=1

            # after we've gotten the pixel intensity list for a given block, we use it to compute the block mean
            pi_sum = sum(block_pi_list)
            block_pi_list_length = len(block_pi_list)
            block_mean = pi_sum // block_pi_list_length

            # we append the block mean we generated for the given block to a block mean list, which we use later to compute the hash
            block_mean_list.append(block_mean)
            block_pi_list.clear()

    # here we compute the mean of the block means (instead of using medians) to threshold the block mean list and create a hash 
    bm_sum = sum(block_mean_list)
    block_mean_list_length = len(block_mean_list)
    mean_of_block_means = bm_sum // block_mean_list_length

    # finally, we use our threshold to generate the hash
    for bm in block_mean_list:
        if bm >= mean_of_block_means:
            hash_as_list.append('1')
        else:
            hash_as_list.append('0')

    hash_as_string = ''.join(hash_as_list)
    return hash_as_string


# this is a utility function that generates an binary text file from an image. this text file will serve as input to the circuit.
def img2text(imgFileName):
    # this should be a separate function for generating the bin_img.txt file that's binary grayscale values of the image 
    img = cv2.imread(imgFileName,0) # Load a color image in grayscale. Grayscale pixel values go from 0 to 255 inclusive
    img_side_length = img.shape[0]

    img_pi_list = [] #pixel intensity list for whole image
    for pixel_row in range(img_side_length):
        for pixel_col in range(img_side_length):
            pixel_intensity = img[pixel_row, pixel_col] #possible source of error if hashes don't match
            img_pi_list.append(pixel_intensity)

    #old img_pi_string returned pixel intensities in msb to lsb order
    img_pi_bin_string = ''.join(["{:08b}".format(pi) for pi in img_pi_list]) #creates boolean string from uint8 values in pixel intesnity list (block_pi_list) 
    img_pi_bin_list = list(img_pi_bin_string)
    img_pi_bin_string_column = "\n".join(img_pi_bin_list)
    MPPHPartyOneInputs = str(len(img_pi_bin_list)) + "\n" + img_pi_bin_string_column

    with open('MPPHPartyOneInputs.txt','w') as f:
        f.write(MPPHPartyOneInputs)
        f.close()


# execution of functions starts here
print("image hash: ", blockMeanHash('big_img.jpg'))
img2text('big_img.jpg')