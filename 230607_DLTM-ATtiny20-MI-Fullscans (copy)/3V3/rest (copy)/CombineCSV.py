import os
import pandas as pd

def emptyRow(l):
    row = []
    for i in range(l):
        row.append('0;')
    row = row[:-1]

path = os.getcwd()

path1 = path + '/csv/resized/cropped/'

List = os.listdir(path1)

#get input documents
for i in range(len(List)):
    print(i, ':\t', List[i])

print()
UserInput = input('Choose the number corresponding to the files you want to join from left to right (Format: 1,3,2)\n')

#process User Input
j = 0
num = []
for i in range(len(UserInput)):
    if UserInput[i] == ',':  
        n = int(UserInput[j:i])
        j = i+1
        num.append(n)

n = int(UserInput[j:])
num.append(n)

#open Files
with open(path1 + List[num[0]], 'r') as file:
    left   = file.readlines()
##    left   = left + ';'

with open(path1 + List[num[1]], 'r') as file:
    middle = file.readlines()
##    middle = middle + ';'

with open(path1 + List[num[2]], 'r') as file:
    right  = file.readlines()


#get neccessary information on docs
lenths = [len(left), len(middle), len(right)]
lenths.sort()
j = lenths[-1]

ln = num[0]
mn = num[1]
rn = num[2]

print(path1 + List[ln])
print(path1 + List[mn])
print(path1 + List[rn])

DF_left   = pd.read_csv(path1 + List[ln])
DF_middle = pd.read_csv(path1 + List[mn])
DF_right  = pd.read_csv(path1 + List[rn])

l_col = DF_left.shape[0]
m_col = DF_middle.shape[0]
r_col = DF_right.shape[0]

##generate empty row
l_row = emptyRow(l_col)
m_row = emptyRow(m_col)
r_row = emptyRow(r_col)


NewCSV = []

#combine documents by appending rows
for i in range(j):
    #get row
    try:
        l = left[i]
        l = l[:-1]
    except:
        l = l_row

    try:
        m = middle[i]
        m = m[:-1]
        
    except:
        m = m_row

    try:
        r = right[i]
    except:
        r = r_row
    
    #combine rows
    try:
        NewCSV.append(l+';'+m+';'+r)
    except:
        print(i)

#save to file
with open(path1 + 'NewCSV.csv', 'w') as file:
    for row in NewCSV:
        #row = row + '\n'
        file.write(row)
