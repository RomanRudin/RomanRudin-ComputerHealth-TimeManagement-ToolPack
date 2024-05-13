from datetime import date
from os import makedirs, path, remove, listdir

#main logger, used by main time manager file to save and load data from log files
class Log():
    def __init__(self, dir):
        self.dir = dir
        self.path = f'{dir}/{date.today()}.txt'
        self.logs = self.__read()
        self.__remove_previous()
        self.new_session = True
        '''
        {
            procces: [type, time],
        }
        '''

    def write(self) -> None:
        self.new_session = False
        if not path.exists(self.dir):
            makedirs(self.dir)
        with open(self.path, 'w', encoding='utf-8') as file:
            self.logs = dict(sorted(self.logs.items(), key=lambda item: item[1][1], reverse=True))
            text = ''
            for process, data in self.logs.items():
                text += f'{str(data[0])} \t {str(data[1])} \t {str(process)}\n' 
            file.write(text)



    def __read(self) -> dict:
        if path.exists(self.path):
            with open(self.path, 'r', encoding='utf-8') as file:
                return {process.strip(): [type_.strip(), int(time.strip())] \
                    for type_, time, process in (line.strip().split('\t') \
                    for line in file.read().splitlines())}

        return {}

    def __remove_previous(self) -> None:
        logs = [file for file in listdir(self.dir)]
        try:
            logs.pop(-1)
            if len(logs) > 28:
                for _ in range(len(logs) - 28):
                    remove(f'{self.dir}/{logs.pop(logs.index(logs[0]))}')
        except IndexError:
            raise IndexError

class TestLog(Log):
    def __init__(self, type):
        super().__init__(f'testLogs/{type}')