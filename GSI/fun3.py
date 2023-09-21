import numpy as np
import cv2
import os
import pandas as pd


##constants
ResizeFactor = 0.56 #fit picture size to data size
ResizeFactorY = 0.57
ResizeFactorX = 0.6
scale = 34.4
ADC = int(4096/scale) +1      #12bit


Defl4_x = 33.7   #um
Defl4_y = 35.7   #um
Objx5_x_um = 900 #deflection in um in x when using 5x lens
Objx5_y_um = 700 #deflection in um in y when using 5x lens
Objx5_x_px = 597 #deflection in pixel in x when using 5x lens
Objx5_y_px = 461 #deflection in pixel in y when using 5x lens


##Scan area
um_to_px_x = Objx5_x_px/Objx5_x_um #px/um, 5x Objektiv
um_to_px_y = Objx5_y_px/Objx5_y_um #px/um, 5x Objektiv4
Defl6_x = Defl4_x * 9 * um_to_px_x #pixel
Defl6_y = Defl4_y * 9 * um_to_px_y #pixel

##general global variables
ErrorCnt = 0
ErrorList = []
cnt = 0
cnt2 = 0

##pixel colors
Red = np.array([0, 0, 255])
Blue = np.array([255, 0, 0])
Black = np.array([0, 0, 0])


def str2list(file, path):
    '''
    function to read the content of a file from the GSI Fullscan experiment
    to turn it into  a list and find SEL
    '''
    
    print("Current file: ", end = '')
    print(file)

    ##read document
    filePath= path + "/docs/" + file
    with open(filePath, 'r') as dat:
        data = dat.readlines()

    ##delete Header
    data = data[6:]
    row = []
    j = 0
    LatchUps = []

    ##clean up data & find Latch ups
    for d in data:
        ##divide the strings of each line in its components and save in list
        for i in range(len(d)):
            if d[i] == "\t" or d[i] == "\n":
                row.append(d[j:i])
                j = i + 1 #remember position of last whitespace

        ##find latch ups and save in list LatchUps
        if row[2] == '4':
            LatchUps.append(row)
        row = []
        j = 0

    print("\t", end = '')
    print(len(LatchUps), end = '')
    print(" latch ups found in ", end = '')
    print(file)
    return LatchUps

def Files(path):
    '''
    function to get a list of all files in the 'pics' and 'docs' subdirectories,
    it returns a list with file names of relevant files for each directory
    '''
    ##create list of files in the folder that end on .dat.txt
    docFiles = os.listdir(path + "/docs")
    picFiles = os.listdir(path + "/pics")


    ##remove not-*.dat.txt files from docFiles list
    for file in docFiles:
        if file[-8:] != ".dat.txt":
            print(file, end = '')
            print(" removed from internal data directory")
            docFiles.remove(file)

    ##remove not-*.tif files from picFiles list
    for pic in picFiles:
        if pic[-4:] != ".tif":
            print(pic, end = '')
            print(" removed from internal picture directory")
            picFiles.remove(pic)

    return [docFiles, picFiles]
