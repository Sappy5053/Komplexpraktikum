import numpy as np
import pandas as pd
import os, cv2

minVal = 0
maxVal = 4000

path = os.getcwd()
path1 = path + '/csv/resized/'
path2 = path + '/csv/'
path = path2
##def genImg(path):
files = os.listdir(path)

##print(files)
for file in files:
    try:
        breakpoint()
        df = pd.read_csv(path+file, sep = ';')
        df = df.astype(int)
        NP = df.to_numpy()
        
        #normalize
        NP[NP > 0] = 255
        
        img = path+file[:-4]+'.png'
        print(img)
        cv2.imwrite(img, NP)

    except pd.errors.ParserError:
        pass
    except IsADirectoryError:
        pass
##        except UnicodeDecodeError:
##            img = path+file[:-4]+'.png'
##            print('ERROR#####', img)
    


