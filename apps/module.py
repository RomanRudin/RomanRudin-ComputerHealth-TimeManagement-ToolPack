from os import system, popen

def commandExecutionP(command):
# Функция использует устаревшую функцию "popen" из модуля os, однако это работает и вполне удобно
    return popen(command).read().splitlines()

def commandExecution(command):
# Функция используем модуль os и выполняет cmd команду
    return system(command)

#Shutdown function for future usage (of course not for the purpose of spying)
def computer_restarter():
    return system('shutdown /r /t 60 /d [p]4 /c "Planned restar of computer (see the setting of time manager programm) in 60 sec"')
def computer_hybernation():
    return system('shutdown /h /t 60 /c "Hybernation mode will be turned on in 60 sec"')
def computer_shutdown():
    return system('shutdown /l /t 60')
def computer_shutdown_canceler():
    return system('shutdown /a /c "Shutdown stopped successfuly"')