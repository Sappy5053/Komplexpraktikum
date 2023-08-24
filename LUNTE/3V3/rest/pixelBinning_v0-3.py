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

###get path of 2 Panos
##path1 = input('Path to GSI Panorama: ')
##path2 = input('Path to LUNTE Panorama: ')

path1 = '/home/thomas/Documents/KP_schmidt/230607_DLTM-ATtiny20-MI-Fullscans (copy)/3V3/rest/panos/Jenamicro_pano_corp.png'
path2 = '/home/thomas/Documents/KP_schmidt/230607_DLTM-ATtiny20-MI-Fullscans (copy)/3V3/rest/panos/20230606-DLTM-ATtiny20_thr.png'

[x, y] = BinningFactors(path1, path2)

print('Factors', x, y)

#get links
cwd = os.getcwd()
path1 = cwd + '/pics/'
path2 = path1 + 'resized/'
path3 = cwd + '/csv/'
path4 = path3 + 'resized/'


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

picList = os.listdir(path1)
picList = picList[3:]
print(picList)

for pic in picList:
##    try:
    if True:
        ResizePic(path1, path2, pic, x, y)
##    except:
##        continue





















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
