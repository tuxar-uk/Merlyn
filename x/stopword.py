stop = 'cmds/stopwords.txt'
stopwords = set()
lines = open(stop)
for line in lines:
	line = line.strip()
	if len(line) and line[0]!="#":
		stopwords.add(line)
	words = str(spoken).lower().split()
	print('<', words)
	phrase = ''
	for word in words:
	
		if word not in stopwords: phrase += ' ' + word

	phrase = phrase.strip().lower()
	if phrase == '': continue

	while phrase.strip() not in commands.keys():
		words = phrase.split()
		del words[-1]
		phrase = ' '.join(words)
