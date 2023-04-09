from sqlite3 import connect
from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QVBoxLayout, QSizePolicy, QLabel
from PyQt5.QtCore import Qt
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
        button.clicked.connect(self.__close)

        self.setLayout(main_layout)

    def __close(self):
        self.close()



class Health_popup_standart(QWidget):
    def __init__(self, name):
        super().__init__()
        self.stay_time = 5
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        main_layout = QVBoxLayout()

        label = QLabel(f'Stay focused on your health! Do a {name}')
        main_layout.addWidget(label)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.setLayout(main_layout)
        self.__close()


    def __close(self):
        sleep(self.stay_time)
        self.close()
