from datetime import date
from os import makedirs, path

class Log():
    def __init__(self, dir) -> None:
        self.dir = dir
        self.path = f'{dir}/{date.today()}.txt'
        self.types = f''
        self.logs = self.__read()
        self.new_session = True
        '''
        {
            procces: [type, time, id],
        }
        '''

    def write(self):
        self.new_session = False
        if not path.exists(self.dir):
            makedirs(self.dir)
        with open(self.path, 'w', encoding='utf-8') as file:
            self.logs = dict(sorted(self.logs.items(), key=lambda item: item[1][1], reverse=True))
            text = ''
            for process, data in self.logs.items():
                text += f'{str(data[0])} \t {str(data[1])} \t {str(process)} \t {str(data[2])} \n' 
            file.write(text)
            print(text)



    def __read(self):
        if path.exists(self.path):
            with open(self.path, 'r', encoding='utf-8') as file:
                return {process.strip(): [type_.strip(), int(time.strip()), id.strip()] \
                    for type_, time, process, id in (line.strip().split('\t') \
                    for line in file.read().splitlines())}

        return {}
