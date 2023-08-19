from fun1 import *

#configuration
FRAME = True #True if you want to add a frame around the active areas in the pictures, otherwise False
SEL = True #True if you want to add the location of the SEL in the pictures

##get current path
path = os.getcwd()
print('current path: ', end = '')
print(path)

#get a list of all relevant txt Files and pitures
[docFiles, picFiles] = Files(path)

##################################################################################

for pic in picFiles:
    try:
    ##open image
        print("\tOpening image ", pic)
        picPath = path + "/pics/" + pic
        image = cv2.imread(picPath)
        picName = pic[:-4] + "_Area.png"
        newPath = path + "/pics/Colour/" + picName
        # print(picPath)
        # print(image)

        ##get height & width
        # height, width = image.shape[:2]
        # print("\t\tImage height: y = ", height)
        # print("\t\tImage width:  x = ", width)
        #
        #
        # #calculate scanned area
        # luLoc = GenArea(width, height)
        # # frame = []

        #writeImg2(image, luLoc, pic, path,)
        cv2.imwrite(newPath, image)
    except:
        print('\tERROR GENERATING IMAGE FOR FILE: ', end = '')
        print(pic, end = '\n\n\n')
        ErrorCnt += 1
        ErrorList.append(pic)

if ErrorCnt == 0:
    print('All images were created successfully.', end = '\n\n')
else:
    print('Image generation failed for following ', ErrorCnt, ' Files: ', end = '\n')
    for i in ErrorList:
        print('\t', end = '')
        print(i, end = '\n')
