#
import cv2
import pandas as pd
import numpy as np



def delete_n_following_values(df, value_to_find, n):
    i = 0
    while i < len(df):
        if df.iloc[i][2] == value_to_find:
            try:
##                print(i)
##                df.drop(index=range(i+1, i+n+1), inplace=True)
                for j in range(n):
                    df.iloc[j][2] = 0
                i += n
                #df.reset_index()#drop=True)
            except KeyError:
                pass
        i += 1
    return df.reset_index(drop=True)

df = pd.read_csv('micfs35.dat.txt', sep = '\t', header = None)

##df.to_csv('test.csv')
df.drop(columns = [3, 4], inplace = True)
df = df.astype(int)

##print(df.head())
print('#####')
print(df.shape)
df1 = df[df[2] == 4]
print(df1.shape)
df = delete_n_following_values(df, 4, 10)
print(df.shape)
df1 = df[df[2] == 4]
print(df1.shape)

df = df[df[2] == 4]
print(df.head())
df.drop(columns = [2], inplace = True)

df = df/34.4
df = df.astype(int)



print(df.head())

arr = np.zeros((120, 120))

for index, row in df.iterrows():
    x,y = row[0], row[1]
    arr[x-1,y-1] = 255

cv2.imwrite(doc+ '.png', arr)









