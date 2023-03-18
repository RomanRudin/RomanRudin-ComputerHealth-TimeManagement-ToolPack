from datetime import datetime
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QLabel
from apps.health import Health
from apps.schedule import Schedule
from apps.time_managment import Management
from apps.module import *
from appData.constants.constants import weekday_list
from PyQt5.QtWidgets import QApplication
from sys import argv, exit

class Window(QWidget):
    def __init__(self):
        self.main_layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()

        #button
        self.schedule = QPushButton('Schedule')
        self.button_layout.addWidget(self.schedule)
        self.schedule.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.management = QPushButton('Time management')
        self.button_layout.addWidget(self.management)
        self.management.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.health = QPushButton('Health')
        self.button_layout.addWidget(self.health)
        self.health.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.date = QLabel(weekday_list[datetime.today().weekday() - 1])
        self.main_layout.addWidget(self.health)
        self.date.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.content = QWidget()
        self.main_layout.addWidget(self.content)
        self.content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

        self.schedule.clicked.connect(self.show_schedule)
        self.management.clicked.connect(self.show_management)
        self.health.clicked.connect(self.show_health)



    def show_schedule(self):
        self.content = Schedule()


    def show_management(self):
        self.content = Management()


    def show_health(self):
        self.content = Health()

if __name__ == "__main__":
    app = QApplication([argv]) 
    main = Window()
    main.resize(600, 400)
    main.show()        
    exit(app.exec_())