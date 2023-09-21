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

    #extract SEL location from file
    LatchUps = str2list(file, path)
    if len(LatchUps) == 0:
        continue #skip iteration

    ##find picture that corresponds to current file
    fileNo = file[-10:-8]
    for p in picFiles:
        picNo = p[-6:-4]

        if picNo == fileNo:
            pic = p

    #open and resize image
    image, height, width = getImage(path, pic)

    #generate SEL map
    array = genSelMap(LatchUps)

    #overlay image and SEL map
    image = overlay(image, array)
    
    #save image
    p1 = path + '/img/' + file + '_overlay.png'
    print(p1)
    cv2.imwrite(p1, image)

    iCnt+=1
