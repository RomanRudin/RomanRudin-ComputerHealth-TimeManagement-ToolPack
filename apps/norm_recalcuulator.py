from datetime import date, timedelta
from appData.settings.settings_parser import OVERCONSUMPTION_RECALCULATOR, UNDERCONSUMPTION_RECALCULATOR, BARS



def formula_reader(formula, data):
    pass



overconsumption_list = {}
underconsumption_list = {}

ocerconsumption_sum = {}
underconsumption_sum = {}



if OVERCONSUMPTION_RECALCULATOR:
    from appData.settings.settings_parser import DAYS_OVERCONSUMPTION, OVERCONSUMPTION_FORMULA
    
    for bar in BARS:
        overconsumption_list.update({bar: {}})

    for day in range(DAYS_OVERCONSUMPTION):
        with open(f'log/{date.today() - timedelta(days=day)}', encoding='utf-8') as file:
            data = file.read().splitlines()
            for bar in BARS:
                overconsumption_list[bar].update({day:formula_reader(OVERCONSUMPTION_FORMULA, sum(int(time.strip()) \
                    for type_, time, _process, _id in (line.strip().split('\t') \
                    for line in data) \
                    if type_.strip() == bar))})



if UNDERCONSUMPTION_RECALCULATOR:
    from appData.settings.settings_parser import DAYS_UNDERCONSUMPTION, UNDERCONSUMPTION_FORMULA

    for day in range(DAYS_UNDERCONSUMPTION):
        pass
