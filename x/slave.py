#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
 
import speech_recognition as sr
from fuzzywuzzy	import fuzz
from time import ctime
import time
import os
from subprocess import Popen
from gtts import gTTS
import sys
import pyjokes
import SR
import sys
#stderr = open('slave.log', 'w')
#sys.stderr = stderr
devnull = open(os.devnull, 'w')
browser = "google-chrome"
web = 0
say = 1
run = 2
exe = 3
fun = 4
cti = ctime()
#joke = pyjokes.get_joke()

cmds = {
	"amazon"    : (web, "http://amazon.co.uk/"),
	"calculator": (run, "galculator"),
	"chess"     : (run, "xboard"),
	"commands"  : (exe, "xxx"),
	"dictation" : (web, "https://dictation.io/"),
        "files"     : (run, "pcmanfm"),
	"google"    : (web, "https://www.google.co.uk/#q="),
        "joke"      : (exe, pyjokes.get_joke),
        "map"       : (web, "https://google.co.uk/maps/place/"),
	"meaning"   : (say, "42"),
        "music"     : (web, "https://www.youtube.com/watch?v=ViIx5uagasY&list=PL-MQ2wS-IPhApRRjqilUit2xBXfH0Li8y"),
	"name"	    : (say, "My name is Juniper Kate."),
        "news"      : (web, "https://news.google.co.uk/"),
        "pinball"   : (run, "pinball"),
        "reddit"    : (web, "https://www.reddit.com/"),
	"rhythmbox" : (run, "rhythmbox"),
        "stop"      : (exe, sys.exit),
        "time"      : (exe, ctime),
        "wikipedia" : (web, "https://www.wikiwand.com/en/"),
        "youtube"   : (web, "https://www.youtube.com/")
	} 
cmdstr = ''
for key in sorted(cmds.keys()):
	cmdstr += key + ", "
cmds["commands"] = cmdstr
print("Welcome to My Master's Voice! Please speak one of the following commands:", cmdstr)

keygen = [(key,0.1) for key in cmds.keys()]
print (keygen)

def speak(text):
	print(">", text)
#	tts = gTTS(text=text, lang='en')
#	tts.save("audio.mp3")
#	Popen(["mpg321", "audio.mp3"], stdout=devnull, stderr=devnull)

def nearest_word(word, words):
	max = 0
	for w in words:
		d = fuzz.ratio(w, word)
		if d > max:
			new = w
			max = d
	return (new, max)

r = sr.Recognizer()
#r.energy_threshold = 2

while True:
	speak("Alan, what do you want me to do?")

	# Record Audio
	with sr.Microphone() as source:
		
		print("Say something!")
		r.adjust_for_ambient_noise(source)
		audio = r.listen(source)

#	text = SR.getSpeechText(r, sr, audio)
	text = (r.recognize_sphinx(audio, keyword_entries = keygen))
#	text = r.recognize_sphinx(audio)
	if text is None or len(text) < 3:
		speak("Sorry, I didn't understand!")
		continue

	print("<", text)
	text = text.lower()
	words = text.split()
	w = words[0]
	if w not in cmds:
		(new, d) = nearest_word(w, cmds.keys())
		if d > 66:
			w = new
			speak("Correcting to " + w)
	if w not in cmds:
		max = 0
		for word in words:
			(alt, d) = nearest_word(word, cmds.keys())
			if d > max:
				new = alt
				max = d
		if max > 66:
			w = new
			speak(w)
	if w in cmds:
		t = cmds[w][0]
		p = cmds[w][1]
		if t == web:
			for i in range(1,len(words)):
				p += words[i]+' '
			Popen([browser, p])

		elif t == say:
			speak(p)

		elif t == exe:
			speak(p())

		elif t == fun:
			p()
		
		elif t == run:
			Popen(p)
	else:
		try:
			Popen(text)
		except FileNotFoundError:
			speak("I don't know, really I don't. Sorry")
