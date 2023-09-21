from fun3 import *

##get current path
path = os.getcwd()
print('current path: ', end = '')
print(path)

#get a list of all relevant txt Files and pitures
[docFiles, picFiles] = Files(path)

##read and process files one by one
iCnt = 0
for file in docFiles:
    #generate empty SEL MAP
    shape = (ADC, ADC, 3)
    array = np.full(shape, Black)
    array[0, :] = array[-1, :] = array[:, 0] = array[:, -1] = Blue

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

    #resize Image
    height = int(height*ResizeFactor)
    width = int(width*ResizeFactor)
    image = cv2.resize(image, (width, height),  interpolation=cv2.INTER_AREA)
   
    #calculate offset
    offsetX = (image.shape[0] - array.shape[0])//2
    offsetY = (image.shape[1] - array.shape[1])//2

    #overlay --> here only for frame
    #image[offsetX:offsetX + array.shape[0], offsetY : offsetY + array.shape[1]] = array
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            if np.all(array[i,j,:] == 0):
                continue #skip iteration

            image[offsetX + i, offsetY + j] = array[i,j]

    #save image
    p1 = path + '/img/empty/' + file + '_overlay.png'
    print(p1)
    cv2.imwrite(p1, image)

    iCnt+=1

