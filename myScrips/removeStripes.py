import cv2
import pandas as pd
import numpy as np
import os

sep     = '\t'
erase   = 10
empty   = '0\t0\t0\t0\t0\n'

genImg  = False

    
#get documents
path = os.getcwd()
path = path + '/docs/'
path1 = path + 'remStrips/'
docs = os.listdir(path)
docs = [doc for doc in docs if doc.endswith('.dat.txt')]

lines1 = []
for doc in docs:
    lines1 = []
    #read documents
    with open(path + doc, 'r') as f:
        lines = f.readlines()
        lines = lines[6:]
    
    for i in range(len(lines)):
        line = lines[i]
        l = line.split(sep)
        if l[2] == '4':
            #latchup
            lines1.append(line)
            for j in range(i+1, i+1+erase):
##                substitude with empty lines
                lines[j] = empty
    file = path1 + doc

    with open(file, 'w') as f:
        for line in lines1:
            f.write(line)

    print(len(lines), len(lines1))
    
    if genImg:
        df = pd.read_csv(path1 + doc, sep = sep, header = None)
        
        df.drop(columns = [2], inplace = True)

        df = df.astype(int)
        df = df/34.4
        df = df.astype(int)
    ##    NP = df.to_numpy()

        arr = np.zeros((120, 120))

    ##    shape = NP.shape
    ##    print(shape)

        for index, row in df.iterrows():
            x,y = row[0], row[1]
            arr[x-1,y-1] = 255

        cv2.imwrite(path1 + doc+ '.png', arr)
    

            
        
