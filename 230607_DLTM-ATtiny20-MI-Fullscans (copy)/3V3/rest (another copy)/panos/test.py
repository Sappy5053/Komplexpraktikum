import cv2

LUNTE  = '20230606-DLTM-ATtiny20_thr.png'
LUNTE1 = '20230606-DLTM-ATtiny20_thr_small.png'
GSI    = 'GSI_Pano_small.png'

LUNTE   = cv2.imread(LUNTE)
GSI     = cv2.imread(GSI)

shape = (472, 472)
print(shape)

LUNTE = cv2.resize(LUNTE, shape)

cv2.imwrite(LUNTE1, LUNTE)
