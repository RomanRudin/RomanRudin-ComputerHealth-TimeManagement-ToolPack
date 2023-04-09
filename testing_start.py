from subprocess import Popen
from sys import executable
from time import sleep

background = Popen([executable, 'main.py'])
programm = Popen([executable, 'window.py'])
sleep(120)
background.kill()
programm.kill()