#!/usr/bin/env python3
#https://www.soundbytesolutions.co.uk/word-lists/ab-short-word-list/

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
import editdistance
import time

def SphinxSpeech(r, sr, audio):
	# recognize speech using Sphinx
	try:
		return r.recognize_sphinx(audio)
	except sr.UnknownValueError:
		print("Sphinx could not understand audio")
	except sr.RequestError as e:
		print("Sphinx error; {0}".format(e))
	return	None

def GoogleSpeech(r, sr, audio):
	
	# recognize speech using Google Speech Recognition
	try:
		# for testing purposes, we're just using the default API key
		# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
		# instead of `r.recognize_google(audio)`
		return	r.recognize_google(audio)
	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))
	return	None

def GoogleCloud(r, sr, audio):
	# recognize speech using Google Cloud Speech
	GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""INSERT THE CONTENTS OF THE GOOGLE CLOUD SPEECH JSON CREDENTIALS FILE HERE"""
	try:
		return r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
	except sr.UnknownValueError:
		print("Google Cloud Speech could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Google Cloud Speech service; {0}".format(e))
	return	None

def WitSpeech(r, sr, audio):
	# recognize speech using Wit.ai
#	WIT_AI_KEY = "INSERT WIT.AI API KEY HERE" # Wit.ai keys are 32-character uppercase alphanumeric strings
	WIT_AI_KEY = "SARSQHBPBKHXEQDSIRIO7ARA2BWWVPPN"
	try:
		return	r.recognize_wit(audio, key=WIT_AI_KEY)
	except sr.UnknownValueError:
		print("Wit.ai could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Wit.ai service; {0}".format(e))
	return	None

def BingSpeech(r, sr, audio):
	# recognize speech using Microsoft Bing Voice Recognition
#	BING_KEY = "INSERT BING API KEY HERE" # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
	BING_KEY = "11081df47aef44529d3b39ec57aee1f6"
	try:
		text = r.recognize_bing(audio, key=BING_KEY)
	except sr.UnknownValueError:
		print("Microsoft Bing Voice Recognition could not understand audio")
		return None
	except sr.RequestError as e:
		print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
		return None
	else:	return text

def HoundifySpeech(r, sr, audio):
	# recognize speech using Houndify
#	HOUNDIFY_CLIENT_ID = "INSERT HOUNDIFY CLIENT ID HERE" # Houndify client IDs are Base64-encoded strings
	HOUNDIFY_CLIENT_ID = "h9uKTtJof9J4lzddl_1MKw=="
#	HOUNDIFY_CLIENT_KEY = "INSERT HOUNDIFY CLIENT KEY HERE" # Houndify client keys are Base64-encoded strings
	HOUNDIFY_CLIENT_KEY = "foFeO2DecGloV-CpSNnUZrmW1wAhLZl8b-VkQZSccHYj3MjtmelaVxa25UTujStGc70DZhFU5B94tw3r4_djpw=="
	try:
		text = r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY)
	except sr.UnknownValueError:
		print("Houndify could not understand audio")
		return None
	except sr.RequestError as e:
		print("Could not request results from Houndify service; {0}".format(e))
		return None
	else:	return text

def IBMSpeech(r, sr, audio):
	# recognize speech using IBM Speech to Text
#	IBM_USERNAME = "INSERT IBM SPEECH TO TEXT USERNAME HERE" # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
	IBM_USERNAME = "2f4e9ae0-cb84-4a77-8349-3abd2d99a874"
#	IBM_PASSWORD = "INSERT IBM SPEECH TO TEXT PASSWORD HERE" # IBM Speech to Text passwords are mixed-case alphanumeric strings
	IBM_PASSWORD = "NCpJLDZ5CZ83"
	try:
		return	r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD)
	except sr.UnknownValueError:
		print("IBM Speech to Text could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from IBM Speech to Text service; {0}".format(e))
	return	None

def getSpeechText(r, sr, audio):
	
	text = BingSpeech(r, sr, audio)
	if text is not None: return text
	text = HoundifySpeech(r, sr, audio)
	if text is not None: return text
	
if __name__ == "__main__":
    # execute only if run as a script

	speechEngines = {
		"Bing"	:	BingSpeech,
		"Hound"	:	HoundifySpeech,
		"IBM"	:	IBMSpeech,
		"Sphinx":	SphinxSpeech,
#		"Google":	GoogleSpeech,
		"Cloud"	:	GoogleCloud,
		"Wit"	:	WitSpeech
		}

	def testEngine(name, engine):
	
		print(name)
		start = time.time()
		text = engine(r, sr, audio)
		if text is not None:
			print((time.time() - start) * editdistance.eval(text, wordlist))
			print( text	)

	def testSpeechText(r, sr, audio):
		for name, engine in speechEngines.items():
			testEngine(name, engine)

	wordlists=[
		"fish duck gap cheese rail hive bone wedge moss tooth",
		"fib thatch sum heel wide rake goes shop vet june",
		"fill catch thumb heap wise rave goat shone bed juice",
		"bath hum dip five ways reach joke noose got shell",
		"man hip thug ride siege veil chose shoot web cough",
		"kiss buzz hash thieve gate wife pole wretch dodge moon",
		"wish dutch jam heath laze bike rove pet fog",
		"hug dish ban rage chief pies wet cove loose"
		]
# obtain audio from the microphone
	r = sr.Recognizer()
	with sr.Microphone() as source:
		for wordlist in wordlists:
			r.adjust_for_ambient_noise(source)
			print("Say: ",wordlist)
			audio = r.listen(source)

			testSpeechText(r, sr, audio)
			input("Press Enter")
