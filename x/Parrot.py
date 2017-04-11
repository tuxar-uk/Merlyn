#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
from subprocess import Popen
from os import devnull
from gtts import gTTS

ignore = open(devnull, 'w')

def speak(text):
    print(">", text)
    tts = gTTS(text=text, lang='en')
    tts.save("audio.mp3")
    Popen(["mpg321", "audio.mp3"], stdout=ignore, stderr=ignore) 

r = sr.Recognizer()
with sr.Microphone() as source:
    
    while True:
        print("Say something!")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        print("I heard you say:")
        
# recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print("(waiting for Google)")
            text = r.recognize_google(audio)
            
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            continue
        
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            continue
        
        if text.lower() == "stop": break
        
        speak(text)
        
       