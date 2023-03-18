from datetime import datetime
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QLabel, QApplication
from apps.health import Health
from apps.schedule import Schedule
from apps.time_managment import Management
from apps.settings_window import Settings
from apps.module import *
from appData.constants.constants import WEEKDAY_LIST
from appData.settings.settings_parser import SCHEDULE, HEALTH, MANAGEMENT
from sys import argv, exit

class Window(QWidget):
    def __init__(self):
        self.main_layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()

        #button
        if SCHEDULE:
            self.schedule = QPushButton('Schedule')
            self.button_layout.addWidget(self.schedule, stretch=3)
            self.schedule.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.schedule.clicked.connect(self.show_schedule)
        if MANAGEMENT:
            self.management = QPushButton('Time management')
            self.button_layout.addWidget(self.management, stretch=3)
            self.management.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.management.clicked.connect(self.show_management)
        if HEALTH:
            self.health = QPushButton('Health')
            self.button_layout.addWidget(self.health, stretch=3)
            self.health.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.health.clicked.connect(self.show_health)
        self.settings = QPushButton('settings')
        self.button_layout.addWidget(self.settings, stretch=3)
        self.settings.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.settings.clicked.connect(self.show_settings)

        self.date = QLabel(WEEKDAY_LIST[datetime.today().weekday() - 1])
        self.main_layout.addWidget(self.health)
        self.date.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.content = QWidget()
        self.main_layout.addWidget(self.content)
        self.content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)


    def show_schedule(self):
        self.content = Schedule()


    def show_management(self):
        self.content = Management()


    def show_health(self):
        self.content = Health()

    def show_settings(self):
        self.content = Settings()

if __name__ == "__main__":
    app = QApplication([argv]) 
    main = Window()
    main.resize(600, 400)
    main.show()        
    exit(app.exec_())