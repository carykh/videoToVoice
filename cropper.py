import numpy as np
from scipy import misc
import random
import math

for i in range(0,20):
    strIndex = str(i)
    while len(strIndex) < 6:
        strIndex = "0"+strIndex
    arr = misc.imread('2/origImages/frame'+strIndex+'.jpg')
    misc.imsave('2/croppedImages/frame'+strIndex+'.jpg',arr[180:540,384:896])
