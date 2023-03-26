from sys import argv
from time import sleep, time
from datetime import date
from PyQt5.QtWidgets import QApplication
from apps.logger import *
from apps.module import *
from appData.settings.settings_parser import BARS, MANAGEMENT, CONSUMPTION_RECALCULATOR
from DialogWindow import DialogWindow
import threading
from json import load

time_counter = {}
bars_in_count = []

if CONSUMPTION_RECALCULATOR:
    from appData.settings.settings_parser import ALL_BARS, NORM_SETTINGS, NORM_SCHEDULE
    from apps.norm_recalcuulator import norm_recalculating
    consumption_list = norm_recalculating()
    consumption_list = {bar: consumption_list[bar]['sum'] for bar in consumption_list.keys()}
    for bar in ALL_BARS:
        if NORM_SETTINGS[bar]['is_stopable'] and bar in BARS:
            time_counter[bar] = (NORM_SCHEDULE[str(date.today().weekday())][bar] + NORM_SETTINGS[bar]['stop-time'] - consumption_list[bar]) * 60
            bars_in_count.append(bar)
    

timer = 30
log = Log('log')

def main():
    global NonTrack, log, killMeProcesses, types
    with open(f'appData/processes/NonTrack.conf', 'r', encoding='utf-8') as file:
        NonTrack = file.read().splitlines()
    with open(f'appData/processes/killMeProcesses.conf', 'r', encoding='utf-8') as file:
        killMeProcesses = file.read().splitlines()
    with open(f'appData/processes/outOfTimeProcesses.conf', 'r', encoding='utf-8') as file:
        killMeProcesses.extend(file.read().splitlines())
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
            process = line[0][:-4]
            if line[3] != '0' and not process in NonTrack and not process in killMeProcesses: 
                if not process in log.logs:
                    if process in types:
                        log.logs.update({process: [types[process], 0, line[1]]})
                    else:
                        app = QApplication(argv)
                        dialog = DialogWindow(process, log, types)
                        dialog.resize(400, 300)
                        dialog.show()
                        app.exec_()
                        if dialog.process_added:
                            types = dialog.types
                            log.logs.update({process: [types[process], 0, line[1]]})
                        else:
                            NonTrack.append(process)
                        del dialog
                        del app
                elif log.logs[process][2] == line[1]:
                    log.logs[process][1] += timer
                    if log.logs[process][0] in bars_in_count:
                        time_counter[log.logs[process][0]] -= timer
                elif log.logs[process][2] != line[1] and log.new_session:
                    log.logs[process][2] = line[1]
            elif process in killMeProcesses: 
                commandExecution('taskkill /PID ' + line[1])
    for bar, time in time_counter.items():
        if time < 0:
            killMeProcesses.extend([process for process, data in log.logs.items() if data[0] == bar and process not in killMeProcesses])
            time_counter[bar] = 0
            with open(f'appData/processes/outOfTimeProcesses.conf', 'w', encoding='utf-8') as file:
                file.write('\n'.join(killMeProcesses))

    log.write()

if __name__ == "__main__":
    if MANAGEMENT:
        main()