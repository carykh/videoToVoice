import face_recognition
import subprocess

image = face_recognition.load_image_file("2/origImages/frame0000.jpg")

face_locations = face_recognition.face_locations(image)

if(len(face_locations) == 1):
    top, right, bottom, left = face_locations[0]
    faceFilename = faceFolderName+"/"+"frame{:04d}.jpg".format(0)
    height = top-bottom
    faceFrame = frame.crop((left,top,right,bottom-height*0.3))
    faceFrame.save(faceFilename)
