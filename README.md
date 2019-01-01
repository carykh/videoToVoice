# videoToVoice

to install the dependencies using pip use requirements.txt file:

```
pip install -r requirements.txt
```

tensorflow might fail to install if you are using an incompatible version of python (python 3.7 as of the time of writing)
in which case you might have to install it manually

the scripts also depend on ffmpeg being installed for video and audio conversions


These files take in a sequence of lip images, and predict the phonemes being said.

pyTubeTest.py takes in a YouTube URL, downloads that video onto the computer, turns the video into an image sequence, tries to find faces in the images, and also extracts the audio from the video and saves that, too. Earlier, we tried to get pyTubeTest.py to also convert the audio into spectrograms with ARSS in the same code, but that just didn’t work because all the libraries required for the first steps only work in Ubuntu, and ARSS only works in Windows.

pyTubeShort.py does the same thing as pyTubeTest.py, but doesn't download the video from YouTube. Instead, it just takes a file from a file directory.

getAudio.py takes in a video file, and saves the audio from that video into a new file.

audioStitcher.py is very simple: it just takes in two audio files, stitches them together, and saves the result.

lipTester.py takes in a sequence of images of faces, and crops each one so that the new folder of images only shows the speaker's lips. (And a margin of 25 pixels or so.)

turnPhonemesToPhoframes.py takes the JSON output the Gentle creates. (This is a time-aligned transcript of what was spoken in the video: e.g., when I said the Bee Movie script, this JSON file has the timestamps at which I said every phoneme of the movie.) Then, it turns that JSON file into phoframes.txt, a text file listing what phoneme is said at every video frame (1/30th of a second)

key.txt tells us what number corresponds with what phoneme, so we can read phoframes.txt more easily!

phoframes.txt tells us what phoneme is being said at every frame of the video. This is the ground truth. And every value is a number, which can be converted back into a phoneme, using key.txt.

phoframeTrain.py creates the neural network architecture, and trains it on processed data. (Note: this code describes the neural network architecture in the most detail.)

phoframeTest.py takes in a pre-trained model, and a sequence of silent images, and generates a text file predicting what phonemes should go along with said video.

rainingDataVisualizer.py

OUTDATED FILES

imageTest.py was an experimental dumping ground of how to use PIL, which I don't think I ended up using.

dump.py is where I tested helper functions such as the spectrogram-smoother, and video-frame-accesser.

faceReadTest.py is where I tested the face recognition library installed from online. It ended up working, but it snaps to the nearest ~30 pixels for some reason, so we decided not to use it for now.

cropper.py crops an image to only show the middle section (middle 40% horizontally and middle 50% vertically), although this is only used for explanation purposes (train.py has a cropping function within it.)

videoGetter.py was a short script we used to extract all the images from a downloaded YouTube video when pyTubeTest.py crashed for some reason.

videoContinue.py is videoGetter’s sequel and does the same thing, but starts in the middle.

trainingDataVisualizer.py was my first attempt at making the pretty bar graphs that show the NN's prediction of phonemes at each frame. The new and improved version is the .pde file.
