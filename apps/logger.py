from datetime import datetime, date
from os import system, popen, makedirs, path
from venv import create

class Log():
    def __init__(self, dir):
        self.dir = dir
        self.path = f'{dir}/{date.today()}.txt'
        self.types = f''
        self.logs = self.__read()
        '''
        {
            procces: [type, time, id],
        }
        '''

    def write(self):
        if not path.exists(self.path):
            makedirs(self.dir)
        with open(self.path, 'w', encoding='utf-8') as file:
            self.logs = dict(sorted(self.logs.items(), key=lambda item: item[1][1], reverse=True))
            text = ''
            for process, data in self.logs.items():
                print(process, data)
                text += f'{str(data[0])} \t {str(data[1])} \t {str(process)} \t {str(data[2])} \n' 
            file.write(text)



    def __read(self):
        if path.exists(self.path):
            with open(self.path, 'r', encoding='utf-8') as file:
                return {process: [type_, int(time), id]  for type_, time, process, id in (line.split('\t') for line in file.read().splitlines())}
        return {}
