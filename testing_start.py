from subprocess import Popen
from sys import executable
from time import sleep

background = Popen([executable, 'main.pyw'])
programm = Popen([executable, 'window.py'])
sleep(60)
background.kill()
programm.kill()
print("Test ended")