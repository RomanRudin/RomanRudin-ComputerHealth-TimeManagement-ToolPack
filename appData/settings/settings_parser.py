from json import load

'''
If you want to read False as False from file in Python, you gonna need to use this crunch, because only empty sting will return False if converted to bool
'''
def boolean_reader(text):
    if text.lower().capitalize() == 'False':
        return False
    return True

def equality_parser(text, boolean=False):
    value = text[text.find(' = ') + 3:]
    if boolean:
       return boolean_reader(value)
    return value

#reading main config file, containing which sections of programms are going to work
with open('appData/settings/config.txt', encoding='utf-8') as file:
    data = file.read().splitlines()
    SCHEDULE = equality_parser(data[0], True)
    MANAGEMENT = equality_parser(data[1], True)
    HEALTH = equality_parser(data[2], True)
    LEARNING = equality_parser(data[2], True)


'''
Timetable of lessons or sessions or classes for a week.
Task list for an everyday usage. Probably with the timer or any other time controlling feature.
'''
#TODO Not even started yet
if SCHEDULE:
    with open('appData/settings/schedule/schedule_settings.txt') as file:
        SCHEDULE_SETTINGS = file.read().splitlines()
    with open('appData/settings/schedule/schedule.json') as file:
        TIMETABLE = load(file)

'''
Main and the special part of programm. Probably can be used to track all the computer processes 
if modified, but here only tracks processes that (user answered) are not system processes
and logs them into different date related files. Than shows the statistics about them (how much time user
had spent on those programms). If user set these in settings, can stop processes user overspent time on 
today and recalculate the norm depending on over and underconsumption of norm a couple of days ago.
'''
if MANAGEMENT:
    with open('appData/settings/management/norm.txt', encoding='utf-8') as file:
        data = file.read().splitlines()
        #parsing bars for process types that programm will trace and all types
        BARS = [type_[:type_.find(' = ')] for type_ in data if equality_parser(type_, True)]
        ALL_BARS = [type_[:type_.find(' = ')] for type_ in data]

    with open('appData/settings/management/formula.txt', encoding='utf-8') as file:
        data = file.read().splitlines()
        CONSUMPTION_RECALCULATOR = equality_parser(data[0], True)
    #Consumption recalculator takes formula with two variables that shows the change of transition of under 
    # and overconsumption of some process types to next few days
    if CONSUMPTION_RECALCULATOR:
        DAYS_OVERCONSUMPTION, OVERCONSUMPTION_FORMULA = int(equality_parser(data[2])), equality_parser(data[3])
        DAYS_UNDERCONSUMPTION, UNDERCONSUMPTION_FORMULA = int(equality_parser(data[5])), equality_parser(data[6])
        with open('appData/settings/management/norm_schedule.json', encoding='utf-8') as file:
            NORM_SCHEDULE = load(file)
        with open('appData/settings/management/norm_settings.txt', encoding='utf-8') as file:
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
    with open('appData/settings/health/norm.txt', encoding='utf-8') as file:
        data = file.read().splitlines()
        HEALTH_SETTINHS = {'Special': {}, 'Standart': {}}
        for line in data:
            settings = equality_parser(line).split(',')
            if boolean_reader(settings[1].strip()):
                HEALTH_SETTINHS[settings[0].strip()][line[:line.find(' = ')]] = 0

'''
In case I have 1,5 months left 'till ЕГЭ - russian main students exam. I'm stupid, yeah...
Reminder (in future (in my dreams) after adding web-scrapping possibility - small student book)
to make some random exersizes depending on today's norm and those exersizes difficulty and user 
preferences, set by user in special settings.
'''
#TODO JUST MAKE IT ALREADY U BASTARD!
if LEARNING: 
    pass