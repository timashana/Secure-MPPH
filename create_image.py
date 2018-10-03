import numpy as np
import cv2

img = []
ROW = 0
INTENSITY = 0
''' test_image_1 '''
while ROW < 256:
# for ite in range(16):
    tmp = []
    for intensity in range(INTENSITY, INTENSITY + 16):
        for k in range(16):
            tmp.append(intensity)
    for r in range(ROW, ROW + 16):
        img.append(tmp)

    ROW += 16
    INTENSITY += 16

imgp = []
for i in range(len(img)):
    imgp.append(img[i])
for i in range(len(img)):
    imgp[i] = img[255-i]

''' test_image_2 '''
# for row in range(128):
#     tmp = []
#     for i in range(128):
#         tmp.append(0)
#     for i in range(128):
#         tmp.append(255)
#
#     img.append(tmp)
#
# for row in range(128):
#     tmp = []
#     for i in range(128):
#         tmp.append(255)
#     for i in range(128):
#         tmp.append(0)
#
#     img.append(tmp)

# ''' test_image_3 '''
# for row in range(256):
#     tmp = []
#     for i in range(128):
#         tmp.append(0)
#     for i in range(128):
#         tmp.append(255)
#
#     img.append(tmp)

# ''' test_image_4 '''
# a = []
# b = []
# for j in range(8):
#     for i in range(16):
#         a.append(0)
#     for it in range(16):
#         a.append(255)
#
# for k in range(8):
#     for i in range(16):
#         b.append(255)
#     for it in range(16):
#         b.append(0)
#
# for l in range(8):
#     for i in range(16):
#         img.append(a)
#     for it in range(16):
#         img.append(b)

''' test_image_5 '''
# tmp = []
# for i in range(256):
#     tmp.append(255)
# for i in range(256):
#     img.append(tmp)

image = np.array(imgp, dtype=np.uint8)
# image = np.array(img) # this construct a different image
# np.set_printoptions(threshold=np.nan)   # print the whole array

# I = cv2.imread('given_mean.jpg', 0)
# cv2.imshow('image', I)
cv2.imshow('image', image)
cv2.waitKey(0)

# check = []
# for i in range(0, 27):
#     check.append(i)
#
# ii = np.array(check)
# shape = (3,3,3)
# ii = ii.reshape(shape)

# # read the string
# bits = [k for k in range(2, 524290)]
# #bits = [k for k in range(2, 2049)]
# input_arr = np.array(bits)
# ''' should we change it to np.array(bits, dtype=np.uint8) '''
# # divide into 16 blocks of 16 pixels (with 8b greyscale)
# shape = (256, 256, 8)
# tmp = input_arr.reshape(shape)
# np.set_printoptions(threshold=np.nan)
# # go from numpy matrix to nested lists
# # A = tmp.tolist() ''' WHY? '''

