import numpy as np
import cv2

path = '/home/thomas/Documents/KP_schmidt/myScrips/pics/Area/'

image = cv2.imread(path + 'area_stitch.tif')

height, width = image.shape[:2]

# delete all but red channel
for y in range(height-1):
    for x in range(width-1):
        pixel = image[y][x]
        b = int(pixel[0] / 1.2)
        g = int(pixel[1] / 1.2)
        r = pixel[-1]
        if g > 80:
            r = 0
            b = 0
        else:
            g = 0
        pixel = [b, g, r]
        image[y][x] = pixel

cv2.imwrite(path + 'green.tif', image)