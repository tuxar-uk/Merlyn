#!/usr/bin/python3

# Edit *.txt to add, change, or delete commands.
# Run this script to generate ../lang/corpus.txt and ../data/*.show
# Submit corpus.txt to
# http://www.speech.cs.cmu.edu/tools/lmtool-new.html

inf = open("files.list", 'r')
out = open("../lang/corpus.txt", 'w')
all = open("all.txt", 'w')
cmds = {}

for file in inf:

	file = file.strip()
	if file[0] == '#': continue
	print(file)

	inp = open(file, 'r')
	(shw, ext) = file.split('.')
	shw = '../data/' + shw
	shw += '.shw'
	cmd = open(shw, 'w')

	for line in inp:
		line = line.strip()
		if line[:9] == '# -------':
			cmd.write('\n' + line[10:].upper() + ':\n')
			pass
	
		elif len(line) and line[0] != "#":
			(name, spell) = line.split(":", 1)
			temp = name.strip().lower().split()
			name = ' '.join(temp).strip()
			spell = spell.strip()
			if name in cmds.keys():
				print("Duplicate:", name, cmds[name], spell)
			else:
				cmds[name] = spell
				out.write(name + '\n')
				cmd.write(name + ',	')
				if spell: all.write(name + ':' + spell + '\n')
	cmd.close()
print("Go to: http://www.speech.cs.cmu.edu/tools/lmtool-new.html")
