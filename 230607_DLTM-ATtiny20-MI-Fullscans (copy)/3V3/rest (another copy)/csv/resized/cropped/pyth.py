##import numpy as np
##import pandas as pd
##
##df = pd.read_csv('NewCSV.csv', sep = ';')
##nump = df.to_numpy(dtype = int)
##
##h, w = np.shape(nump)
##
##print(h, w)
##
##for r in range(h):
##    for c in range(w):
##        n = nump[r,c]
##        if n > 4000:
##            print(r,c,n)


base = 26

abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

a = 'f'
b = 'k'
e = 29

for i in range(len(abc)):
    if abc[i] == a:
        c = i*base
    if abc[i] == b:
        d = i

c = c+d-e

d = int(c % base)
c = int((c-d)/base)
print(d,c)

print(abc[c]+abc[d])





        
