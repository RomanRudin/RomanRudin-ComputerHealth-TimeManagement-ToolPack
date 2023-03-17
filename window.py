from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy
from apps.health import Health
from apps.schedule import Schedule
from apps.time_managment import Management
from apps.module import *

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

        self.content = QWidget()

        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

    def show_schedule(self):
        self.content = Schedule()

    def show_management(self):
        self.content = Management()

    def show_health(self):
        self.content = Health()