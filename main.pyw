from sys import argv
from time import sleep
from datetime import date
from PyQt5.QtWidgets import QApplication
from apps.logger import *
from apps.module import *
from appData.settings.settings_parser import BARS, MANAGEMENT, CONSUMPTION_RECALCULATOR, HEALTH, SCHEDULE, \
    HEALTH_SETTINHS, stylesheet_popup
from apps.health import Health_popup_special, Health_popup_standart
from DialogWindow import DialogWindow
import threading
from json import load

log = Log('log')    #logger


class ThreadController():
    def __init__(self):

        self.time_counter = {}
        self.bars_in_count = []
        self.health_time_counter = {}

        self.timer = 60          #duration between two tracking sessions
        self.management_norm_counter = 5    #duration (in 'timers' units of measure) between two recalculating sessions
        self.stopped = False
        if MANAGEMENT:
            with open('appData/processes/NonTrack.conf', 'r', encoding='utf-8') as file:
                self.NonTrack = file.read().splitlines()         #untracked processes (such as system processes)
            with open('appData/processes/killMeProcesses.conf', 'r', encoding='utf-8') as file:
                self.killMeProcesses = file.read().splitlines()  #processes user don't want to deal with at all
            with open('appData/processes/types.json', 'r', encoding='utf-8') as file:
                self.types = load(file)                          #types of every known for programm process
            with open('appData/processes/DoNotDisturbProcesses.conf', 'r', encoding='utf-8') as file:
                self.doNotDisturbProcesses = file.read().splitlines()
        if SCHEDULE:
            pass    #TODO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.load()
        self.main()
        self.get_norm()
        counter = 0
        #every iteration takes one thread and gets data of processes and etc.
        while (True):
            thread = threading.Thread(target=self.main)
            thread.start()
            sleep(self.timer)
            if counter % self.management_norm_counter == 0:
                self.get_norm()
            counter += 1
    
    
    def main(self):
        if not self.stopped:
            #Multiple tools (such as mangement, health nd etc.) need to be done at the sme trcking itertion, 'cause I don't want programm to take multiple threads 
            if MANAGEMENT:
                doNotDisturb = self.management_thread()
            if SCHEDULE:
                self.schedule_thread()
            if HEALTH:
                self.health_thread(doNotDisturb)


    def load(self):
        if HEALTH:
            for exersize, exersize_data in HEALTH_SETTINHS.items():
                self.health_time_counter[exersize] = {'timer_counter': exersize_data[1] * 60 // self.timer, \
                    'type': exersize_data[0]}


    def get_norm(self):
        if CONSUMPTION_RECALCULATOR and MANAGEMENT:
            from appData.settings.settings_parser import ALL_BARS, NORM_SETTINGS, NORM_SCHEDULE
            from apps.norm_recalcuulator import norm_recalculating
            consumption_list = norm_recalculating()
            consumption_list = {bar: consumption_list[bar]['sum'] for bar in consumption_list.keys()}
            for bar in ALL_BARS:
                if NORM_SETTINGS[bar]['is_stopable'] and bar in BARS:
                    self.time_counter[bar] = (NORM_SCHEDULE[str(date.today().weekday())][bar] + NORM_SETTINGS[bar]['stop_time'] - consumption_list[bar]) * 60
                    self.bars_in_count.append(bar)


    def management_thread(self):
        doNotDisturb = False
        tasks = commandExecutionP('tasklist /FO CSV')
        task_list = set()   #my own interpretaton of checking on already tracked programm processes (because one programm can have multiple of them with different ids)
        for line in tasks:        
            line = line.replace('"', '').split(',')
            if len(line) > 1: 
                process = line[0][:-4]
                if line[3] != '0' and not process in self.NonTrack and not process in self.killMeProcesses: 
                    if not process in log.logs: #if process hadn't been tracked today
                        if process in types:
                            log.logs.update({process: [types[process], 0, line[1]]})
                        else:   #asking user about what type this process has
                            self.stopped = True
                            app = QApplication(argv)
                            dialog = DialogWindow(process, log, types)
                            dialog.resize(400, 300)
                            dialog.show()
                            app.exec_()
                            if dialog.process_added:
                                types = dialog.types
                                log.logs.update({process: [types[process], 0]})
                            else:
                                self.NonTrack.append(process)
                            #I'm really sorry for the next 2 lines of code, but this was the only way the programm won't destroy itself after asking user
                            del dialog
                            del app
                            self.stopped = False
                    elif process not in task_list: #if this programms processes weren't tracked in this tracking session
                        log.logs[process][1] += self.timer
                        task_list.add(process)
                        if log.logs[process][0] in self.bars_in_count:
                            self.time_counter[log.logs[process][0]] -= self.timer #timer before possibility to close the process on programm's purpose (because user spent to much time on this category already)
                    if process in self.doNotDisturbProcesses:
                        doNotDisturb = True
                elif process in self.killMeProcesses: 
                    commandExecution('taskkill /PID ' + line[1])
        for bar, time in self.time_counter.items():
            if time < 0:
                self.killMeProcesses.extend([process for process, data in log.logs.items() if data[0] == bar and process not in self.killMeProcesses])
                self.time_counter[bar] = 0
        log.write()
        return doNotDisturb

        
    def health_thread(self, doNotDisturb):
        for exersize, exersize_data in self.health_time_counter.items():
            exersize_data['timer_counter'] -= 1
            if exersize_data['timer_counter'] <= 0 and not doNotDisturb:
                app = QApplication(argv)
                app.setStyleSheet(stylesheet_popup)
                if exersize_data['type'] == 'Standart':
                    popup = Health_popup_standart(exersize)
                    popup.show()
                    app.exec_()
                else:
                    self.stopped = True
                    popup = Health_popup_special(exersize)
                    popup.show()
                    app.exec_()
                    self.stopped = False
                del popup
                del app
                exersize_data['timer_counter'] = HEALTH_SETTINHS[exersize][1]


    def schedule_thread():
        pass


if __name__ == "__main__":
    if MANAGEMENT or HEALTH or SCHEDULE:
        thread_controller = ThreadController()
