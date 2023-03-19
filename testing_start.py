from subprocess import Popen
from sys import executable
from time import sleep
from main import timer

background = Popen([executable, 'main.py'])
sleep(timer * 2 + 1)
programm = Popen([executable, 'window.py'])
sleep(timer * 2)
background.kill()
programm.kill()