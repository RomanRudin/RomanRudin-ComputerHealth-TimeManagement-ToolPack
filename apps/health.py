from sqlite3 import connect
from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QVBoxLayout, QSizePolicy, QLabel
from PyQt5.QtCore import Qt, QTimer
from time import sleep

class Health(QWidget):
    def __init__(self):
        super().__init__()



class Health_popup_special(QWidget):
    def __init__(self, name):
        super().__init__()
        main_layout = QVBoxLayout()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        label = QLabel(f'Stay focused on your health! Do a {name}')
        main_layout.addWidget(label, stretch=2)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        button = QPushButton('ok')
        main_layout.addWidget(button, stretch=1)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button.clicked.connect(self.closing)

        self.setLayout(main_layout)

    def closing(self):
        self.close()



class Health_popup_standart(QWidget):
    def __init__(self, name):
        super().__init__()
        self.stay_time = 3
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        main_layout = QVBoxLayout()

        label = QLabel(f'Stay focused on your health! Do a {name}')
        main_layout.addWidget(label)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        timer = QTimer(self)
        timer.setInterval(1000)
        timer.timeout.connect(self.closing)
        timer.start()

        self.setLayout(main_layout)


    def closing(self):
        if self.stay_time <= 0:
            self.close()
        self.stay_time -= 1
