import os
from fun import *


##get current path
path = os.getcwd()
print('current path: ', end = '')
print(path)

#get a list of all relevant txt Files and pitures
[docFiles, picFiles] = Files(path)

##################################################################################
##read and process files one by one
for file in docFiles:
    LatchUps = str2list(file, path)
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


    #calculate SEL location in image coordinates
    luLoc = SEL_location(LatchUps, width, height)

    # try:
    writeImg(image, luLoc, pic, path)
#     except:
#         print('\tERROR GENERATING IMAGE FOR FILE: ', end = '')
#         print(file, end = '\n\n\n')
#         ErrorCnt += 1
#         ErrorList.append(file)
#
# if ErrorCnt == 0:
#     print('All images were created successfully.', end = '\n\n')
# else:
#     print('Image generation failed for following ', ErrorCnt, ' Files: ', end = '\n')
#     for i in ErrorList:
#         print('\t', end = '')
#         print(i, end = '\n')
