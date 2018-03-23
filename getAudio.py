import subprocess

command = "ffmpeg -i 3/IMG_4700.MOV -ab 160k -ac 2 -ar 44100 -vn 3/audiop2.wav"

subprocess.call(command, shell=True)
