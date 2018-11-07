# Secure-MPPH
 Secure-MPPH stands for Secure Multi-Party Perceptual Hash. The block-mean value perceptual hash algorithm is secured by Yao's garbling circuit. 

## This Repository Uses Submodules for Dependencies
Secure-MPPH draws upon [libscapi](https://github.com/cryptobiu/libscapi)  and [phash](https://github.com/clearscene/pHash) which are both 3rd party C++ libraries. Note: we use a [forked version of phash](https://github.com/dahadaller/pHash) in order to incorporate the block mean hash algorithm implemented [here.](https://gist.github.com/stereomatchingkiss/6b9034f72850b518f63631852d7b636f)  So, to properly clone this library, issue the following commands after `git clone https://github.com/timashana/Secure-MPPH.git` :

```bash
git submodule init
git submodule update
```

the submodules will then download into the `libraries/libscapi` and `libararies/phash` folders. Without this step, the `libraries` folder will remain empty and all code dependent on the non-stl libraries will not function. For more information about submodules check the [git-scm documentation](https://git-scm.com/book/en/v2/Git-Tools-Submodules).

## Circuit Build Program and Circuit Functions Library:
#### Circuit Description

NOTE: There are no actual values in this circuit, only wire labels. The values will be computed by libscapi on the circuit file and input files. All values below represent the wire labels in the circuit, and only one and zero represent 1 and 0 as those are labels for the wires with constant current of 1 or no current of 0.

In the circuit_builder:
1. The 1-D list of wire labels for the input bits of the picture is created in circuit builder (bits). If the size of the bit string representing grayscale image is bit_size, then labels in the list are [2..bit_size+1] since wire labels 0 and 1 are reserved for constant wires zero and one.
* Using numpy, the above list is changed into array, then shaped into a 3-D matrix and then into a 3-D list A with dimensions A1xA2xA3 where A1=# of blocks in the picture, A2=# of pixels in the block, A3=# of bits in grayscale representation of a bit. In case of 256x256 bit picture with 8-bit grayscale, the 3-D list has dimensions 256x256x8.
  * NOTE: A[0] contains wire labels for all bits in the first block of the picture. A[0][0] contains wire labels for 8-bits of grayscale for the 1st pixel in the 1st block of the picture
###### POSSIBLE BUG:
 * The wire labels follow the row-major order of blocks, not the general row-major order of the picture. In other words, the labels correspond to the 4-loop structure of the tester program and not the resulting bit string
2. The curr_wire variable is assigned the last used label in the circuit so far (at the moment it’s bit_size+1
3. ALLMEANS is called on A to compute wire labels for means of each block - assigned to 2-D list M, update curr_wire, update the number of gates in the circuit, and append the list of gates description with the used gates (list l in the arguments). In circuit functions:
   1. ALLMEANS accepts the above described 3-D list A, zero wire, # of gates, and the list l with descriptions for all gates in the circuit.
   2. It creates the list means to store wire labels for means of each block
   3. In the for loop, BLKMEAN is called for each block in A and the calculated wire labels for the block mean are appended to list means
   4. After all means are calculated, BLKMEAN is called one more time on list means to calculate the main mean (mean of means) and it is appended at the end on the means list
4. BLKHASH is called to compute the wire labels for the resulting hash - assigned to result, update curr_wire, number of gates in the circuit, and append the gates to the list l. In circuit functions:
   1. BLKHASH accepts the above described list of means with the main mean as the last element of the list, one wire, # of gates, and the list of gates l
   2. It creates the hash list for storing wire labels for the final hash
   3. For loop runs through all elements of means list, except last (since its the main hash) and calls COMPARATOR function to compare the current means element to the last element (the main mean)
   4. The resulting wire label for each comparison is appended to hash
5. The writeCircuitFile is called with # of gates, 2 for second party, number of input wires for the second party(=bit_size), list l with gates description, result - wire labels for the resulting hash

#### Compimentary Functions:
1. BLKMEAN:
   1. It accepts a 2-D list A (which is a list of pixels in one block with their 8-bit grayscale), zero wire, curr_wire, # of gates, and the list of gates l)
   2. Lvls is the number of binary additions we need to do to sum all of the pixels’ grayscale values (i.e. on first lvl we just sum pairs of values, then store the results, on the next level we sum pairs of those results from the first level and so on until we are left with only 2 values to sum - that’s the last lvl)
   3. For loop goes lvl by lvl and creates the sum list to save sums of pair in the lvl, then:
   4. The inner for loop runs through the list A with step 2 and adds the elements of A pairwise using BINADDER, then it append the resulting wire label to the sum list
   5. After the inner for loop is done, A is set to sum (to go to the “next lvl”)
   6. At the end of the outer for loop, A only contains one list (so it’s a list of one list, still 2-D), namely A[0], which contains the resulting wire labels for the sum of values all pixels in the block.
   7. To find the mean, we have to divide by the number of “lvls” since at each lvl the sums can be 1 bit longer than the addends. To do that, you can “chop off” that number of lvls from the end of the sum, hence deleting LSB’s. Since the list ordering is from LSB to MSB, the resulting mean is A[0][lvls::]
2. COMPARATOR:
   1. See the picture (M is one wire for this case)
   2. Each 2 bit block is TWOCOMPARATOR
   3. Output - C: 1 if A>=b, 0 if A<B
   4. We don't care about the difference itself, so the Si's from the picture is not in the TWOCOMPARATOR function nor is V in the COMPARATOR, we only care about C
3. Went through in person, Bon or David can add description to make sure we’re clear on it
   1. BINADDER
   2. ADD
   
## Test Program Description:
#### The tester’s program flow:
First we call BlockMeanHash function in which we:
* Transform the image into a grayscale 2D matrix of decimal values in range 0..255 (8-bit grayscale equivalent) using cv2 library function imread()
* Determine the image’s size and set the block’s size to be the square root of that
* Using 2 nested for loops, traverse the image matrix block by block. The iteration is done by starting with 0 and incrementing the index with block’s length for each iteration.
* In the further 2 nested while loops, the program traverses each individual pixel in the current block. This is done by setting the Inside_block iterator to the current block value from the for loop and then incrementing the inside_block index after every while loop iteration until inside_block%current block from the for loop is 0. That means we have incremented the starting index by exactly the size of the block and the loop is done. This is done in both row (first while loop) and column (second while loop) direction.
* Inside the above while loops, we append each pixel’s intensity into a list of block intensity (block_pi_list) and after the loops are done, we find the mean of that list and append it to the list of blocks’ mean intensities (block_mean_list) and clear that block’s block_pi_list for use in the next block
* After the for loops are done, meaning the program went through every block, we compute the mean of the block means in block_mean_least and assign it to mean_of_block_means
* Then, we go through the block_mean_list again and compare every block mean to the mean of means and append either 1 (if the block’s mean >= mean of means) or 0 otherwise to the separate list hash_as_list. Then we turn that list into a string and assign it to hash_as_string and return it

Then we call img2text utility function that:
* Transform the image into a grayscale 2D matrix of decimal values in range 0..255 (8-bit grayscale equivalent) using cv2 library function imread()
* Go through every pixel in the image in row major order and put its value into the list of intensities (img_pi_list)
* Turn the decimal values into binary (8-bit), put them into a list and then turn it into a string: img_pi_bin_string
* …
* Put the resulting bits into the file that will be the input for the circuit
