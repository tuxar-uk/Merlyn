import sys, os, pyaudio
from pocketsphinx import *

modeldir = "/usr/share/pocketsphinx/model/"
# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', os.path.join(modeldir, 'hmm/en_US/hub4wsj_sc_8k'))
config.set_string('-dict', os.path.join(modeldir, 'lm/en_US/cmu07a.dic'))
config.set_string('-keyphrase', 'oh mighty computer')
config.set_float('-kws_threshold', 1e-40)

decoder = Decoder(config)
decoder.start_utt('spotting')

stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()        

while True:
    buf = stream.read(1024)
    decoder.process_raw(buf, False, False)
    if decoder.hyp() != None and decoder.hyp().hypstr == 'oh mighty computer':
        print("Detected keyword, restarting search")
        decoder.end_utt()
        decoder.start_utt('spotting')
