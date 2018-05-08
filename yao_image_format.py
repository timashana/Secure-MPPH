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
