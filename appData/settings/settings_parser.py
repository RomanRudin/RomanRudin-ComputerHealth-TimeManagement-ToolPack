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


with open('appData/settings/config.txt', encoding='utf-8') as file:
    data = file.read().splitlines()
    SCHEDULE = equality_parser(data[0], True)
    MANAGEMENT = equality_parser(data[1], True)
    HEALTH = equality_parser(data[2], True)



if SCHEDULE:
    with open('appData/settings/schedule/schedule.json') as file:
        pass


if MANAGEMENT:
    with open('appData/settings/management/norm.txt', encoding='utf-8') as file:
        data = file.read().splitlines()
        BARS = [type_[:type_.find(' = ')] for type_ in data if equality_parser(type_, True)]
        ALL_BARS = [type_[:type_.find(' = ')] for type_ in data]

    with open('appData/settings/management/formula.txt', encoding='utf-8') as file:
        data = file.read().splitlines()
        CONSUMPTION_RECALCULATOR = equality_parser(data[0], True)
    if CONSUMPTION_RECALCULATOR:
        DAYS_OVERCONSUMPTION, OVERCONSUMPTION_FORMULA = int(equality_parser(data[2])), equality_parser(data[3])
        DAYS_UNDERCONSUMPTION, UNDERCONSUMPTION_FORMULA = int(equality_parser(data[5])), equality_parser(data[6])
        with open('appData/settings/management/norm_schedule.json', encoding='utf-8') as file:
            NORM_SCHEDULE = load(file)
        with open('appData/settings/management/norm_settings.txt', encoding='utf-8') as file:
            data = file.read().splitlines()
            NORM_SETTINGS = {type_[:type_.find(' = ')]:{} for type_ in data} 
            for index, bar in enumerate(NORM_SETTINGS.keys()):
                line = equality_parser(data[index]).split(',')
                NORM_SETTINGS[bar] = {'bar_type': True if line[0].strip() == 'Straight' else False, \
                    'is_stopable': True if line[1].strip() == 'Stopable' else False, \
                    'stop-time': int(line[2].strip())}


if HEALTH:
    pass