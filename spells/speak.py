#!/opt/anaconda3/bin/python

from os import devnull
from sys import stdin, exit
from subprocess import Popen
from gtts import gTTS

text = str(stdin.readline().strip())
print(">", text)

tts = gTTS(text=text, lang='en')
tts.save("/tmp/speak.mp3")
Popen(["mpg321", "/tmp/speak.mp3"])
# stdout=devnull, stderr=devnull)
