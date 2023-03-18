import os
from time import sleep, time
from datetime import datetime, date
from apps.logger import *
from apps.module import *
import threading
from json import load

timer = 60

def main():
    global NonTrack, log, killMeProcesses, types
    with open(f'appData/processes/NonTrack.conf', 'r', encoding='utf-8') as file:
        NonTrack = file.read().splitlines()
    with open(f'appData/processes/killMeProcesses.conf', 'r', encoding='utf-8') as file:
        killMeProcesses = file.read().splitlines()
    with open(f'appData/processes/types.json', 'r', encoding='utf-8') as file:
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
            if line[3] != '0' and not line[0] in NonTrack: #
                if not line[0][:-4] in log.logs:
                    log.logs.update({line[0][:-4]: ['TYPE', 0, line[1]]})    #types[line[0][:-4]], 0, line[1]]})
                elif log.logs[line[0][:-4]][2] == line[1]:
                    log.logs[line[0][:-4]][1] += timer
            elif line[0] in killMeProcesses: 
                commandExecution('taskkill /PID ' + line[1])
    log.write()

if __name__ == "__main__":
    main()