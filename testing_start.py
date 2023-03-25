from subprocess import Popen
from sys import executable
from time import sleep
from main import timer

background = Popen([executable, 'main.py'])
programm = Popen([executable, 'window.py'])
sleep(timer - 5)
background.kill()
programm.kill()