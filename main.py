import os
from time import sleep, time
from datetime import datetime, date
from logger import *
from module import *
import threading
from json import load

timer = 10

def main():
    global BlackList, log, killMeProcesses, types
    with open('NonTrack.conf', 'r', encoding='utf-8') as file:
        BlackList = file.read().splitlines()
    with open('killMeProcesses.txt', 'r', encoding='utf-8') as file:
        killMeProcesses = file.read().splitlines()
    with open('types.json', 'r', encoding='utf-8') as file:
        types = load(file)
    log = Log('log')
    _PID = commandExecutionP('tasklist /FO CSV')
    PidSave(_PID)
    while (True):
        thread = threading.Thread(target= PidRead)
        thread.start()
        sleep(timer)


def PidRead():
    _PID = commandExecutionP('tasklist /FO CSV')
    d = str(date.today())
    t = str(datetime.today().strftime("%H:%M:%S"))
    PidSave(_PID)

def PidSave(_PID):
    for line in _PID:
        line = line.replace('"', '').split(',')
        if len(line) > 1: 
            if line[3] != '0' and not line[0] in BlackList: #
                if not line[0][:-4] in log.logs:
                    log.logs.update({line[0][:-4]: ['TYPE', 0, line[1]]})    #types[line[0][:-4]], 0]})
                elif log.logs[line[0][:-4]][2] == line[1]:
                    log.logs[line[0][:-4]][1] += timer
            elif line[0] in killMeProcesses: 
                commandExecution('taskkill /PID ' + line[1])
    log.write()

if __name__ == "__main__":
    main()