import numpy as np
from scipy import misc

INSPEC_WIDTH = 240 # 2 seconds
INSPEC_HEIGHT = 368

def readAndClipImage(i):
    if i < 0 or i > 90:
        return np.zeros((INSPEC_HEIGHT,INSPEC_WIDTH,1))
    arr = misc.imread('2/audioSnippets/'+str(i)+'.jpg')
    if i == 0: 
        return arr[:,:]
    elif i == 90:
        return arr[:,120:]
    else:
        return arr[:,120:]


def getSpecAtFrame(f,w):
    specIndex = (f // 300)

    arr = np.zeros((INSPEC_HEIGHT,INSPEC_WIDTH))

    specImageFile = readAndClipImage(specIndex)
    prevSpecImageFile = readAndClipImage(specIndex-1)

    mod = frameIndex%300

    if mod < w: # The previous 2 seconds is going to bleed into the previous section
        seamSpot = (w-mod)*4
        arr[:,seamSpot:] = specImageFile[:,0:mod*4,0]
        arr[:,:seamSpot] = prevSpecImageFile[:,1200-seamSpot:1200,0]
        for col in range(seamSpot,min(seamSpot+w,INSPEC_WIDTH)): #60-pixel smoothing between one portion and the next, cuz I'm fancy.
	    sFrom = prevSpecImageFile[:,1200+col-seamSpot,0]
	    sTo = specImageFile[:,col-seamSpot,0]
	    prog = (col-seamSpot)/60.0
	    arr[:,col] = sFrom+(sTo-sFrom)*prog
    else:
	arr = specImageFile[:,(mod-w)*4:mod*4,0]
    return np.asarray(arr)/255.0

def getInSpecAtFrame(f):
    return getSpecAtFrame(f,60)

def getOutSpecAtFrame(f):
    return getSpecAtFrame(f+2,2)


frameIndex = 5125

misc.imsave('dump9.png',getOutSpecAtFrame(frameIndex))

