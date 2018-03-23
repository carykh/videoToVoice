import glob
import os
from contextlib import closing
from videosequence import VideoSequence
from PIL import Image
import subprocess

from pytube import YouTube

folderNumber = "2"

folderName = folderNumber+"/origImages"

latest_file = folderNumber+"/\"My children dont exist.mp4\""

if not os.path.exists(folderName):
    os.makedirs(folderName)
"""
with closing(VideoSequence(latest_file)) as frames:
    for idx, frame in enumerate(frames[:]):
        if idx >= 12950:
            filename = folderName+"/"+"frame{:06d}.jpg".format(idx)
            frame.save(filename)
        print("SAVED IMAGE #"+str(idx))

"""

command = "ffmpeg -i "+latest_file+" -ab 160k -ac 2 -ar 44100 -vn "+folderNumber+"/audio.wav"

subprocess.call(command, shell=True)
