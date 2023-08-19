from fun1 import *
##import imutils# import paths
####from pathlib import Path
from matplotlib import pyplot as plt


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

#'''
##open all pictures
##print(picFiles)
images = []
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

#get stitched image or stitch it
if panoExists:#Path.exists(path + '/pics/pano.tiff'):#Path.is_file(path + '/pics/pano.tiff'):
    pano = cv2.imread(path + '/pics/pano.tif')
else:
    '''
    ##stitching algorithmus found on
    ##https://pyimagesearch.com/2018/12/17/image-stitching-with-opencv-and-python/
    ##on 2023/03/30
    '''
    
    #initialize stitcher and start stitching
    print("[INFO] stitching images...")
    stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
    (status, pano) = stitcher.stitch(images)
    print('status: ', status)

    # if the status is '0', then OpenCV successfully performed image stitching
    if status == 0:
            # write the output stitched image to disk
            cv2.imwrite(path + '/pics/pano.tif', stitched)

            # display the output stitched image to our screen
            cv2.imshow("Pano", pano)
            cv2.waitKey(0)

    # otherwise the stitching failed, likely due to not enough keypoints)
    # being detected
    else:
            print("[INFO] image stitching failed ({})".format(status))

'''
##homography algorithmus found on
##https://docs.opencv.org/3.4/d1/de0/tutorial_py_feature_homography.html
##on 2023/03/30
'''
print('[INFO] start feature extracting...')
MIN_MATCH_COUNT = 10
            
##initialize SIFT feature detection
sift = cv2.SIFT_create()

## find features in pano
kpPano, desPano = sift.detectAndCompute(pano, None)

##prepare flann
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

##initialize FLANN
flann = cv2.FlannBasedMatcher(index_params, search_params)

##for image in images:
if True:
    image = images[0]

    ##find features in image
    kp2, des2 = sift.detectAndCompute(image, None)
    
    ##find matches
    matches = flann.knnMatch(desPano,des2,k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)

    #condition: At least 10 good matches found
    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kpPano[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()
        h,w,f = pano.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)
        image = cv2.polylines(image,[np.int32(dst)],True,255,3, cv2.LINE_AA)
    else:
        print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
        matchesMask = None

    #draw inliers
    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                       singlePointColor = None,
                       matchesMask = matchesMask, # draw only inliers
                       flags = 2)
    img3 = cv2.drawMatches(pano,kpPano,image,kp2,good,None,**draw_params)
    plt.imshow(img3, 'gray')
    plt.show()


            

#'''


































'''
    
##################################################################################
##read and process files one by one
for file in docFiles:
    LatchUps = str2list(file, path) #get list of SEL
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

    #calculate frame location in image coordinates
    frame = GenFrame(width, height)

    try:
        writeImg(image, luLoc, pic, path, frame, FRAME, SEL)
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
