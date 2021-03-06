"""	Merlyn Speech Control for PC

	We load in commands (& spells) generated by lmtool.py
	and also language files generated by the Sphinx lmtool
	http://www.speech.cs.cmu.edu/tools/lmtool-new.html
	then open up a stream of words from the mic via LiveSpeech
	and try to parse it into commands and possibly some parameters.
	If succesful, hand off to the OS.

	The parsing will need improving as the syntax evolves...

	Copyright 2017 Alan Richmond @ AILinux.net
	The MIT License	https://opensource.org/licenses/MIT
"""
import os
from subprocess import call
from pocketsphinx import LiveSpeech, get_model_path

class Merlyn:
	"""	Merlyn Speech Control for PC"
	"""
	def __init__(self, num):
		"""	init with the number given by the lmtool
		"""
		self.num  = str(num)
		self.mer = os.path.expanduser("~/Merlyn")
		cmds = os.path.join(self.mer, 'cmds/all.txt')
		lang = os.path.join(self.mer, 'lang/')
		self.lm   = os.path.join(lang, self.num + '.lm')
		self.dic  = os.path.join(lang, self.num + '.dic')

# Read in and store commands
		try:
			lines = open(cmds)
		except IOError:
			sys.exit("Could not open file " + cmds)

		count = 0
		self.commands = {}
		for line in lines:
			line = line.strip()
			if len(line) > 1 and line[0] != "#":		# skip over empty lines & comments
				(cmd, spell) = line.split(":",1)
				self.commands[cmd.strip().lower()] = spell.strip()
				count += 1

	def parse_the(self, cmd):
		"""	Parse the text command supplied by the PocketSphinx listener.
		"""
		self.cmd = cmd
		self.spell = None
		self.params = []
						# start with the whole phrase
		while self.cmd not in self.commands:	# if not recognised then
			words = self.cmd.split()	# split up phrase into words
			if len(words) < 2: break
			word = words[-1]		# split off last word
			del words[-1]
# This is probably temporary. I'm assuming only integer params for now...
			if word == "to":		# Sphinx thinks user said 'to'
				word = "two"			# but more likely they said 'two'
			elif word == "for":		# Sphinx thinks user said 'for'
				word = "four"			# you get the idea...
			self.params.append(word)		# save words not part of the command
			self.cmd = ' '.join(words).strip()	# re-join words for possible command

		if self.cmd not in self.commands:
			return None

		self.params.reverse()		# above loop picked off words from right
		self.spell = self.commands[self.cmd]	# this is the spell that Merlyn will utter

		if self.params:			# are there some params?
			par = ' '.join(self.params).strip()	# join them back into a string
			try:				# for now I'm assuming ints only 
				num = str(text2int(par))
			
			except:
				print("Not a good num:", par)

			try:
				self.spell = self.spell % num		# substitute in the spell

			except:	ok = False

		return self.spell

	def printcmd(self):
#		print("<", self.cmd, self.params, '	{', self.spell, '	}')
		print("<", self.cmd, self.params)

	def parse_do(self, cmd):
		"""	Parse the command then do it.
		"""
		spell = self.parse_the(cmd)

		if spell is None: return

		self.printcmd()

		try:
			retcode = call(spell, shell=True)	# here OS, do this!
			if retcode < 0:
				print("Child was terminated by signal", -retcode, file=sys.stderr)

		except OSError as e:
			print("Execution failed:", e, file=sys.stderr)

	def do_demo(self):
		"""	Run Merlyn's self-demo.
		"""
		demo = os.path.join(self.mer, 'demo/demo.sh &')
		print(demo)
		call(demo, shell=True)	# here OS, do this!

	def listen(self):
		"""	Top-level loop to get text from the user's microphone,
	check for some special commands; if we're expecting a command then do it.
		"""
		print( "|	Say 'Merlyn' to make him/her listen.\n\
|		Merlyn will obey the next command. If that is 'keep listening' then\n\
|		Merlyn will continue to obey commands until you say 'stop listening'.\n\
|		Say 'help' to see this message again, and to get further help.")

		listening = obey = first = False

#		https://pypi.python.org/pypi/pocketsphinx
		speech = LiveSpeech(hmm=os.path.join(get_model_path(), 'en-us'), lm=self.lm, dic=self.dic)

		for spoken in speech:		# get user's command

			cmd = str(spoken).lower()

			if cmd == 'merlyn':		# need to hear my name before doing stuff
				obey = True			# flag to obey next command
				first = True			# obey flag will be toggled off after first use

			elif cmd == 'keep listening':	# or be told to keep listening for commands
				listening = True

			elif cmd == 'stop listening':	# until told to stop
				listening = False
				obey = True			# need to acknowledge the stop

			elif cmd == 'exit':		# we're done...
				break

			elif cmd == '':			# somehow got an empty command
				continue

			if obey or listening:		# attempt to recognise the command and params

				self.parse_do(cmd)

				if not first:
					obey = False

			first = False

# http://stackoverflow.com/questions/493173/is-there-a-way-to-convert-number-words-to-integers

def text2int(textnum, numwords={}):
    if not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = ["hundred", "thousand", "million", "billion", "trillion"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word == 'full': word = 'four'	# kludge
        if word == 'q': word = 'two'	# kludge
        if word not in numwords:
          raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current
