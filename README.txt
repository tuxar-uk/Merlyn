Merlyn Computer Control by Speech Recognition
=============================================

Copyright 2017 Alan Richmond @ AILinux.net
https://opensource.org/licenses/MIT

Merlyn is a Python program for controlling a computer by using voice commands. It is based on the CMU PocketSphinx system, and is capable of supporting most tasks that you might want to do on a regular PC, using voice only. It is currently Linux only. You may find the following useful (altered to your own context) in your .bashrc or some alias file:

# Merlyn
alias mln="cd ~/Merlyn"
alias merlyn="~/Merlyn/listen.py"
export MLN_BROWSER=google-chrome
export MLN_DATA=/home/c/Merlyn/data
export MLN_FM="pcmanfm"
export MLN_KEYPRESS="xdotool key "
export MLN_LOCATION=Neath
export MLN_MYNAME=Alan
export MLN_SPELLS=/home/c/Merlyn/spells

You need to install PocketSphinx, either from your distro's repo, or from https://github.com/cmusphinx/pocketsphinx Then take a look through Merlyn/cmds/all.txt for the software needed to implement the spoken commands, e.g. xdotool, zenity, ...

The subdirectories are:

cmds	:	files mapping spoken commands to Linux
demo	:	invoke demo on the command line, e.g. merlyn demo
data	:	text & media for Merlyn to display, e.g. help
lang	:	the files from http://www.speech.cs.cmu.edu/tools/lmtool-new.html
spells	:	scripts for Merlyn's wizardry
x	:	not important, just stuff that might one day be useful. or not.

Adding & Editing Commands: Look at the *.txt files in the cmds subdirectory. Edit those or add your own. If you want to start a new .txt file be sure to add it to files.list. Run the lmtool.py file to generate corpus.txt then go to the indicated URL, click on 'choose file'. Click on 'Compile knowledge base'. Download the generated tar file, e.g. copy the link and give it to wget inside the lang dir. tar xvzf the tar file. Note the 4-digit number in its name, and edit Merlyn.py to replace the old number.



If you have problems, or suggestions for improvement, please visit http://AILinux.net/Merlyn
or send email to merlyn at the just-mentioned domain name.

DISCLAIMER: This is an alpha release, i.e. just proof-of-concept. If I don't get positive feedback about it there might not be a beta realease. And if I do, there may be changes that are incompatible with the previous version. And you use Merlyn at your own risk. See the MIT license:

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
