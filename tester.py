import numpy as np

with open('bin_img.txt', 'r') as f:
    s = f.read()
    f.close()
lst = [i for i in s]
input_arr = np.array(lst)
# divide into 16 blocks of 16 pixels (with 8b greyscale)
shape = (16, 16, 8)
tmp = input_arr.reshape(shape)
# go from numpy matrix to nested lists
A = tmp.tolist()
# A is a 3D list (16x16x8)
means = []
for i in A:
    blkmn = 0
    for j in i:
        blkmn += int(''.join([str(k) for k in reversed(j)]))
    blkmn = blkmn // len(A[0])
    means.append(blkmn)

main_mean = 0
for i in means:
    main_mean += i
main_mean = main_mean // len(means)

hash = []
for i in means:
    if i < main_mean:
        hash.append(0)
    else:
        hash.append(1)

print(''.join([str(i) for i in hash]))

#1110111001100101