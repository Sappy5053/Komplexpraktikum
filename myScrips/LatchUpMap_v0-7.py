import os
import cv2
import numpy as np
import sys
import pandas as pd

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
    # print(erg[1])


##constants
ADC = 4096       #12bit
Defl4_x = 33.7   #um
Defl4_y = 35.7   #um
Objx5_x_um = 900 #deflection in um in x when using 5x lens
Objx5_y_um = 700 #deflection in um in y when using 5x lens
Objx5_x_px = 557 #deflection in pixel in x when using 5x lens
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

##current path
path = os.getcwd()
print(path)
##create list of files in the folder that end on .dat.txt
docFiles = os.listdir(path + "/docs")
picFiles = os.listdir(path + "/pics")

##print(docFiles, end = '\n\n')
##print(picFiles)

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

##################################################################################
##read and process files one by one
for file in docFiles:
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
    data1 = []
    LatchUps = []
    Xc = []
    Yc = []

    ##clean up data & find Latch ups
    for d in data:
        ##divide the strings of each line in its components and save in list
        for i in range(len(d)):
            if d[i] == "\t" or d[i] == "\n":
                row.append(d[j:i])
                j = i + 1 #remember position of last whitespace

        ##append edited rows to data1
        data1.append(row)
        ##find latch ups and save in list LatchUps
        if row[2] == '4':
            Xc.append(row[0])
            Yc.append(row[1])
            LatchUps.append(row)
        row = []
        j = 0
        # comb = {
        #     'X': Xc,
        #     'Y': Yc
        # }
    # DF_LatchUps = pd.DataFrame(comb)
    print("\t", end = '')
    print(len(LatchUps), end = '')
    print(" latch ups found in ", end = '')
    print(file)

    ##############################################################################
    ##find picture that corresponds to current file
    fileNo = file[-10:-8]
    for p in picFiles:
        picNo = p[-6:-4]

        if picNo == fileNo:
            pic = p

    ##open image
    print("\tOpening image ", pic)
    picPath = path + "/pics/" + pic
    image = cv2.imread(picPath)

    ##get height & width
    height, width = image.shape[:2]
    print("\t\tImage height: y = ", height)
    print("\t\tImage width:  x = ", width)

    ##calculate location of latch ups in active area (Defl6)
    luLoc = []
    xFactor = Defl6_x/ADC #number of ADC steps in one pixel in x direction
    yFactor = Defl6_y/ADC #number of ADC steps in one pixel in y direction
    cnt = 0
##############################################################################################
    # LatchUps = []
    # zwischen = []
    #
    # for i in range(ADC):
    #     zwischen.append(i)
    # for i in range(ADC):
    #     for j in range(ADC):
    #         a = [zwischen[i], zwischen[j]]
    #         LatchUps.append(a)

##############################################################################################
    for l in LatchUps:
        cnt += 1
        xPos = int(int(l[0]) * xFactor)
        yPos = int(int(l[1]) * yFactor)

        ##mirroring on y-axis
        xPosN = Defl6_x - (xPos + 1)

        ##rotate 90DEG anti-clockwise
        [xPosNew, yPosNew] = rot90DEG_left([xPosN, yPos])

        ##coordinate transformation (Defl6 to image coordinates)
        yNew = int(yPosNew + (width/2) - (Defl6_x/2))
        xNew = int(xPosNew + (height/2) - (Defl6_y/2))
        

        ##save latch up locations in image coordinates
        luLoc.append([xNew, yNew])

    #print(luLoc)

    try:
        ##turn latch up areas red
        for i in luLoc:
            x = i[0]
            y = i[1]
            image[x][y] = [0, 0, 255]
        ##save as picture
        picName = pic[:-4] + "_LatchUpMap.png"
        newPath = path + "/pics/Latchup/" + picName

        cv2.imwrite(newPath, image)

        print("\tGenerated latch up map: ", end = '')
        print(picName, end = '\n\n\n')

    except:
        print('\tERROR GENERATING IMAGE FOR FILE: ', end = '')
        print(file, end = '\n\n\n')
        ErrorCnt += 1
        ErrorList.append(file)

if ErrorCnt == 0:
    print('All images were created successfully.', end = '\n\n')
else:
    print('Image generation failed for following ', ErrorCnt, ' Files: ', end = '\n')
    for i in ErrorList:
        print('\t', end = '')
        print(i, end = '\n')
