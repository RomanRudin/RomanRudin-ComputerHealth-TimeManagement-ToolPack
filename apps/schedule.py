from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel, QPushButton, QComboBox
from datetime import date
from appData.settings.settings_parser import TIMETABLE_SETTINGS, TASK_LIST_SETTINGS
from apps.pyqt_module import delete_items_of_layout
from json import dump

class Schedule(QWidget):
    def __init__(self) -> None:
        super().__init__()
        main_layout = QVBoxLayout()
        today_layout = QHBoxLayout()
        main_layout.addLayout(today_layout)
        tomorrow_layout = QHBoxLayout()
        main_layout.addLayout(tomorrow_layout)


        if TIMETABLE_SETTINGS['is_on']:
            from appData.settings.settings_parser import TIMETABLE

            self.timetable_today = QVBoxLayout()
            today_layout.addLayout(self.timetable_today)
            self.__construct_timetable(self.timetable_today, TIMETABLE[str(date.today().weekday())])

            self.timetable_tomorrow = QVBoxLayout()
            tomorrow_layout.addLayout(self.timetable_tomorrow)
            self.__construct_timetable(self.timetable_tomorrow, TIMETABLE[str((date.today().weekday() + 1) % 7)])


        if TASK_LIST_SETTINGS['is_on']:
            from appData.settings.settings_parser import TASK_LIST_SAVED
            self.task_list_today = QVBoxLayout()
            today_layout.addLayout(self.task_list_today)
            
            self.task_list_tomorrow = QVBoxLayout()
            tomorrow_layout.addLayout(self.task_list_tomorrow)
                        
            if TASK_LIST_SAVED['date'] != str(date.today()):
                from appData.settings.settings_parser import TASK_LIST
                a, b, c = map(int, TASK_LIST_SAVED['date'].split('-'))
                if (date.today() - date(a, b, c)).days == 1:
                    TASK_LIST_SAVED['today'] = TASK_LIST_SAVED['tomorrow']
                else:
                    TASK_LIST_SAVED['today'] = TASK_LIST[str(date.today().weekday())]
                TASK_LIST_SAVED['tomorrow'] = TASK_LIST[str((date.today().weekday() + 1) % 7)]
                with open('appData/settings/schedule/tasks_log.json', 'w', encoding='utf-8') as file:
                    TASK_LIST_SAVED['date'] = str(date.today())
                    dump(TASK_LIST_SAVED, file)

            self.__construct_task_list(self.task_list_today, TASK_LIST_SAVED['today'])
            self.__construct_task_list(self.task_list_tomorrow, TASK_LIST_SAVED['tomorrow'])      


        self.setLayout(main_layout)



    def __construct_timetable(self, parent, data):
        for case, time in data.items():
            line = QHBoxLayout()

            print(case)

            case_name = QLabel(case)
            case_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            line.addWidget(case_name)
            time_start = QLabel(str(time[0]))
            time_start.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            line.addWidget(time_start)
            time_end = QLabel(str(time[1]))
            time_end.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            line.addWidget(time_end)
            del_button = QPushButton()
            del_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            line.addWidget(del_button)
            del_button.clicked.connect(lambda: delete_items_of_layout(line))

            parent.addLayout(line)
        
        last_line = QHBoxLayout()

        add_once_button = QPushButton()
        add_once_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        last_line.addWidget(add_once_button)
        add_once_button.clicked.connect(lambda: self.add_case(parent, True))

        add_button = QPushButton()
        add_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        last_line.addWidget(add_button)
        add_button.clicked.connect(lambda: self.add_case(parent, False))

        parent.addLayout(last_line)
        print(parent.children())


    def __construct_task_list(self, parent, data): #TODO
        for case, time in data.items():
            line = QHBoxLayout()

            case_name = QLabel(case)
            case_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            line.addWidget(case_name)
            time_start = QLabel(str(time[0]))
            time_start.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            line.addWidget(time_start)
            time_end = QLabel(str(time[1]))
            time_end.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            line.addWidget(time_end)
            del_button = QPushButton()
            del_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            line.addWidget(del_button)
            del_button.clicked.connect(lambda: delete_items_of_layout(line))

            parent.addLayout(line)
        
        last_line = QHBoxLayout()
        add_once_button = QPushButton()
        add_once_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        last_line.addWidget(add_once_button)
        add_once_button.clicked.connect(lambda: self.add_case(parent, True))

        add_button = QPushButton()
        add_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        last_line.addWidget(add_button)
        add_button.clicked.connect(lambda: self.add_case(parent, False))

        parent.addLayout(last_line)


    def add_task(self, parent, once):
        pass


    def add_case(self, parent, once):
        pass