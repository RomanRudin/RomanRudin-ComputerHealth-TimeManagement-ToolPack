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
    pass


if MANAGEMENT:
    with open('appData/settings/management/norm.txt', encoding='utf-8') as file:
        BARS = [type_[:type_.find(' = ')] for type_ in file.read().splitlines() if equality_parser(type_, True)]

    with open('appData/settings/management/formula.txt', encoding='utf-8') as file:
        data = file.read().splitlines()
        OVERCONSUMPTION_RECALCULATOR, UNDERCONSUMPTION_RECALCULATOR = equality_parser(data[0], True), equality_parser(data[4], True)
        if OVERCONSUMPTION_RECALCULATOR:
            DAYS_OVERCONSUMPTION, OVERCONSUMPTION_FORMULA = int(equality_parser(data[1])), equality_parser(data[2])
        if UNDERCONSUMPTION_RECALCULATOR:
            DAYS_UNDERCONSUMPTION, UNDERCONSUMPTION_FORMULA = int(equality_parser(data[5])), equality_parser(data[6])


if HEALTH:
    pass