import numpy as np
import pandas as pd
import cv2

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

def compArea(arr, arr2):
    #calculate relative latchup area
    iCnt  = 0
    iCnt2 = 0

##    original
    for x in np.nditer(arr):
        if x > 0:
            iCnt += 1

    ##resized
    for x in np.nditer(arr2):
        if x > 0:
            iCnt2 += 1

    relArea = iCnt/arr.size
    relArea2 = iCnt2/arr2.size

    print('original: ', relArea)
    print('resized: ', relArea2)

    return relArea, relArea2



#File Used: 20230606-124422_t.csv
path = '20230606-124422_t.csv'#'/home/thomas/Documents/KP_schmidt/230607_DLTM-ATtiny20-MI-Fullscans (copy)/3V3/rest/csv/20230606-124422_t.csv'

df = pd.read_csv(path, header = None, sep = ';')
arr = df.to_numpy()

#Factors: x: 0.8266033254156769 , y: 0.7913486005089059
x = 0.8266033254156769
y = 0.7913486005089059

arr2 = custom_binning_smallest_value(arr, x, y)

compArea(arr, arr2)

##output:
##original:  0.014004811633939492
##resized:   0.014512083097795364
## --> Auf beiden Bildern sind ca. 1.4% der Fäche als SEL erkannt

cv2.imwrite('img0.png', arr)
cv2.imwrite('img1.png', arr2)
    


