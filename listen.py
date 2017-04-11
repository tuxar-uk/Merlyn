#!/opt/anaconda3/bin/python3
import sys
from Merlyn import Merlyn

mln = Merlyn(5514)	# change to the number from lmtool
if len(sys.argv) > 1 and sys.argv[1] == 'demo': mln.do_demo()
mln.listen()

# Testing 1 2 3...
#mln.parse_do(['calculator', 'place window', 'number one thousand and twenty four', 'add ninety nine', 'divide by twenty two', 'equals', 'press enter'])
#mln.parse_do(['paint', 'place window', 'left button down', 'mouse east four hundred'])
