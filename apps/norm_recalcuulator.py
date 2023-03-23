from datetime import date, timedelta
from appData.settings.settings_parser import BARS, ALL_BARS, OVERCONSUMPTION_FORMULA, \
    UNDERCONSUMPTION_FORMULA, NORM_SCHEDULE, DAYS_OVERCONSUMPTION, DAYS_UNDERCONSUMPTION
from json import load, dump
from os import path


def formula_reader(formula, main, day):
    return eval(formula.replace('main', main).replace('day', day))


def consumption_recalculating():
    full_consumption_list = {} #{bar:{} for bar in ALL_BARS}
    consumption_list = {} #{bar:{'sum': 0} for bar in BARS}


    with open('log/dataLogs/norm_recalculation_data.json', encoding='utf-8') as file:
        data = load(file)

        max_days = max(DAYS_OVERCONSUMPTION, DAYS_UNDERCONSUMPTION)

        if data['date'] != str(date.today()):
            for day in range(max_days):
                if path.exists(f'log/{date.today() - timedelta(days=day + 1)}'):
                    with open(f'log/{date.today() - timedelta(days=day + 1)}', encoding='utf-8') as file:
                        reader = file.read().splitlines()
                        weekday = (date.today() - timedelta(days=day + 1)).weekday()
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
                            full_consumption_list[bar][day] = 0 - sum(int(time.strip()) \
                                for type_, time, _process, _id in (line.strip().split('\t') \
                                for line in reader) if type_.strip() == bar) \
                                + NORM_SCHEDULE[weekday]
            data = full_consumption_list.copy()
            dump(file, data, indent=4)

        for bar in BARS:
            for day in range(max_days):
                summ = full_consumption_list[bar][day]
                if summ < 0 and day <= DAYS_OVERCONSUMPTION - 1:
                    consumption_list[bar][day] = formula_reader(OVERCONSUMPTION_FORMULA, abs(summ), day)
                elif summ > 0 and day <= DAYS_UNDERCONSUMPTION - 1:
                    consumption_list[bar][day] = formula_reader(UNDERCONSUMPTION_FORMULA, summ, day)
            consumption_list[bar]['sum'] = sum(consumption_list[bar].values())
    return consumption_list
                