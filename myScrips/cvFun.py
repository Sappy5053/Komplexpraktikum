import numpy as np
from matplotlib import pyplot as plt
import cv2
##import imutils


kpPano = None
desPano = None
FLANN_INDEX_KDTREE = 1
index_params = None
search_params = None
sift = None
flann = None
MIN_MATCH_COUNT = 10
pano = None

img = None



def getPano(path, images, panoExists):
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
            cv2.imwrite(path + '/pics/pano.tif', pano)

            # display the output stitched image to our screen
##            cv2.imshow("Pano", pano)
##            cv2.waitKey(0)

        # otherwise the stitching failed, likely due to not enough keypoints)
        # being detected
        else:
            print("[INFO] image stitching failed ({})".format(status))
    return pano      

def prepareMatching(pano1):
    '''
    ##homography algorithmus found on
    ##https://docs.opencv.org/3.4/d1/de0/tutorial_py_feature_homography.html
    ##on 2023/03/30
    '''
    global kpPano 
    global desPano 
    global FLANN_INDEX_KDTREE 
    global index_params 
    global search_params
    global sift
    global flann
    global pano
    global MIN_MATCH_COUNT

    pano = pano1

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


def getHomography(image, SHOW_INLIERS):
    '''
    ##homography algorithmus found on
    ##https://docs.opencv.org/3.4/d1/de0/tutorial_py_feature_homography.html
    ##on 2023/03/30
    '''
    global kpPano 
    global desPano 
    global FLANN_INDEX_KDTREE 
    global index_params 
    global search_params
    global sift
    global flann
    global pano
    global MIN_MATCH_COUNT

    
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
##        print('pts', pts)
        image = cv2.polylines(image,[np.int32(dst)],True,255,3, cv2.LINE_AA)
    else:
        print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
        matchesMask = None
    if SHOW_INLIERS:
        #draw inliers
        draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                           singlePointColor = None,
                           matchesMask = matchesMask, # draw only inliers
                           flags = 2)
        img3 = cv2.drawMatches(pano,kpPano,image,kp2,good,None,**draw_params)
        plt.imshow(img3, 'gray')
        plt.show()
    return [M, pts]


def transformPerspective(M, mask):
    global pano

    matchesMask = mask.ravel().tolist()
    h,w,f = pano.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)

    return dst


def genCanvas(dim):
    global img

    height = dim[0]
    width = dim[1]
    
    pixel = np.array([0, 0, 0])

    w = 2*width
    h = 2*height
    line = []
    img = []

    for i in range(w):
        line.append(pixel)
    line = np.array(line)

    for i in range(h):
        img.append(line)
    img = np.array(img)

##    return img
    #printImg('canas0.png')
##    print(img)
    


def AddCorners(array, panoDim):
    global img

    height = panoDim[0]
    width = panoDim[1]
    
    pix = np.array([255, 255, 255])

    for pixel in array:
        x = pixel[0] + width
        y = pixel[1] + height

        img[int(y)][int(x)] = pix



def printImg(path):
    global img
    cv2.imwrite(path, img)

def correctPos():
    global img

    [height, width] = img.shape[:2]

    #rotate
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    #flip around y-axis
    img = cv2.flip(img, 1)

    #move by 1 pxl down
    pixel = np.array([0, 0, 0])
    line = img[0] #get empty line
##    line = np.append(arr = line, values = pixel)
    line = np.array([line])
##    line = np.transpose(line)
    img = img[:-1] #delete last line

    print(img.shape[:2], line.shape[:2])
    img = np.vstack([line, img]) #add new line to top

    #move one pixel right
    pixel = np.array([0, 0, 0])
    col = []
    for i in range(height):
        col.append(pixel)
    col = np.array(col)
    
    img = np.delete(img, width-1, 1)
    img = np.insert(arr = img, obj = 0, axis = 1, values = col)

    

    
        
    

    














        
