##import cv2
##import os
##import pandas as pd
##import numpy as np
##from scipy.ndimage import zoom
from binningFun_v0_6 import *

#get links
cwd = os.getcwd()
path1 = cwd     + '/pics/'
path2 = path1   + 'resized/'
path3 = cwd     + '/csv/'
path4 = path3   + 'resized/'
path5 = cwd     + '/panos/'

#get input panos
List = os.listdir(path5)

for i in range(len(List)):
    print(i, ':\t', List[i])

print()

UserInput = input('Choose the number corresponding to the panoramas you want to use to calculate the resizing factor (Format: GSI Panorama, LUNTE Panorama)\n')

#process User Input
j = 0
num = []
for i in range(len(UserInput)):
    if UserInput[i] == ',':  
        n = int(UserInput[j:i])
        j = i+1
        num.append(n)

n = int(UserInput[j:])
num.append(n)

#get Binning Factors
[x, y] = BinningFactors(path5 + List[int(num[0])], path5 + List[int(num[1])])

print('Factors: x:', x, ', y:', y)

#resize all csv and save in sub-folder resized
csvList = os.listdir(path3)
print(csvList)

for csv in csvList:
    #csv = csv
    try:
        NP = ResizeCSV(path3, x, y, csv)
        DF = pd.DataFrame(NP)
        DF = DF.astype(int)
        DF.to_csv(path4+csv, header = None, index = None, sep = ';')
        print(csv, ' saved!')
    except IsADirectoryError:
        pass

#resize all pic and save in sub-folder resized
picList = os.listdir(path1)
picList = picList#[3:]
print(picList)

for pic in picList:
    try:
        ResizePic(path1, path2, pic, x, y)
    except:
        continue

