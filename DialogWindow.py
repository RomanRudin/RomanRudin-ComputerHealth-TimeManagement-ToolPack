from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QVBoxLayout, QSizePolicy, QLabel
from appData.constants.constants import PROCESS_TYPES
from json import dump

class DialogWindow(QWidget):
    def __init__(self, process, log, types) -> None:
        super().__init__()
        self.process = process
        self.log = log
        self.types = types

        self.process_added = False

        main_layout = QVBoxLayout()

        label = QLabel(f'New process found. What type of process is {self.process}?')
        main_layout.addWidget(label, stretch=2)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.list = QComboBox()
        main_layout.addWidget(self.list, stretch=2)
        self.list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.list.addItems(PROCESS_TYPES)
        self.list.addItem('System')

        self.ok = QPushButton('OK')
        self.ok.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.ok, stretch=1)
        self.ok.clicked.connect(self.__save)

        self.setLayout(main_layout)


    def __save(self):
        selected = self.list.currentText()
        if selected != '':
            if selected == 'System':
                with open(f'appData/processes/NonTrack.conf', 'a', encoding='utf-8') as file:
                    file.write('\n' + self.process)
                    self.close()

            else:
                with open(f'appData/processes/types.json', 'w', encoding='utf-8') as file:
                    self.types.update({self.process: selected})
                    dump(self.types, file, ensure_ascii=False, indent=4)
                    self.process_added = True
                    self.close()
