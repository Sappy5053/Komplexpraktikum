import cv2
import numpy as np
import os
from cvFun import *

path = os.getcwd()
img = cv2.imread(path + '/pics/pano_BU.tif')

[height, width] = img.shape[:2]

print('height, width = ', img.shape[:2])

diff = abs(int((width - height)/4))
w = int(width / 2)

genCanvas([diff, w])

bar = cv2.imread('canas0.png')

bar = np.delete(bar, range(1430), axis = 1)
bar = np.delete(bar, range(83), axis = 0)

print(bar.shape[:2])
img = np.vstack([img, bar])
img = np.vstack([bar, img])

path = path + '/pics/pano.tif'
cv2.imwrite(path, img)

##pixel = np.array([0, 0, 0])
##line = []
##
##for i in range(width):
##    line.append(pixel)
##
##line = np.array(line)
##
####print(img.shape[:2], line.shape[:2])
##bar = []
##for i in range(diff):
##    bar.append(line)
##bar = np.array(bar)
####    img = np.vstack([img, line])
##print(bar)
print(img.shape[:2])
##path = path + '/pics/pano1.tif'
##cv2.imwrite(path, bar)#img)
##






















##import numpy as np
##
##a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
##
##col = np.array([10, 11, 12])
##print(col , '\n\n')
##
##b = np.array(a)
##
##print(b, '\n\n')
##
##line = b[0]
##
##b = b[:-1]
##print(b, '\n\n')
##
####c = np.array([line])
##
##b = np.vstack([line, b])
##
##print(b, '\n\n')
##
##[height, width] = b.shape[:2]
##
##b = np.delete(b, width-1, 1)
##
##print(b, '\n\n')
##
##b = np.insert(arr = b, obj = 0, axis = 1, values = col)
####col.append(b)
##
##
##print(b, '\n\n')
