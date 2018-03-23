import tensorflow as tf
import numpy as np
from scipy import misc
import random
import math
import os

FOLDER_SAVE_NAME = "3"



w = 400
h = 250

phoframeFile = open("/media/rob/Ma Book1/CS 230/videoToVoice/3/phoframes.txt","r") 

phoframes = phoframeFile.read().split("\n")

keyFile = open("/media/rob/Ma Book1/CS 230/videoToVoice/3/key.txt","r") 

key = keyFile.read().split("\n")

for i in range(0,200):
  strIndex = str(i)
  while len(strIndex) < 6:
    strIndex = "0"+strIndex
  newImage = misc.imread('3/mouthImages/frame'+strIndex+'.jpg')
  s = newImage.shape;


  imageToSave = np.zeros([h,w,3])
  imageToSave[0:s[0],0:s[1],0:3] = newImage
  misc.imsave(FOLDER_SAVE_NAME+"/lineupCheck/sample"+str(i)+'.png',imageToSave)
  
  

  
