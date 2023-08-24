from fun3 import *


#configuration
D4Col = False#True

##get current path
path = os.getcwd()
print('current path: ', end = '')
print(path)

#get a list of all relevant txt Files and pitures
[docFiles, picFiles] = Files(path)

##################################################################################
##read and process files one by one
iCnt = 0
for file in docFiles:
##    #generate empty SEL MAP
##    shape = (ADC, ADC, 3)
##    array = np.full(shape, Black)
##    array[0, :] = array[-1, :] = array[:, 0] = array[:, -1] = Blue

    #extract SEL location from file
    LatchUps = str2list(file, path)
    if len(LatchUps) == 0:
        continue #skip iteration
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

    #resize Image
    height = int(height*ResizeFactorY)
    width = int(width*ResizeFactorX)
    image = cv2.resize(image, (width, height),  interpolation=cv2.INTER_AREA)

    #generate empty SEL MAP
    shape = (ADC, ADC, 3)
    array = np.full(shape, Black)
    array[0, :] = array[-1, :] = array[:, 0] = array[:, -1] = Blue

    #get coordinates
    df = pd.DataFrame(LatchUps)
    try:
        df.drop(columns = [2, 3, 4], inplace = True)
        df = df.astype(int)

        #resize to fit image
        coord = df/scale
        coord = coord.astype(int
                             )
##        print('######')
##        print(coord.min())#0))
##        print(coord.max())
        coord.rename(columns = {1 : 'x', 0 : 'y'}, inplace = True)

        #mirror
        coord['x'] = -coord['x']
        coord['x'] += ADC -1

        #rotate
        coord['x'], coord['y'] = ADC - 1 - coord['y'], coord['x']
    except KeyError:
        pass

    #add SEL
    if not D4Col:
        for index, row in coord.iterrows():
            x,y = row[0], row[1]
            array[x-1,y-1] = Red
    else:
        for index, row in coord.iterrows():
            if row[1] > 4:
                x,y = row[0], row[1]
                array[x-1,y-1] = Red
##            else:
##                breakpoint()
        

    
    #calculate offset
    #// --> int(a/b)
    offsetX = (image.shape[0] - array.shape[0])//2
    offsetY = (image.shape[1] - array.shape[1])//2

    #overlay
    #image[offsetX:offsetX + array.shape[0], offsetY : offsetY + array.shape[1]] = array
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            if np.all(array[i,j,:] == 0):
                continue #skip iteration

            image[offsetX + i, offsetY + j] = array[i,j]

    
    p1 = path + '/img/' + file + '_overlay.png'
    print(p1)
    cv2.imwrite(p1, image)

    iCnt+=1

    
    

##    #calculate SEL location in image coordinates
##    luLoc = SEL_location(LatchUps, width, height)
##
##    #calculate frame location in image coordinates
##    frame = GenFrame(width, height)
##
##    #try:
##    if True:
##        writeImg(image, luLoc, pic, path, frame, FRAME, SEL)
####    except:
####        print('\tERROR GENERATING IMAGE FOR FILE: ', end = '')
####        print(file, end = '\n\n\n')
####        ErrorCnt += 1
####        ErrorList.append(file)
##
##if ErrorCnt == 0:
##    print('All images were created successfully.', end = '\n\n')
##else:
##    print('Image generation failed for following ', ErrorCnt, ' Files: ', end = '\n')
##    for i in ErrorList:
##        print('\t', end = '')
##        print(i, end = '\n')
