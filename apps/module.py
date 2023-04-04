from os import system, popen

def commandExecutionP(command) -> list:
# Функция использует устаревшую функцию "popen" из модуля os, однако это работает и вполне удобно
    return popen(command).read().splitlines()

def commandExecution(command) -> str:
# Функция используем модуль os и выполняет cmd команду
    return system(command)

#Shutdown function for future usage (of course not for the purpose of spying)
def computer_restarter() -> str:
    return system('shutdown /r /t 60 /d [p]4 /c "Planned restar of computer (see the setting of time manager programm) in 60 sec"')
def computer_hybernation() -> str:
    return system('shutdown /h /t 60 /c "Hybernation mode will be turned on in 60 sec"')
def computer_shutdown() -> str:
    return system('shutdown /l /t 60')
def computer_shutdown_canceler() -> str:
    return system('shutdown /a /c "Shutdown stopped successfuly"')