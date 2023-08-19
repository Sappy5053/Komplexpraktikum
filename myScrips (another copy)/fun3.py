import numpy as np
import cv2
import os
import pandas as pd


##constants
ResizeFactor = 0.56#0.497#1.086#0.735 #fit picture size to data size
ResizeFactorY = 0.57
ResizeFactorX = 0.6
scale = 34.4#23
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


ErrorCnt = 0
ErrorList = []
cnt = 0
cnt2 = 0

Red = np.array([0, 0, 255])
Blue = np.array([255, 0, 0])
Black = np.array([0, 0, 0])



'''
def rot90DEG_left(coord):
    # print(coord)
    global Defl6_y
    npA_coord = np.array(coord)
    # print(npA_coord)
    rot90 = [[0, -1], [1, 0]]

    npA_rot90 = np.array(rot90)
    # print(npA_rot90)

    erg = np.matmul(npA_rot90, npA_coord)


    erg[0] = erg[0] + Defl6_y
    return erg
    # print(erg)
    # print(erg[0])
    # print(erg[1])'''

def str2list(file, path):
##    file = docFiles[1]
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

    # DF_LatchUps = pd.DataFrame(comb)
    print("\t", end = '')
    print(len(LatchUps), end = '')
    print(" latch ups found in ", end = '')
    print(file)
    return LatchUps

def Files(path):
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




























'''
def SEL_location(LatchUps, width, height):
    ##calculate location of latch ups in active area (Defl6)
    xFactor = Defl6_x / ADC  # number of ADC steps in one pixel in x direction
    yFactor = Defl6_y / ADC  # number of ADC steps in one pixel in y direction
    luLoc = []
    for l in LatchUps:
        xPos = int(int(l[0]) * xFactor)
        yPos = int(int(l[1]) * yFactor)
        coordinates  = SELarea2pic(xPos, yPos, width, height)
        luLoc.append(coordinates)
    return luLoc


def writeImg(image, luLoc, pic, path, frame, FRAME, SEL):
    #generate name & path
    picName = pic[:-4] + "_LatchUpMap.png"
    newPath = path + "/pics/Latchup/" + picName

    #add frame
    if FRAME:
        for i in frame:
            x = int(i[0])
            y = int(i[1])
            image[x][y] = [255, 0, 0]
        print("\tGenerated latch up map with frame: ", end='')
        print(picName, end='\n\n\n')
    else:
        print("\tGenerated latch up map: ", end='')
        print(picName, end='\n\n\n')

    ##turn latch up areas red
    if SEL:
        for i in luLoc:
            x = int(i[0])
            y = int(i[1])
            image[x][y] = [0, 0, 255]

    #write image
    cv2.imwrite(newPath, image)

    return image

def writeImg2(image, luLoc, pic, path):
    #generate name & path
    picName = pic[:-4] + "_Area.png"
    newPath = path + "/pics/Area/" + picName

    for i in luLoc:
        x = i[0]
        y = i[1]
        image[x][y] = [0, 0, 255]

    #write image
    cv2.imwrite(newPath, image)


def GenFrame(width, height):
    frame = []
    #generate coordinates for left and right border
    for i in range(int(Defl6_y)):
        # calculate in outermost pixels of active area
        left = SELarea2pic(0, i, width, height)
        right = SELarea2pic(Defl6_x, i, width, height)
        frame.append(left)
        frame.append(right)

    #generate coordinates for upper and lower border
    for i in range(int(Defl6_x)):
        upper = SELarea2pic(i, 0, width, height)
        lower = SELarea2pic(i, Defl6_y, width, height)
        frame.append(upper)
        frame.append(lower)

    return frame


def SELarea2pic(xPos, yPos, width, height):
    ##mirroring on y-axis
    xPosN = Defl6_x - (xPos + 1)

    ##rotate 90DEG anti-clockwise
    [xPosNew, yPosNew] = rot90DEG_left([xPosN, yPos])#[xPos, yPos]#

    ##coordinate transformation (Defl6 to image coordinates)
    yNew = int(yPosNew + (width / 2) - (Defl6_x / 2))
    xNew = int(xPosNew + (height / 2) - (Defl6_y / 2))

    ##save latch up locations in image coordinates
    return [xNew, yNew]


def GenArea(width, height):
    area = []

    for i in range(int(Defl6_y)):
        for j in range(int(Defl6_x)):
            pixel = SELarea2pic(j, i, width, height)
            area.append(pixel)

            # x, y
    return area
'''
