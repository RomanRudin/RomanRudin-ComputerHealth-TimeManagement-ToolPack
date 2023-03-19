from subprocess import Popen
from sys import executable
from time import sleep

background = Popen([executable, 'main.py'])
sleep(1)
programm = Popen([executable, 'window.py'])