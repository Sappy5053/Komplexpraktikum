import cv2
import os
import pandas as pd
import numpy as np
from scipy.ndimage import zoom


def BinningFactors(path1, path2):
    print(path1, path2)
    #open open Pano from GSI experiment
    P1 = cv2.imread(path1)
    P1Height, P1Width = P1.shape[:2]
    print('GSI: ',P1.shape[:2])

    #open Lunte Pano
    P2 = cv2.imread(path2)
    P2Height, P2Width = P2.shape[:2]
    print('LUNTE: ',P2.shape[:2])

    #calculate factors
    xFac = P1Width/P2Width
    yFac = P1Height/P2Height
    return [xFac, yFac]#P2Resized

def ResizeCSV(path3, x, y):
    DF = pd.read_csv(path3 + csv, header = None, sep = ';')
    NP = DF.to_numpy()
    h, w = NP.shape[:2]

    #get resized array, making sure that the smallest threshhold is used when several SEL
    #are mapped to the same pixel
    NP1 = custom_resize2(arr = NP, zoom_factor_x = x, zoom_factor_y = y)
    return NP1


def custom_resize(arr, zoom_factor_x, zoom_factor_y):
    # Identify the positions of non-zero elements in the original array
    non_zero_positions = np.transpose(np.nonzero(arr))

    # Calculate the shape of the resized array
    new_shape = (int(arr.shape[0]*zoom_factor_x), int(arr.shape[1]*zoom_factor_y))

    # Create a new array of zeros with the calculated shape
    resized_arr = np.zeros(new_shape, dtype=arr.dtype)

    # Create a 2D list to store the values that map to each position
    value_list = [[[] for _ in range(new_shape[1])] for _ in range(new_shape[0])]

    # Calculate the new positions of the non-zero elements
    new_positions = non_zero_positions * [zoom_factor_x, zoom_factor_y]
    new_positions = new_positions.astype(int)

    # Ensure the new positions are within the bounds of the resized array
    new_positions = np.clip(new_positions, 0, np.array(resized_arr.shape) - 1)

    # Set the values at the new positions in the resized array to the values
    # of the non-zero elements in the original array and add the values to
    # the corresponding lists in value_list
    for old, new in zip(non_zero_positions, new_positions):
        #resized_arr[tuple(new)] = arr[tuple(old)]
        value_list[new[0]][new[1]].append(arr[tuple(old)])

    return resized_arr, value_list

def custom_resize2(arr, zoom_factor_x, zoom_factor_y):
    #wrapper around custom resize
    newArr, value_list = custom_resize(arr, zoom_factor_x, zoom_factor_y)
    subArr = np.zeros_like(newArr)

    shape = newArr.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            #retrieve elements from array and list
            arrE  = newArr[i, j]
            listE = value_list[i][j]
            #arrE  = int(arrE)

            #check if listelement is empty
            if bool(listE):
                #not empty
##                print('1', listE)
                minimum = int(min(listE))
            else:
                #empty
                #print('2', listE)
                minimum = 0
                

            #write minimum to substitute Array
            subArr[i, j] = minimum

    return subArr

def ResizePic(path1, path2, picName, x, y):
    pic = cv2.imread(path1 + picName)
    height, width = pic.shape[:2]

    w = int(x * width)
    h = int(y * height)
    dim = (w, h)

    resized = cv2.resize(pic, dim, interpolation = cv2.INTER_AREA)

    cv2.imwrite(path2 + picName, resized)

