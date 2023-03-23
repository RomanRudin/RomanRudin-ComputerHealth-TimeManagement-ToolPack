from asyncio import tasks
from sys import argv, exit
from time import sleep, time
from PyQt5.QtWidgets import QApplication
from datetime import datetime, date
from apps.logger import *
from apps.module import *
from appData.settings.settings_parser import MANAGEMENT
from DialogWindow import DialogWindow
import threading
from json import load

timer = 5
log = Log('log')

def main():
    global NonTrack, log, killMeProcesses, types
    with open(f'appData/processes/NonTrack.conf', 'r', encoding='utf-8') as file:
        NonTrack = file.read().splitlines()
    with open(f'appData/processes/killMeProcesses.conf', 'r', encoding='utf-8') as file:
        killMeProcesses = file.read().splitlines()
    with open(f'appData/processes/types.json', 'r', encoding='utf-8') as file:
        types = load(file)
    tasksSave()
    while (True):
        thread = threading.Thread(target= tasksSave)
        thread.start()
        sleep(timer)

def tasksSave():
    global types
    tasks = commandExecutionP('tasklist /FO CSV')
    for line in tasks:        
        line = line.replace('"', '').split(',')
        if len(line) > 1: 
            if line[3] != '0' and not line[0][:-4] in NonTrack: 
                if not line[0][:-4] in log.logs:
                    if line[0][:-4] in types:
                        log.logs.update({line[0][:-4]: [types[line[0][:-4]], 0, line[1]]})
                    else:
                        app = QApplication(argv)
                        dialog = DialogWindow(line[0][:-4], log, types)
                        dialog.resize(400, 300)
                        dialog.show()
                        app.exec_()
                        if dialog.process_added:
                            types = dialog.types
                            log.logs.update({line[0][:-4]: [types[line[0][:-4]], 0, line[1]]})
                            print(list(types.keys())[-1])
                        else:
                            NonTrack.append(line[0][:-4])
                        del dialog
                        del app
                elif log.logs[line[0][:-4]][2] == line[1]:
                    log.logs[line[0][:-4]][1] += timer
            elif line[0] in killMeProcesses: 
                commandExecution('taskkill /PID ' + line[1])
    log.write()

if __name__ == "__main__":
    if MANAGEMENT:
        main()