from sys import argv
from time import sleep
from datetime import date
from PyQt5.QtWidgets import QApplication
from apps.logger import *
from apps.module import *
from appData.settings.settings_parser import BARS, LEARNING, MANAGEMENT, CONSUMPTION_RECALCULATOR, HEALTH, SCHEDULE
from DialogWindow import DialogWindow
import threading
from json import load


log = Log('log')    #logger

#norm autorecalculating function
def norm_getting():
    if CONSUMPTION_RECALCULATOR and MANAGEMENT:
        from appData.settings.settings_parser import ALL_BARS, NORM_SETTINGS, NORM_SCHEDULE
        from apps.norm_recalcuulator import norm_recalculating
        consumption_list = norm_recalculating()
        consumption_list = {bar: consumption_list[bar]['sum'] for bar in consumption_list.keys()}
        for bar in ALL_BARS:
            if NORM_SETTINGS[bar]['is_stopable'] and bar in BARS:
                time_counter[bar] = (NORM_SCHEDULE[str(date.today().weekday())][bar] + NORM_SETTINGS[bar]['stop-time'] - consumption_list[bar]) * 60
                bars_in_count.append(bar)


def start_programm():
    if MANAGEMENT:
        global NonTrack, log, killMeProcesses, types
        with open(f'appData/processes/NonTrack.conf', 'r', encoding='utf-8') as file:
            NonTrack = file.read().splitlines()         #untracked processes (such as system processes)
        with open(f'appData/processes/killMeProcesses.conf', 'r', encoding='utf-8') as file:
            killMeProcesses = file.read().splitlines()  #processes user don't want to deal with at all
        with open(f'appData/processes/types.json', 'r', encoding='utf-8') as file:
            types = load(file)                          #types of every known for programm process
    if SCHEDULE:
        pass    #TODO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    main()
    norm_getting()
    counter = 0
    #every iteration takes one thread and gets data of processes and etc.
    while (True):
        thread = threading.Thread(target= main)
        thread.start()
        sleep(timer)
        if counter % norm_counter == 0:
            norm_getting()
        counter += 1


def main():
    #Multiple thins (such as mangement, health nd etc.) need to be done at the sme trcking itertion, 'cause I don't want programm to take multiple threads 
    if MANAGEMENT:
        global types
        tasks = commandExecutionP('tasklist /FO CSV')
        task_list = set()   #my own interpretaton of checking on already tracked programm processes (because one programm can have multiple of them with different ids)
        print(tasks)
        for line in tasks:        
            line = line.replace('"', '').split(',')
            if len(line) > 1: 
                process = line[0][:-4]
                if line[3] != '0' and not process in NonTrack and not process in killMeProcesses: 
                    if not process in log.logs: #if process hadn't been tracked today
                        if process in types:
                            log.logs.update({process: [types[process], 0, line[1]]})
                        else:   #asking user about what type this process has
                            app = QApplication(argv)
                            dialog = DialogWindow(process, log, types)
                            dialog.resize(400, 300)
                            dialog.show()
                            app.exec_()
                            if dialog.process_added:
                                types = dialog.types
                                log.logs.update({process: [types[process], 0]})
                            else:
                                NonTrack.append(process)
                            #I'm really sorry for the next 2 lines of code, but this was the only way the programm won't destroy itself after asking user
                            del dialog
                            del app
                    elif process not in task_list: #if this programms processes weren't tracked in this tracking session
                        log.logs[process][1] += timer
                        task_list.add(process)
                        if log.logs[process][0] in bars_in_count:
                            time_counter[log.logs[process][0]] -= timer #timer before possibility to close the process on programm's purpose (because user spent to much time on this category already)
                elif process in killMeProcesses: 
                    commandExecution('taskkill /PID ' + line[1])
        for bar, time in time_counter.items():
            if time < 0:
                killMeProcesses.extend([process for process, data in log.logs.items() if data[0] == bar and process not in killMeProcesses])
                time_counter[bar] = 0
        log.write()

    if SCHEDULE:
        pass

    if HEALTH:
        pass

    if LEARNING:
        pass


if __name__ == "__main__":
    if MANAGEMENT or HEALTH or SCHEDULE or LEARNING:
        time_counter = {}
        bars_in_count = []

        timer = 60          #duration between two tracking sessions
        norm_counter = 5    #duration (in 'timers' units of measure) between two recalculating sessions
        start_programm()
