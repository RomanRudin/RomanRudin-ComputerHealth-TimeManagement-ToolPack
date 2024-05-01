 #!
#todo
#todo
#todo
#todo
#todo
#todo
#todo
#todo
#todo
from PyQt5.QtWidgets import QApplication, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QListWidget, QListWidgetItem, QSizePolicy
from datetime import datetime
from sys import argv, exit
from json import dump, load

STATISTICS_DAYS = [0, 1, 3, 7]
DELETE_ADTER = 28  

#FOrmatting of data.json:
#
# data = {
#   task_name_1: {
#       "is_done": bool,
#       "deadline": datetime,
#       "importance": int,
#       "value": int,
#       "finished": datetime,
#   },
#   task_name_2: {
#       ...
#   }.
#   ...
# }


class Schedule(QWidget):
    def __init__(self): #path: str):
        super().__init__()
        
        self.data = self.read_data()

        self.main_layout = QHBoxLayout()

        self.statistics_layout = QVBoxLayout()        
        self.main_layout.addLayout(self.statistics_layout, stretch=1)
        
        self.tasks_layout = QVBoxLayout()
        tasks_label = QLabel("Tasks")
        tasks_label.setObjectName('tasks_main_label')
        tasks_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tasks_layout.addWidget(tasks_label)
        self.main_layout.addLayout(self.tasks_layout, stretch=2)

        self.tasks_list = QListWidget()
        self.tasks_layout.addWidget(self.tasks_list, stretch=20)
        self.tasks_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        buuton_layout = QHBoxLayout()
        self.tasks_layout.addLayout(buuton_layout, stretch=2)
        self.add_task_button = QPushButton("Add task")
        self.save_button = QPushButton("Save")
        self.add_task_button.setObjectName('add_task_button')
        self.save_button.setObjectName('save_button')
        self.add_task_button.clicked.connect(self.add_task)
        self.save_button.clicked.connect(self.reset)
        self.add_task_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.save_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        buuton_layout.addWidget(self.add_task_button, stretch=2)
        buuton_layout.addWidget(self.save_button, stretch=1)

        self.construct()
        self.setLayout(self.main_layout)

    def construct(self):
        #Statistics part:
        statistics_label = QLabel("Statisticsr")
        statistics_label.setObjectName('statistics_main_label')
        statistics_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.statistics_layout.addWidget(statistics_label)
        for index, days in enumerate(STATISTICS_DAYS):
            statistics_panel = Statistics_panel(days, self)
            statistics_panel.setObjectName('statistics_panel')
            statistics_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.statistics_layout.addWidget(statistics_panel, stretch=(20 // len(STATISTICS_DAYS)))
            if (index != len(STATISTICS_DAYS) - 1):
                spacer = QLabel()
                self.statistics_layout.addWidget(spacer, stretch=(12 // (len(STATISTICS_DAYS) - 1)))
                
        #tasks part:
        for task, name in [[self.data[elem], elem] for elem in self.data.keys() if 
                        ((not self.data[elem]["is_done"]) and (datetime.strptime(self.data[elem]["deadline"], "%d%m%Y") >= datetime.today()))]:
            new_task = Task(name=str(name), deadline=task["deadline"],
                            importance=task["importance"], value=task["value"],
                            is_done=task["is_done"], parent=self)
            # Clutch, that helps me customize QListWidgtItems 
            listWidgetItem = QListWidgetItem(self.tasks_list)
            listWidgetItem.setSizeHint(new_task.sizeHint())
            self.tasks_list.addItem(listWidgetItem)
            self.tasks_list.setItemWidget(listWidgetItem, new_task)

    def reset(self):
        self.save()
        self.clear()
        self.construct()

    def __delete_items_of_layout(self, layout) -> None:
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.__delete_items_of_layout(item.layout())

    def clear(self):
        self.tasks_list.clear()
        self.__delete_items_of_layout(self.statistics_layout)

    def read_data(self) -> dict: 
        with open('data.json', 'r', encoding='utf-8') as file:
            return load(file)

    def add_task(self):
        new_task = Task(name="", deadline="".join(str(datetime.today().date()).split("-")[::-1]),
                            importance=1, value=1,
                            is_done=False, parent=self)
        listWidgetItem = QListWidgetItem(self.tasks_list)
        listWidgetItem.setSizeHint(new_task.sizeHint())
        self.tasks_list.addItem(listWidgetItem)
        self.tasks_list.setItemWidget(listWidgetItem, new_task)

    def save(self):
        with open('data.json', 'w', encoding='utf-8') as file:
            dump(self.data, file, indent=4)




class Statistics_panel(QWidget):
    def __init__(self, days: int, parent: Schedule) -> None:
        super().__init__()
        main_layout = QVBoxLayout()       
        self.setLayout(main_layout)

        self.days = days
        self.parent = parent
        self.data = self.get_data()

        label = QLabel(f"Last {days} days")
        label.setObjectName('statistics_labl')
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(label, stretch=1)
        stats = QHBoxLayout()
        main_layout.addLayout(stats, stretch=5)
        done = QLabel("Done: " + str(self.data["done"]))
        missed = QLabel("Missed: " + str(self.data["missed"]))
        score = QLabel("Score: " + str(self.data["score"]))
        done.setObjectName('statistics_done')
        missed.setObjectName('statistics_missed')
        score.setObjectName('statistics_score')
        done.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        missed.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        score.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        stats.addWidget(done)
        stats.addWidget(missed)
        stats.addWidget(score, stretch=2)
        
    def get_data(self) -> dict:
        data_statistiics = set()
        score = 0
        for elem, info in self.parent.data.items():
            if (info["is_done"] and (0 <= (datetime.today() - datetime.strptime(info["finished"], "%d%m%Y")).days  <= self.days)) :
                data_statistiics.add(elem)
                score += info["importance"] * info["value"]
            elif ((0 < (datetime.today() - datetime.strptime(info["deadline"], "%d%m%Y")).days <= self.days) and (not info["is_done"])):
                data_statistiics.add(elem)
                score -= info["importance"] * info["value"]
                
        return {
            "done": len([self.parent.data[name] for name in data_statistiics
                    if self.parent.data[name]["is_done"]]),
            "missed": len([self.parent.data[name] for name in data_statistiics
                    if ((not self.parent.data[name]["is_done"]) and 
                    (0 < (datetime.today() - datetime.strptime(info["deadline"], "%d%m%Y")).days <= self.days))]),
            "score": score
        }



class Task(QWidget):
    def __init__(self, name: str, deadline: datetime, importance: int, value: int, is_done: bool, parent: Schedule):
        super().__init__()
        main_layout = QHBoxLayout()       
        self.setLayout(main_layout)

        self.parent = parent 
        self.is_done = is_done

        self.done = QPushButton("Done") 
        self.done.setObjectName('task_done_button')
        self.done.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.done.clicked.connect(self.task_finished)
        main_layout.addWidget(self.done, stretch=2)
        if (self.is_done):
            self.done.setEnabled(False)

        self.name = QLineEdit()
        self.previous_name = name
        self.name.setText(name)
        self.name.setObjectName("task_name")
        self.name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.name.editingFinished.connect(self.change_name)
        main_layout.addWidget(self.name, stretch=5)
    
        self.deadline = QLineEdit()
        self.deadline.setText(str(datetime.strptime(deadline, "%d%m%Y").date()))
        self.deadline.setObjectName('task_deadline')
        self.deadline.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.deadline.editingFinished.connect(lambda: self.save_data_part("deadline", "".join(self.deadline.text().split("-")[::-1])))
        main_layout.addWidget(self.deadline, stretch=3)
        
        self.importance = QLineEdit()
        self.importance.setText(str(importance))
        self.importance.setObjectName('task_importace')
        self.importance.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.importance.editingFinished.connect(lambda: self.save_data_part("importance", int(self.importance.text())))
        main_layout.addWidget(self.importance, stretch=1)
        
        self.value = QLineEdit()
        self.value.setText(str(value))
        self.value.setObjectName('task_value')
        self.value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.value.editingFinished.connect(lambda: self.save_data_part("value", int(self.value.text())))
        main_layout.addWidget(self.value, stretch=1)

    def change_name(self):
        if (self.previous_name != ""):
            self.parent.data[self.name.text()] = self.parent.data.pop(self.previous_name)
            return
        self.parent.data[self.name.text()] = {
            "is_done": self.is_done, "deadline": "".join(self.deadline.text().split("-")[::-1]), 
            "importance": int(self.importance.text()), "value": int(self.importance.text()),
            "finished": "".join(str(datetime.today().date()).split("-")[::-1])}

    def save_data_part(self, key:str, data:any):
        if self.name.text() == "":
            return
        self.parent.data[self.name.text()][key] = data

    def task_finished(self):
        if self.done.isEnabled():
            self.done.setEnabled(False)
            self.is_done = True
            self.save_data_part("is_done", True)
            self.save_data_part("finished", "".join(str(datetime.today().date()).split("-")[::-1])) 
            return
        self.done.setEnabled(True)
        self.is_done = False
        self.save_data_part("is_done", True)    
    


if __name__ == "__main__":
    app = QApplication([argv]) 
    with open("style.qss", "r") as file:
        app.setStyleSheet(file.read())
    main = Schedule()
    main.resize(1200, 800)
    main.show()        
    exit(app.exec_())