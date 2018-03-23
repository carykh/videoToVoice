import face_recognition
from scipy import misc
margin = 25
maxWidth = 0
maxHeight = 0

# frames with my hand in front of my mouth
# 3197 - 3224


for i in range(0,131663):
    strIndex = str(i)
    while len(strIndex) < 4:
        strIndex = "0"+strIndex

    image = face_recognition.load_image_file("/media/rob/Ma Book1/CS 230/videoToVoice/3/origImages/frame"+strIndex+".jpg")
    face_landmarks_list = face_recognition.face_landmarks(image)

    if(len(face_landmarks_list) >= 1):
        xMin = 999999
        xMax = -999999
        yMin = 999999
        yMax = -999999
        
        points = face_landmarks_list[0]['bottom_lip']+face_landmarks_list[0]['top_lip']
        
        for point in points:
            if point[0] < xMin:
                xMin = point[0]
            if point[0] > xMax:
                xMax = point[0]
            if point[1] < yMin:
                yMin = point[1]
            if point[1] > yMax:
                yMax = point[1]

        if(yMax-yMin > maxHeight):
            maxHeight = yMax-yMin

        if(xMax-xMin > maxWidth):
            maxWidth = xMax-xMin

        arr = misc.imread("3/origImages/frame"+strIndex+".jpg")
        misc.imsave("3/mouthImages/frame"+strIndex+".jpg",arr[yMin-margin:yMax+margin,xMin-margin:xMax+margin])
        print("FINISHED IMAGE #"+str(i)+". Also, the maximum dimensions are "+str(maxWidth)+" x "+str(maxHeight))
