import cv2
import pandas as pd
import numpy as np
import os

sep     = '\t' #character that seperates values in file
erase   = 10 #number of detected SEL to be erased after first one SEL 
empty   = '0\t0\t0\t0\t0\n' #line that is inserted in place of incorrect SEL
   
#get documents that end with '.dat.txt'
path = os.getcwd()
path = path + '/docs/'
path1 = path + 'remStrips/'
docs = os.listdir(path)
docs = [doc for doc in docs if doc.endswith('.dat.txt')]

for doc in docs:
    lines1 = []
    #read documents
    with open(path + doc, 'r') as f:
        lines = f.readlines()
        lines = lines[6:]
    
    for i in range(len(lines)):
        #turn string into list, sperate string at sep
        line = lines[i]
        l = line.split(sep)
        
        if l[2] == '4':
            #latchup found --> save line
            lines1.append(line)
            for j in range(i+1, i+1+erase):
                ##substitude with empty lines
                lines[j] = empty
    file = path1 + doc

    #write list with SEL to file
    with open(file, 'w') as f:
        for line in lines1:
            f.write(line)

    #print number of Ions fires vs number of SEL
    print(len(lines), len(lines1))
    
    
            
        
