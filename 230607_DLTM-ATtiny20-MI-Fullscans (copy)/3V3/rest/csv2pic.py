import numpy as np
import pandas as pd
import os
import cv2

maxVal = 4000
maxGray = 255

path = os.getcwd()
path = path+ '/csv/'#resized/'

files = os.listdir(path)

for i in range(len(files)):
    print(i, ': ', files[i]) 

ui = int(input('number:'))

file = path + files[ui]
print(file)

df = pd.read_csv(file, sep = ';')

arr = df.to_numpy()

for i in range(arr.shape[0]):
    #row
    for j in range(arr.shape[1]):
        #column
        v = int(arr[i, j])
        v = int((v/maxVal)*maxGray)
        arr[i, j] = v

##scipy.misc.toimage(arr, 
cv2.imwrite(path+'img.png', arr)

