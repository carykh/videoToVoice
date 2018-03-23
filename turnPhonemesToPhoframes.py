import json

FOLDER_NAME = "3"

phonemeToIndex = {'silence':0}
file = open("/media/rob/Ma Book1/CS 230/videoToVoice/3/phonemes.json","r") 

parsed_json = json.loads(file.read())
words = parsed_json["words"]

frameCount = 132000 #(int)(17*30)
phoframes = [0] * frameCount

for word in words:
  if word["case"] == "success":
    wordText = word["alignedWord"]

    wordPointer = word["start"]
    for phonemes in word["phones"]:
      start = wordPointer
      end = wordPointer+phonemes["duration"]
      
      startFrame = (int)(start*(29.96835))
      endFrame = (int)(end*(29.96835))

      for frame in range(startFrame,endFrame):
        phoneme = phonemes["phone"].split("_")[0]
        if not phoneme in phonemeToIndex:
          phonemeToIndex[phoneme] = len(phonemeToIndex)
        phoframes[frame] = phonemeToIndex[phoneme] 

      wordPointer += phonemes["duration"]

f = open(FOLDER_NAME+'/key.txt','w')
for i in range(len(phonemeToIndex)):
  for j in phonemeToIndex:
    if(phonemeToIndex[j] == i):
      f.write(str(phonemeToIndex[j])+"\t"+str(j)+"\n")
f.close()

f = open(FOLDER_NAME+'/phoframes.txt','w')
for phoframe in phoframes:
  f.write(str(phoframe)+"\n")
f.close()
