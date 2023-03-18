with open('config.txt', encoding='utf8') as file:
    SCHEDULE = bool(file.readline()[file.readline().find(' = '):])
    MANAGEMENT = bool(file.readline()[file.readline().find(' = '):])
    HEALTH = bool(file.readline()[file.readline().find(' = '):])



if SCHEDULE:
    pass


if MANAGEMENT:
    with open(f'management/norm.txt', encoding='utf-8') as file:
        BARS = [type_[:type_.find(' = ')] for type_ in file.read().splitlines() if type_[type_.find(' = '):]]


if HEALTH:
    pass