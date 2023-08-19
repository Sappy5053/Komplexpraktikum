import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

def Itegrate(lowerLim, upperLim, arr):
    #find positions
    a = True
    UL = arr.shape[0]
    for i in range(arr.shape[0]):
        if (arr[i, 0] > lowerLim) and a:
            a = False
            LL = i
        elif (arr[i, 0] > upperLim):# and a:
##            print(i)
            UL = i
            break
    s = 0
    for i in range(LL,UL):
        s += arr[i,1]
    return s
    

path = os.getcwd()
csv_files = [f for f in os.listdir(".") if f.endswith('.csv')]

for csv in csv_files:
    df = pd.read_csv(csv, sep=';')

    NP = df.to_numpy()
##    print(NP.max())

    #1433.87    280
    s = Itegrate(0, 1433.87, NP)
    print(csv, s)


    
