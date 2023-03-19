'''
If you want to read False as False from file in Python, you gonna need to use this crunch, because only empty sting will return False if converted to bool
'''
def normal_reader(text):
    if text.lower().capitalize() == 'False':
        return False
    return True


with open('appData/settings/config.txt', encoding='utf-8') as file:
    data = file.read().splitlines()
    SCHEDULE = normal_reader(data[0][data[0].find(' = ') + 3:])
    MANAGEMENT = normal_reader(data[1][data[1].find(' = '):])
    HEALTH = normal_reader(data[2][data[2].find(' = '):])



if SCHEDULE:
    pass


if MANAGEMENT:
    with open(f'appData/settings/management/norm.txt', encoding='utf-8') as file:
        BARS = [type_[:type_.find(' = ')] for type_ in file.read().splitlines() if normal_reader(type_[type_.find(' = ') + 3:])]


if HEALTH:
    pass