import cv2, os
import numpy as np
import pandas as pd

RED = np.array([0, 0, 255])
IMPULSE = 4000

cwd = os.getcwd()
path = cwd + '/panos/'

List = os.listdir(path)

for i in range(len(List)):
    print(i, ':\t', List[i])

print()

UserInput = input('Choose the number corresponding to the panorama you want to convert to csv \n')

file = List[int(UserInput)]

FilePath = path + file

pano = cv2.imread(FilePath)
h, w = pano.shape[:2]
print(h,w)

csv = []
SEL_CNT = 0
for r in range(w):
    row = []
    for c in range(h):
        pixel = pano[c, r]
        if np.array_equal(pixel, RED):#pixel == RED:
            row.append(IMPULSE)
            SEL_CNT += 1
        else:
            row.append(0)
    csv.append(row)

DF_CSV = pd.DataFrame(csv)
path = path + 'GSI.csv'
DF_CSV.to_csv(path, sep = ';', header = False, index = False)
##print(DF_CSV.head())
##loc = np.where(pano == RED)

print('SEL found: ', SEL_CNT)





