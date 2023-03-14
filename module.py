from os import system, popen

def commandExecutionP(command):
# Функция использует устаревшую функцию "popen" из модуля os, однако это работает и вполне удобно
    return popen(command).read().splitlines()

def commandExecution(command):
# Функция используем модуль os и выполняет cmd команду
    return system(command)