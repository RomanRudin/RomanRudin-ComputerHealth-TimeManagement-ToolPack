from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel, QPushButton, QLineEdit, QListWidget
from datetime import date
from appData.settings.settings_parser import TIMETABLE_SETTINGS, TASK_LIST_SETTINGS, GOALS, ABSOLUTE_PATH
from apps.pyqt_module import delete_items_of_layout
from json import dump, load

class Schedule(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()


        self.goals = QListWidget()
        self.goals.addItems(GOALS.keys())
        self.goals.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.goals)


        today_layout = QHBoxLayout()
        main_layout.addLayout(today_layout)
        tomorrow_layout = QHBoxLayout()
        main_layout.addLayout(tomorrow_layout)


        if TIMETABLE_SETTINGS['is_on']:
            from appData.settings.settings_parser import TIMETABLE
            
            with open(ABSOLUTE_PATH + 'log/dataLogs/schedule_log.json') as file:
                TIMETABLE_SAVED = load(file)
            if TIMETABLE_SAVED['date'] != str(date.today()):
                a, b, c = map(int, TIMETABLE_SAVED['date'].split('-'))
                if (date.today() - date(a, b, c)).days == 1:
                    TIMETABLE_SAVED['today'] = TIMETABLE_SAVED['tomorrow']
                else:
                    TIMETABLE_SAVED['today'] = TIMETABLE[str(date.today().weekday())]
                TIMETABLE_SAVED['tomorrow'] = TIMETABLE[str((date.today().weekday() + 1) % 7)]
                with open(ABSOLUTE_PATH + 'log/dataLogs/schedule.json', 'w', encoding='utf-8') as file:
                    TIMETABLE_SAVED['date'] = str(date.today())
                    dump(TIMETABLE_SAVED, file)

            self.timetable_today = QVBoxLayout()
            today_layout.addLayout(self.timetable_today)
            self.__construct_timetable(self.timetable_today, TIMETABLE[str(date.today().weekday())])

            self.timetable_tomorrow = QVBoxLayout()
            tomorrow_layout.addLayout(self.timetable_tomorrow)
            self.__construct_timetable(self.timetable_tomorrow, TIMETABLE[str((date.today().weekday() + 1) % 7)])


        if TASK_LIST_SETTINGS['is_on']:
            from appData.settings.settings_parser import TASK_LIST
            self.task_list_today = QVBoxLayout()
            today_layout.addLayout(self.task_list_today)
            
            self.task_list_tomorrow = QVBoxLayout()
            tomorrow_layout.addLayout(self.task_list_tomorrow)
            with open(ABSOLUTE_PATH + 'log/dataLogs/task_log.json') as file:
                TASK_LIST_SAVED = load(file)
                        
            if TASK_LIST_SAVED['date'] != str(date.today()):
                a, b, c = map(int, TASK_LIST_SAVED['date'].split('-'))
                if (date.today() - date(a, b, c)).days == 1:
                    TASK_LIST_SAVED['today'] = TASK_LIST_SAVED['tomorrow']
                else:
                    TASK_LIST_SAVED['today'] = TASK_LIST[str(date.today().weekday())]
                TASK_LIST_SAVED['tomorrow'] = TASK_LIST[str((date.today().weekday() + 1) % 7)]
                with open(ABSOLUTE_PATH + 'log/dataLogs/task_log.json', 'w', encoding='utf-8') as file:
                    TASK_LIST_SAVED['date'] = str(date.today())
                    dump(TASK_LIST_SAVED, file)

            self.__construct_task_list(self.task_list_today, TASK_LIST_SAVED['today'])
            self.__construct_task_list(self.task_list_tomorrow, TASK_LIST_SAVED['tomorrow'])      


        self.setLayout(main_layout)



    def __construct_timetable(self, parent, data):
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
        button_line = QHBoxLayout()

        add_once_button = QPushButton()
        add_once_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        add_once_button.setDisabled(True)
        button_line.addWidget(add_once_button)
        add_button = QPushButton()
        add_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        add_button.setDisabled(True)
        button_line.addWidget(add_button)
        adding_box = QLineEdit()
        adding_box.setPlaceholderText('abcdef')
        adding_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        last_line.addWidget(adding_box)
        time_start_line = QLineEdit()
        time_start_line.setPlaceholderText('abcdef')
        time_start_line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        last_line.addWidget(time_start_line)
        time_end_line = QLineEdit()
        time_end_line.setPlaceholderText('abcdef')
        time_end_line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        last_line.addWidget(time_end_line)

        adding_box.editingFinished.connect(lambda: self.enabling_line(False, time_start_line))
        time_start_line.editingFinished.connect(lambda: self.enabling_line(False, time_end_line))
        time_end_line.editingFinished.connect(lambda: self.enabling_buttons(False, (add_once_button, add_button)))
        add_once_button.clicked.connect(lambda: self.add_case(parent, True, (adding_box, time_start_line, time_end_line), (add_once_button, add_button)))
        add_button.clicked.connect(lambda: self.add_case(parent, False, (adding_box, time_start_line, time_end_line), (add_once_button, add_button)))

        last_line.addLayout(button_line)

        parent.addLayout(last_line)


    def __construct_task_list(self, parent, data): #TODO
        for task, complition in data.items():
            line = QHBoxLayout()
            
            completed_button = QPushButton()
            completed_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            line.addWidget(completed_button)
            completed_button.clicked.connect(lambda: self.task_completed(line, complition))
            case_name = QLabel(task)
            case_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            line.addWidget(case_name)
            del_button = QPushButton()
            del_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            line.addWidget(del_button)
            del_button.clicked.connect(lambda: delete_items_of_layout(line))

            self.task_completed(line, not complition)
    
            parent.addLayout(line)

        last_line = QVBoxLayout()
        button_line = QHBoxLayout()

        add_once_button = QPushButton()
        add_once_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        add_once_button.setDisabled(True)
        button_line.addWidget(add_once_button)

        add_button = QPushButton()
        add_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        add_button.setDisabled(True)
        button_line.addWidget(add_button)

        adding_box = QLineEdit()
        adding_box.setPlaceholderText('abcdef')
        adding_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        last_line.addWidget(adding_box)

        adding_box.editingFinished.connect(lambda: self.enabling_task_buttons(False, (add_once_button, add_button)))
        add_once_button.clicked.connect(lambda: self.add_task(parent, True, adding_box, (add_once_button, add_button)))
        add_button.clicked.connect(lambda: self.add_task(parent, False, adding_box, (add_once_button, add_button)))

        last_line.addLayout(button_line)

        parent.addLayout(last_line)


    def add_task(self, parent, once, line, buttons):
        self.enabling_task_buttons(True, buttons)


    def add_case(self, parent, once, lines, buttons):
        self.enabling_task_buttons(True, buttons)
        for index, line in enumerate(lines):
            if index >= 1:
                self.enabling_line(True, line)


    def enabling_line(self, is_enabled, line):
        line.setDisabled(is_enabled)


    def enabling_buttons(self, is_enabled, buttons):
        for button in buttons:
            button.setDisabled(is_enabled)


    def task_completed(self, parent, completed):
        pass