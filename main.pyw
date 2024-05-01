from sys import argv
from time import sleep
from datetime import date
from PyQt5.QtWidgets import QApplication
from apps.logger import *
from apps.module import *
from appData.settings.settings_parser import BARS, MANAGEMENT, \
    CONSUMPTION_RECALCULATOR, HEALTH, SCHEDULE, HEALTH_SETTINHS, stylesheet_popup, ABSOLUTE_PATH
from apps.health import Health_popup_special, Health_popup_standart
from DialogWindow import DialogWindow
import threading
from json import load
import ctypes

enumWindows = ctypes.windll.user32.EnumWindows
enumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
getWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW 
getWindowText = ctypes.windll.user32.GetWindowTextW

log = Log(ABSOLUTE_PATH + 'log')    #logger

#Getting current window (stolen from pyautogui) :)
def getActiveWindowTitle() -> str:
    global activeWindowTitle
    activeWindowHwnd = ctypes.windll.user32.GetForegroundWindow()
    if activeWindowHwnd == 0:
        raise "ctypes.windll.user32.GetForegroundWindow() is 0"
    def foreach_window(hWnd, lParam) -> bool:
        global activeWindowTitle
        if hWnd == activeWindowHwnd:
            length = getWindowTextLength(hWnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            getWindowText(hWnd, buff, length + 1)
            activeWindowTitle = buff.value
        return True
    enumWindows(enumWindowsProc(foreach_window), 0)
    return str(activeWindowTitle).split(" - ")[-1]

class ThreadController():
    def __init__(self) -> None:

        self.time_counter = {}
        self.bars_in_count = []
        self.health_time_counter = {}

        #duration between two tracking sessions
        self.timer = 1          
        #duration (in 'timers' units of measure) between two recalculating sessions
        self.management_norm_counter = 5    
        self.stopped = False
        
        if MANAGEMENT:
            with open(ABSOLUTE_PATH + 'appData/processes/NonTrack.conf', 'r', encoding='utf-8') as file:
                self.NonTrack = file.read().splitlines()         #untracked processes (such as system processes)
            with open(ABSOLUTE_PATH + 'appData/processes/types.json', 'r', encoding='utf-8') as file:
                self.types = load(file)                          #types of every known for programm process
            with open(ABSOLUTE_PATH + 'appData/processes/DoNotDisturbProcesses.conf', 'r', encoding='utf-8') as file:
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
    
    
    def main(self) -> None:
        if not self.stopped:
            #Multiple tools (such as mangement, health nd etc.) need to be done at the sme trcking itertion, 'cause I don't want programm to take multiple threads 
            if MANAGEMENT:
                doNotDisturb = self.management_thread()
            if SCHEDULE:
                self.schedule_thread()
            if HEALTH:
                self.health_thread(doNotDisturb)


    def load(self) -> None:
        if HEALTH:
            for exersize, exersize_data in HEALTH_SETTINHS.items():
                self.health_time_counter[exersize] = {'timer_counter': exersize_data[1] * 60 // self.timer, \
                    'type': exersize_data[0]}


    def get_norm(self) -> None:
        if CONSUMPTION_RECALCULATOR and MANAGEMENT:
            from appData.settings.settings_parser import ALL_BARS, NORM_SETTINGS, NORM_SCHEDULE
            from apps.norm_recalcuulator import norm_recalculating
            consumption_list = norm_recalculating()
            consumption_list = {bar: consumption_list[bar]['sum'] for bar in consumption_list.keys()}
            for bar in ALL_BARS:
                if NORM_SETTINGS[bar]['is_stopable'] and bar in BARS:
                    self.time_counter[bar] = (NORM_SCHEDULE[str(date.today().weekday())][bar] + NORM_SETTINGS[bar]['stop_time'] - consumption_list[bar]) * 60
                    self.bars_in_count.append(bar)


    def management_thread(self) -> None:
        doNotDisturb = False
        current_window_title = getActiveWindowTitle()
        if not current_window_title in self.NonTrack: 
            if not current_window_title in log.logs: #if process hadn't been tracked today
                if current_window_title in self.types:
                    log.logs.update({current_window_title: [self.types[current_window_title], 0]})
                else:   #asking user about what type this process has
                    self.stopped = True
                    app = QApplication(argv)
                    dialog = DialogWindow(current_window_title, log, self.types)
                    dialog.resize(400, 300)
                    dialog.show()
                    app.exec_()
                    if dialog.process_added:
                        self.types = dialog.types
                        log.logs.update({current_window_title: [self.types[current_window_title], 0]})
                    else:
                        self.NonTrack.append(current_window_title)
                    #I'm really sorry for the next 2 lines of code, but this was the only way the programm won't destroy itself after asking user
                    del dialog
                    del app
                    self.stopped = False
        if not current_window_title in self.NonTrack: 
            log.logs[current_window_title][1] += self.timer
        log.write()
        return doNotDisturb

        
    def health_thread(self, doNotDisturb) -> None:
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


    def schedule_thread(self) -> None:
        pass


if __name__ == "__main__":
    if MANAGEMENT or HEALTH or SCHEDULE:
        thread_controller = ThreadController()
