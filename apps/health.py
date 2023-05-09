from sqlite3 import connect
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QSizePolicy, QLabel, QDesktopWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtMultimedia import QSound
from time import sleep

class Health(QWidget):
    def __init__(self):
        super().__init__()


#Special popup window (with interactive button to force user to do what programm wants him to do)
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

        self.setFixedSize(400, 300)
        self.sound()

        self.setLayout(main_layout)

    #Sound playing
    def sound(self):
        QSound.play("appData/constants/media/health_special.wav")

    #Closing window
    def closing(self):
        self.close()


#Standart popup window (without any interactive widgets, just clear information on the screen)
class Health_popup_standart(QWidget):
    def __init__(self, name):
        super().__init__()
        self.stay_time = 3
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        main_layout = QVBoxLayout()

        label = QLabel(f'Stay focused on your health! Please, do {name} exersize')
        main_layout.addWidget(label)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.setFixedSize(400, 300)
        self.set_location_on_screen()
        self.sound()

        self.setLayout(main_layout)

        #closing window in self.stay_time seconds
        timer = QTimer(self)
        timer.setInterval(1000)
        timer.timeout.connect(self.closing)
        timer.start()
        
    #Moving window to bottom right corner
    def set_location_on_screen(self):
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()
        widget = self.geometry()
        
        x = ag.width() - widget.width()
        y = 2 * ag.height() - sg.height() - widget.height()
        self.move(x, y)

    #Sound playing
    def sound(self):
        QSound.play("appData\constants\media\health_standart.wav")

    #Closing window
    def closing(self):
        if self.stay_time <= 0:
            self.close()
        self.stay_time -= 1
