from datetime import date, timedelta
from appData.settings.settings_parser import BARS, ALL_BARS, OVERCONSUMPTION_FORMULA, \
    UNDERCONSUMPTION_FORMULA, NORM_SCHEDULE, DAYS_OVERCONSUMPTION, DAYS_UNDERCONSUMPTION, \
    NORM_SETTINGS
from json import load, dump
from os import path


def formula_reader(formula, main, day):
    return str(int(eval(formula.replace('main', str(main)).replace('day',  str(day)))))


def norm_recalculating():
    full_consumption_list = {bar:{} for bar in ALL_BARS}
    consumption_list = {bar:{'sum': 0} for bar in ALL_BARS}

    #getting las saved data about recalculations
    with open('log/dataLogs/norm_recalculation_data.json', encoding='utf-8') as file:
        data = load(file)
    #getting overhauled data from file
    with open('log/dataLogs/norm_overhaul_logs.json', encoding='utf-8') as file:
        norm = load(file)

    #getting the maximum "file date depth level" the programm will go
    max_days = max(DAYS_OVERCONSUMPTION, DAYS_UNDERCONSUMPTION)

    #reading data from files if no recalculations were made today yet
    if data['date'] != str(date.today()):
        for day in range(max_days):
            print(day)
            if path.exists(f'log/{date.today() - timedelta(days=day + 1)}.txt'):
                with open(f'log/{date.today() - timedelta(days=day + 1)}.txt', encoding='utf-8') as file:
                    reader = file.read().splitlines()
                weekday = str((date.today() - timedelta(days=day + 1)).weekday())
                logs_day = str(date.today() - timedelta(days=day + 1))
                print(logs_day)
                for bar in ALL_BARS:
                    '''
                    I'm so sorry for this line of code...
                    In full_consumption_list[bar][day] we need to have the difference between
                    time that you could spend on this type of activity this day (NORM_SCHEDULE[weekday])
                    and time you spent this day. If it is < 0, then we need to decrease noem for today, 
                    else - increase. 
                    Time you spent this day can be count like summary of all the time programms of this types
                    were working. We take lines in reader, split them into type_ and time (we don't really need
                    other variables) and, if type_ is the same with bar - we take time to sum().
                    '''
                    full_consumption_list[bar][str(day)] = 0 - sum(int(time.strip()) / 60 \
                       for type_, time, _process, _id in (line.strip().split('\t') \
                       for line in reader) if type_.strip() == bar)\
                       + NORM_SCHEDULE[weekday][bar]

                    #if overhauling system was working in recent days
                    if logs_day in norm.keys():
                        #unfortunately, overhauled system doesn't support reversed bars from the 'in-box' variant
                        if NORM_SETTINGS[bar]['bar_type']:
                            full_consumption_list[bar][str(day)] -= norm[logs_day][bar]
                        else:
                            full_consumption_list[bar][str(day)] += norm[logs_day][bar]

        #saving this data for fast acess
        with open('log/dataLogs/norm_recalculation_data.json', 'w', encoding='utf-8') as file:
            full_consumption_list['date'] = str(date.today())
            dump(full_consumption_list, file, indent=4)
            full_consumption_list.pop('date')

    else:
        #getting today's saved recalculations
        data.pop('date')
        full_consumption_list = data

    #recalculating block
    for bar in ALL_BARS:
        if bar in full_consumption_list.keys():
            for day in range(max_days):
                if str(day) in full_consumption_list[bar].keys():
                    summ = full_consumption_list[bar][str(day)]
                    #formula counting part
                    if not NORM_SETTINGS[bar]['bar_type']: #if bar is reversed
                        if summ > 0 and day <= DAYS_UNDERCONSUMPTION - 1:
                            consumption_list[bar][day] = formula_reader(OVERCONSUMPTION_FORMULA, abs(summ), day)
                        elif summ < 0 and day <= DAYS_OVERCONSUMPTION - 1:
                            consumption_list[bar][day] = formula_reader(UNDERCONSUMPTION_FORMULA, summ, day)
                    else:
                        if summ < 0 and day <= DAYS_OVERCONSUMPTION - 1:
                            consumption_list[bar][day] = formula_reader(OVERCONSUMPTION_FORMULA, abs(summ), day)
                        elif summ > 0 and day <= DAYS_UNDERCONSUMPTION - 1:
                            consumption_list[bar][day] = formula_reader(UNDERCONSUMPTION_FORMULA, summ, day)
            #counting summary of all the recalculated transitions of one bar
            consumption_list[bar]['sum'] = sum(int(value) for value in consumption_list[bar].values())
            #if recalculated norm is higher than the maximum possibly nirm for user
            if consumption_list[bar]['sum'] > (NORM_SCHEDULE[str(date.today().weekday())][bar] * NORM_SETTINGS[bar]['max_increasment']):
                consumption_list[bar]['sum'] = (NORM_SCHEDULE[str(date.today().weekday())][bar] * NORM_SETTINGS[bar]['max_increasment'])
    
    #changing overhauled logs because of new data
    with open('log/dataLogs/norm_overhaul_logs.json', 'w', encoding='utf-8') as file:
        for day in norm.keys():
            a, b, c = map(int, day.split('-'))
            if (date.today() - date(a, b, c)).days > 14:
                norm.pop(day)
        norm[str(date.today())] = {}
        for bar in ALL_BARS:
            norm[str(date.today())][bar] = consumption_list[bar]['sum']
        dump(norm, file, indent=4)

    return consumption_list
                