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

def ResizeCSV(path3, x, y, csv):
    DF = pd.read_csv(path3 + csv, header = None, sep = ';')
    NP = DF.to_numpy()
    h, w = NP.shape[:2]

    #get resized array, making sure that the smallest threshhold is used when several SEL
    #are mapped to the same pixel
    #NP1 = custom_resize2(arr = NP, zoom_factor_x = x, zoom_factor_y = y)
    NP1 = custom_binning_smallest_value(NP, x, y)
    return NP1

def custom_binning_smallest_value(original_array, scale_factor_x, scale_factor_y):
    new_shape = (int(original_array.shape[0] * scale_factor_x), int(original_array.shape[1] * scale_factor_y))
    resized_array = np.zeros(new_shape)
    
    for i_resized in range(new_shape[0]):
        for j_resized in range(new_shape[1]):
            # Calculate the corresponding region in the original array
            start_i_original = int(i_resized / scale_factor_x)
            end_i_original = int((i_resized + 1) / scale_factor_x)
            start_j_original = int(j_resized / scale_factor_y)
            end_j_original = int((j_resized + 1) / scale_factor_y)

            # Extract the region of original pixels that correspond to the current pixel in the resized array
            region = original_array[start_i_original:end_i_original, start_j_original:end_j_original]

            # Find the smallest value greater than 0 in the region
            if (region > 0).any():
                smallest_value = region[region > 0].min()
            else:
                smallest_value = 0

            # Assign the smallest value to the current pixel in the resized array
            resized_array[i_resized, j_resized] = smallest_value

    return resized_array

def ResizePic(path1, path2, picName, x, y):
    pic = cv2.imread(path1 + picName)
    height, width = pic.shape[:2]

    w = int(x * width)
    h = int(y * height)
    dim = (w, h)

    resized = cv2.resize(pic, dim, interpolation = cv2.INTER_AREA)

    cv2.imwrite(path2 + picName, resized)

