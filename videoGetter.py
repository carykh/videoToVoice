import glob
import os
from contextlib import closing
from videosequence import VideoSequence
from PIL import Image
import subprocess

from pytube import YouTube

folderNumber = "2"

if not os.path.exists(folderNumber):
    os.makedirs(folderNumber)

print("BEGAN DOWNLOADING VIDEO")

YouTube('https://www.youtube.com/watch?v=_J7dEhYttbQ').streams.first().download(folderNumber)

print("FINISHED DOWNLOADING VIDEO")

list_of_files = glob.glob(folderNumber+'/*') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)

folderName = folderNumber+"/origImages"

if not os.path.exists(folderName):
    os.makedirs(folderName)

with closing(VideoSequence(latest_file)) as frames:
    for idx, frame in enumerate(frames[:]):
        filename = folderName+"/"+"frame{:06d}.jpg".format(idx)
        frame.save(filename)
        print("SAVED IMAGE #"+str(idx))

command = "ffmpeg -i "+latest_file+" -ab 160k -ac 2 -ar 44100 -vn "+folderNumber+"/audio.wav"

subprocess.call(command, shell=True)
