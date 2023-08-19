import cv2
import os
import pandas as pd
import numpy as np


def BinningFactors(path1, path2):
    #open open Pano from GSI experiment
    P1 = cv2.imread(path1)
    P1Height, P1Width = P1.shape[:2]
    print('GSI: ',P1.shape[:2])

    #open Lunte Pano
    P2 = cv2.imread(path2)
    P2Height, P2Width = P2.shape[:2]
    print('LUNTE: ',P2.shape[:2])

    #calculate factors
    xFac = P1Width/P2Width
    yFac = P1Height/P2Height
    return [xFac, yFac]#P2Resized

def ResizeCSV(path3, x, y):
    DF = pd.read_csv(path3 + csv, header = None, sep = ';')
    NP = DF.to_numpy()
    h, w = NP.shape[:2]
##    print(h, w, '\n\n')

    PixX = int(x*w)
    PixY = int(y*h)

    NP1 = np.resize(NP, [PixY, PixX])
    return NP1

def ResizePic(path1, path2, picName, x, y):
    pic = cv2.imread(path1 + picName)
    height, width = pic.shape[:2]

    w = int(x * width)
    h = int(y * height)
    dim = (w, h)

    resized = cv2.resize(pic, dim, interpolation = cv2.INTER_AREA)

    cv2.imwrite(path2 + picName, resized)

#get links
cwd = os.getcwd()
path1 = cwd     + '/pics/'
path2 = path1   + 'resized/'
path3 = cwd     + '/csv/'
path4 = path3   + 'resized/'
path5 = cwd     + '/panos'

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
[x, y] = BinningFactors(int(num[0]), int(num[1]))

print('Factors: x:', x, ', y:', y)

#resize all csv and save in sub-folder resized
csvList = os.listdir(path3)
print(csvList)

for csv in csvList:
    try:
        NP = ResizeCSV(path3, x, y)
        DF = pd.DataFrame(NP)
    ##    print(DF.head())
        DF.to_csv(path4+csv, header = None, index = None, sep = ';')
    except:
        continue

#resize all csv and save in sub-folder resized
picList = os.listdir(path1)
picList = picList[3:]
print(picList)

for pic in picList:
    try:
        ResizePic(path1, path2, pic, x, y)
    except:
        continue





















###get and resize the LUNTE Strips
##picList = os.listdir(path1)
##print(picList)

##for pic in picList:
##    if pic[-4:] == '.png':
##        print(pic)
##        ResizePic(path1+pic, (x, y), path2 + pic)
##
        

#resize
##    ##resize GSI Panorama
##    dim = (P1Width, P1Height)
##    P2Resized = cv2.resize(P2, dim, interpolation = cv2.INTER_AREA)
