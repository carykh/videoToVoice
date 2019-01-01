import glob
import os
from contextlib import closing
from videosequence import VideoSequence
from PIL import Image
import face_recognition
import subprocess

from pytube import YouTube

folderNumber = "3"

if not os.path.exists(folderNumber):
    os.makedirs(folderNumber)

YouTube('https://www.youtube.com/watch?v=0bdHdGS3OlI').streams.first().download(folderNumber)

list_of_files = glob.glob(folderNumber+'/*') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)

folderName = folderNumber+"/origImages"
faceFolderName = folderNumber+"/faceImages"

if not os.path.exists(folderName):
    os.makedirs(folderName)

if not os.path.exists(faceFolderName):
    os.makedirs(faceFolderName)

with closing(VideoSequence(latest_file)) as frames:
    for idx, frame in enumerate(frames[:]):
        filename = folderName+"/"+"frame{:04d}.jpg".format(idx)
        frame.save(filename)

        # Load the jpg file into a numpy array
        image = face_recognition.load_image_file(filename)

        # Find all the faces in the image using the default HOG-based model.
        # This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
        # See also: find_faces_in_picture_cnn.py
        face_locations = face_recognition.face_locations(image)

        if(len(face_locations) == 1):
            top, right, bottom, left = face_locations[0]
            faceFilename = faceFolderName+"/"+"frame{:04d}.jpg".format(idx)
            height = top-bottom
            faceFrame = frame.crop((left,top,right,bottom-height*0.3))
            faceFrame.save(faceFilename)

subprocess.run(["ffmpeg", "-i", latest_file, "-ab", "160k", "-ac", "2", "-ar", "44100", "-vn", folderNumber+"/audio.wav"])
