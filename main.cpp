#include "./libraries/pHash.h"
//doxygen may be used for troubleshooting code
//linker flags in gcc -L -I 
//horsteman book on C++

int ph_bmb_imagehash(CImg<uint8_t> &img,
                     std::vector<double> &mean_vals,
                     uint8_t method, 
                     BinHash **ret_hash)
{
    const uint8_t *ptrsrc;  // source pointer (img)
    uint8_t *block;
    int pcol;  // "pointer" to pixel col (x)
    int prow;  // "pointer" to pixel row (y)
    int blockidx = 0;  //current idx of block being processed.
    double median;  // median value of mean_vals
    const int preset_size_x=256;
    const int preset_size_y=256;
    const int blk_size_x=16;
    const int blk_size_y=16;
    int pixcolstep = blk_size_x;
    int pixrowstep = blk_size_y;

    int number_of_blocks;
    uint32_t bitsize;
    // number of bytes needed to store bitsize bits.
    uint32_t bytesize;

    const int blk_size = blk_size_x * blk_size_y;
    block = (uint8_t*)malloc(sizeof(uint8_t) * blk_size);
    // in C++: block = new uint8_t[blk_size];

    if(!block)
        return -1;

    switch (img.spectrum()) {
    case 3: // from RGB
        img.RGBtoYCbCr().channel(0);
        break;
    default:
        break;
    }

    img.resize(preset_size_x, preset_size_y);

    // ~step b
    ptrsrc = img.data();  // set pointer to beginning of pixel buffer

    if(method == 2)
    {
        pixcolstep /= 2;
        pixrowstep /= 2;

        number_of_blocks =
                ((preset_size_x / blk_size_x) * 2 - 1) *
                ((preset_size_y / blk_size_y) * 2 - 1);
    } else {
        number_of_blocks =
                preset_size_x / blk_size_x *
                preset_size_y / blk_size_y;
    }

    bitsize= number_of_blocks;
    bytesize = bitsize / 8;

    mean_vals.resize(number_of_blocks);
    for(prow = 0;prow<=preset_size_y-blk_size_y;prow += pixrowstep)
    {

        /* block row */
        for(pcol = 0;pcol<=preset_size_x-blk_size_x;pcol += pixcolstep)
        {

            // idx for array holding one block.
            int blockpos = 0;
            for(int i=0 ; i < blk_size_y; i++)
            {
                ptrsrc = img.data(pcol, prow + i);
                memcpy(block + blockpos, ptrsrc, blk_size_x);
                blockpos += blk_size_x;
            }

            mean_vals[blockidx] = CImg<uint8_t>(block,blk_size).mean();
            //std::cout<<mean_vals[blockidx]<<",";
            blockidx++;
        }
        std::cout<<std::endl;
    }

    median = CImg<double>(&mean_vals[0], number_of_blocks).median();

    /* step e */
    BinHash *hash = _ph_bmb_new(bytesize);

    if(!hash)
    {
        *ret_hash = NULL;
        return -1;
    }

    *ret_hash = hash;
    for(uint32_t i = 0; i < bitsize; i++)
    {
        if(mean_vals[i] < median)
        {
            hash->addbit(0);
            std::cout<<0<<",";
        } else {
            hash->addbit(1);
            std::cout<<1<<",";
        }
    }
    free(block);
    return 0;
}

/**********************************************************/
#include "./libraries/pHash.h"// do I need to include phash? I don't think I'll be using any of their libraries
#include <vector>   //std::vector
#include <algorithm>    // std::sort
//also need to include opencv and install it too.

Mat imput_img = imread(filename, IMREAD_GRAYSCALE); //replace "filename" input parameter with actual input name

// is the size_t datatype the best one I could be using here?
//ideally, the datatype I use should match the datatype of the grayscaled pixel.
//what is that datatype? ASK: find it in the openCV documentation.

size_t block_side_length = 4;
size_t img_side_length = 16;
size_t last = block_side_length - img_side_length;

size_t pixel_intensity; 
std::vector<size_t> pi_vector;

size_t vector_sum;
size_t vector_length;
size_t block_mean;

std::vector<size_t> bm_vector;

size_t median;

// I forget, what is the scope of variables declared in for loops like init_row?

// In this nested for loop, I am iterating through a 2-d matrix of 2-d matrices.
//By dividing the image into blocks, each block itself is a 2d matrix of grayscale intensity values.
//The image, then, becomes a matrix of 2d matrices.
for (size_t init_row = 0; init_row <= last; init_row+=block_side_length){
    for (size_t init_col = 0; init_col <= last; init_col+=block_side_length){

        for (size_t block_row = init_row; block_row % 4 != 0 && block_row != init_row; block_row++){
            for (size_t block_col = init_col; block_col % 4 != 0 && block_col != init_col; block_col++){

                pixel_intensity = input_img.at<uchar>(block_row, block_col); //find out the filetype of the image, it matters for this step. Might need to replace uchar with something else.
                pi_vector.pushback(pixel_intensity);

            }
        }

        for(std::vector<size_t>::iterator it = pi_vector.begin(); it != pi_vector.end(); ++it){
            vector_sum += *it;
        }
        vector_length = pi_vector.size();
        block_mean = vector_sum / vector_length; // this uses integer division. ASK: does that interfere with the mean as calculated in the circuit?
        bm_vector.pushback(block_mean);
    }
}
std::sort (bm_vector.begin(), bm_vector.end());
median = bm_vector[bm_vector.size()/2];
//ASK: depending on what Bon and Anastasia say about the "normalizing" process, the median can be 


/*
TODOs
    1.[Later] Take input image and reduce to 256x256 (with cropping). This step, though it comes first in the 
        algorithm, can be implemented after May 9th.
    2.[DONE] Convert image to grayscale.
    3.[DONE] Divide image into 256 row-major blocks.
    4.[DONE]For each of the blocks, calculate the mean intensity and put that mean into a vector of means 
        after it's computed.
    5.[DONE] Sort the vector of means and find the median.
    6.Convert the median (of the block-means) into a binary number.
    7.somehow obtain the hash from the binary number (not too sure about this step)

TODO(later)
    8. Address comments and questions about type to skeith.
    9. get filename from std::in, make a command line interface to this application.
    10. find out how to compile with the OpenCV lbrary. 
*/