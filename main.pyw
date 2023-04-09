from sys import argv
from time import sleep
from datetime import date
from PyQt5.QtWidgets import QApplication
from apps.logger import *
from apps.module import *
from appData.settings.settings_parser import BARS, LEARNING, MANAGEMENT, CONSUMPTION_RECALCULATOR, HEALTH, SCHEDULE, \
    HEALTH_SETTINHS
from apps.health import Health_popup_special, Health_popup_standart
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
                time_counter[bar] = (NORM_SCHEDULE[str(date.today().weekday())][bar] + NORM_SETTINGS[bar]['stop_time'] - consumption_list[bar]) * 60
                bars_in_count.append(bar)
    if HEALTH:
        for exersize, exersize_data in HEALTH_SETTINHS.items():
            health_time_counter[exersize] = {'timer_counter': exersize_data[1] * 60 // timer, \
                'type': exersize_data[0]}


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
        if counter % management_norm_counter == 0:
            norm_getting()
        counter += 1


def  management_thread():
    global types, stopped
    tasks = commandExecutionP('tasklist /FO CSV')
    task_list = set()   #my own interpretaton of checking on already tracked programm processes (because one programm can have multiple of them with different ids)
    for line in tasks:        
        line = line.replace('"', '').split(',')
        if len(line) > 1 and not stopped: 
            process = line[0][:-4]
            if line[3] != '0' and not process in NonTrack and not process in killMeProcesses: 
                if not process in log.logs: #if process hadn't been tracked today
                    if process in types:
                        log.logs.update({process: [types[process], 0, line[1]]})
                    else:   #asking user about what type this process has
                        stopped = True
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
                        stopped = False
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


def health_thread():
    for exersize, exersize_data in health_time_counter.items():
        if exersize_data['timer_counter'] <= 0:
            app = QApplication(argv)
            if exersize_data['type'] == 'Standart':
                popup = Health_popup_standart(exersize)
                popup.resize(400, 300)
                popup.show()
                app.exec_()
            else:
                popup = Health_popup_special(exersize)
                popup.resize(400, 300)
                popup.show()
                app.exec_()
            del popup
            del app
            exersize_data['timer_counter'] = HEALTH_SETTINHS[exersize][1]
        else:
            exersize_data['timer_counter'] -= 1




def schedule_thread():
    pass


def learning_thread():
    pass



def main():
    #Multiple thins (such as mangement, health nd etc.) need to be done at the sme trcking itertion, 'cause I don't want programm to take multiple threads 
    if MANAGEMENT:
        management_thread()
    if SCHEDULE:
        schedule_thread()
    if HEALTH:
        health_thread()
    if LEARNING:
        learning_thread


if __name__ == "__main__":
    if MANAGEMENT or HEALTH or SCHEDULE or LEARNING:
        time_counter = {}
        bars_in_count = []
        health_time_counter = {}

        timer = 60          #duration between two tracking sessions
        management_norm_counter = 5    #duration (in 'timers' units of measure) between two recalculating sessions
        stopped = False
        start_programm()
