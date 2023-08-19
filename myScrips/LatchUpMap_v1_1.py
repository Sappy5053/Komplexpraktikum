from fun1 import *
from cvFun import *

#configuration
FRAME = True #True if you want to add a frame around the active areas in the pictures, otherwise False
SEL = True #True if you want to add the location of the SEL in the pictures
SHOW_INLIERS = False#True #True if you want to show the the inliers for every piture

##get current path
path = os.getcwd()
print('current path: ', end = '')
print(path)

#get a list of all relevant txt Files and pitures
[docFiles, picFiles] = Files(path)

##################################################################################

#'''
##open all pictures
panoExists = False
images = []
pics = [] #in order
for pic in picFiles:
    picPath = path + "/pics/" + pic
    image = cv2.imread(picPath)
    if image is None:
        continue
    elif pic[:4] == 'pano':
        panoExists = True
        continue
    else:
        images.append(image)
        pics.append(pic)

#prepare coordinate transformation        
pano = getPano(path, images, panoExists)
print('height, width = ', pano.shape[:2])
prepareMatching(pano)


##################################################################################
##read and process files one by one
for file in docFiles:
    LatchUps = str2list(file, path) #get list of SEL
    ##############################################################################
    ##find picture that corresponds to current file
    fileNo = file[-10:-8]
    i = 0
    for p in picFiles:
        picNo = p[-6:-4]
        
        if picNo == fileNo:
            pic = p
            image = images[i]
        if p[:3] == 'Jen':
            i+=1

    #get homography H = [M, pts]
    H = getHomography(image, SHOW_INLIERS)
    H = np.array(H[0])

    ##get height & width
    height, width = image.shape[:2]
    print("\t\tImage height: y = ", height)
    print("\t\tImage width:  x = ", width)

    #calculate SEL location in image coordinates
    luLoc = SEL_location(LatchUps, width, height)

    #calculate frame location in image coordinates
    frame = GenFrame(width, height)

    #transform into pano coordinatess
    luLocP = []
    frameP = []

##    try:
##    if True:
    for coord in luLoc:
##        print(luLoc)
        coord.append(1)
        coord = np.array(coord)
##        coord.transpose()
##        coord = cv2.smf.euclideanToHomogeneous(coord)
        c = np.matmul(H, coord)#cv2.perspectiveTransform(coord, H[0])
        luLocP.append(c)
##    print(luLocP)
    
    for coord in frame:
        coord.append(1)
        coord = np.array(coord)
##        coord.transpose()
##        coord = cv2.euclideanToHomogeneous(coord)
        c = np.matmul(H, coord)#c = cv2.perspectiveTransform(coord, H[0])
        frameP.append(c)
##    print(frameP)
##    except:
##        print('error ln 88-110')
        
    try:
    ##    if True:
        img = writeImg(pano, luLocP, pic, path, frameP, FRAME, SEL)
    ##        plt.imshow(img, 'gray')
    ##        plt.show()
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
#'''
