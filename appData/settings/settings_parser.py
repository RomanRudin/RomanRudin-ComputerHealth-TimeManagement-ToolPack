from datetime import date
from json import load
from typing import Final, TypedDict
from os import path

ABSOLUTE_PATH = path.realpath('settings_parser.py')[:-18]
# C:\Programing\InProgress\TimeManager\appData\settings
'''
If you want to read False as False from file in Python, you gonna need to use this crunch, because only empty sting will return False if converted to bool
'''
def boolean_reader(text) -> bool:
    if text.lower().capitalize() == 'False':
        return False
    return True

def equality_parser(text, boolean=False) -> str or bool:
    value = text[text.find(' = ') + 3:]
    if boolean:
       return boolean_reader(value)
    return value

#TODO Make data classes for TIMETABLE_SETTINGS and TASK_LIST_SETTINGS
class Tasks_settings(TypedDict):
    is_on: bool
    messaging: bool


#reading main config file, containing which sections of programms are going to work
with open(ABSOLUTE_PATH + 'appData/settings/config.txt', encoding='utf-8') as file:
    data = file.read().splitlines()
    SCHEDULE: Final[bool] = equality_parser(data[0], True)
    MANAGEMENT: Final[bool] = equality_parser(data[1], True)
    HEALTH: Final[bool] = equality_parser(data[2], True)

#Stylesheets reading
with open(ABSOLUTE_PATH + 'design/main.qss', encoding='utf-8') as file:
    stylesheet_main = file.read()

with open(ABSOLUTE_PATH + 'design/popup.qss', encoding='utf-8') as file:
    stylesheet_popup = file.read()


'''
Timetable of lessons or sessions or classes for a week.
Task list for an everyday usage. Probably with the timer or any other time controlling feature.
'''
#TODO Not even started yet
# if SCHEDULE:
#     with open(ABSOLUTE_PATH + 'appData/settings/schedule/schedule_settings.txt') as file:
#         data = file.read().splitlines()
#         SCHEDULE_SETTINGS: Final[dict] = 0 #??????????????????????????????????
#         TIMETABLE_SETTINGS = {"is_on": equality_parser(data[0], True),\
#             "messaging": False if not equality_parser(data[0], True) else equality_parser(data[1], True)}
#         TASK_LIST_SETTINGS = {"is_on": equality_parser(data[2], True),\
#             "messaging": False if not equality_parser(data[2], True) else equality_parser(data[3], True)}
#     if TIMETABLE_SETTINGS['is_on']:
#         with open(ABSOLUTE_PATH + 'appData/settings/schedule/schedule.json') as file:
#             TIMETABLE: Final[dict] = load(file)
#     if TASK_LIST_SETTINGS['is_on']:
#         with open(ABSOLUTE_PATH + 'appData/settings/schedule/everyday_routine.json') as file:
#             TASK_LIST: Final[dict] = load(file)
#     with open(ABSOLUTE_PATH + 'appData/settings/schedule/goals.json') as file:
#         data = load(file)
#         GOALS: Final[dict] = {goal: date(int(day.split('.')[2]), int(day.split('.')[1]),  int(day.split('.')[0])) for goal, day in data.items()}
        

'''
Main and the special part of programm. Probably can be used to track all the computer processes 
if modified, but here only tracks processes that (user answered) are not system processes
and logs them into different date related files. Than shows the statistics about them (how much time user
had spent on those programms). If user set these in settings, can stop processes user overspent time on 
today and recalculate the norm depending on over and underconsumption of norm a couple of days ago.
'''
if MANAGEMENT:
    with open(ABSOLUTE_PATH + 'appData/settings/management/norm.txt', encoding='utf-8') as file:
        data = file.read().splitlines()
        #parsing bars for process types that programm will trace and all types
        BARS = [type_[:type_.find(' = ')] for type_ in data if equality_parser(type_, True)]
        ALL_BARS: Final[list] = [type_[:type_.find(' = ')] for type_ in data]

    with open(ABSOLUTE_PATH + 'appData/settings/management/formula.txt', encoding='utf-8') as file:
        data = file.read().splitlines()
        CONSUMPTION_RECALCULATOR: Final[bool] = equality_parser(data[0], True)
    #Consumption recalculator takes formula with two variables that shows the change of transition of under 
    # and overconsumption of some process types to next few days
    if CONSUMPTION_RECALCULATOR:
        DAYS_OVERCONSUMPTION:     Final[int] = int(equality_parser(data[2]))
        OVERCONSUMPTION_FORMULA:  Final[str] =     equality_parser(data[3])
        DAYS_UNDERCONSUMPTION:    Final[int] = int(equality_parser(data[5]))
        UNDERCONSUMPTION_FORMULA: Final[str] =     equality_parser(data[6])
        with open(ABSOLUTE_PATH + 'appData/settings/management/norm_schedule.json', encoding='utf-8') as file:
            NORM_SCHEDULE: Final[dict] = load(file)
        with open(ABSOLUTE_PATH + 'appData/settings/management/norm_settings.txt', encoding='utf-8') as file:
            data = file.read().splitlines()
            NORM_SETTINGS = {type_[:type_.find(' = ')]:{} for type_ in data} 
            #Creating global dictionary with settings for each process type including if it has maximum or minimum border per day, 
            # if it needs to bbe stopped after overconsumption, after what time it needs to be stopped, which increasement is possible
            # for user to handle with maximally
            for index, bar in enumerate(NORM_SETTINGS.keys()):
                line = equality_parser(data[index]).split(',')
                NORM_SETTINGS[bar] = {'bar_type': True if line[0].strip() == 'Straight' else False, \
                    'is_stopable': True if line[1].strip() == 'Stopable' else False, \
                    'stop_time': int(line[2].strip()), \
                    'max_increasment': int(line[3].strip())} #TODO Needs to be implemented

'''
Small messaging part that will remind user to do eye gimnastics or whatever.
'''
#TODO Not even started yet
if HEALTH:
    with open(ABSOLUTE_PATH + 'appData/settings/health/norm.txt', encoding='utf-8') as file:
        data = file.read().splitlines()
        HEALTH_SETTINHS = {}
        for line in data:
            settings = equality_parser(line).split(',')
            if boolean_reader(settings[0].strip()):
                HEALTH_SETTINHS[line[:line.find(' = ')]] = [settings[1].strip(), int(settings[2].strip())]