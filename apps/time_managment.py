from datetime import date
from PyQt5.QtWidgets import QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from appData.constants.constants import BAR1_COLORS, BAR2_COLORS
from random import randint
from main import log
from appData.settings.settings_parser import BARS, CONSUMPTION_RECALCULATOR, NORM_SCHEDULE, NORM_SETTINGS
from apps.norm_recalcuulator import norm_recalculating

class Management(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        changes_layout = QVBoxLayout()
        main_statistic_layout = QHBoxLayout()

        #plotting: plot for gaming, coding and learning
        self.statistic_in_spheres = plt.figure()
        self.statistic_in_spheres_canvas = FigureCanvasQTAgg(self.statistic_in_spheres)
        main_statistic_layout.addWidget(self.statistic_in_spheres_canvas, stretch=3)

        main_layout.addLayout(main_statistic_layout)

        #plotting: plot for top 10 programms you waqsted time on
        random_bar_colors = BAR2_COLORS.copy()
        self.statistic_of_programms = plt.figure()
        self.statistic_of_programms_canvas = FigureCanvasQTAgg(self.statistic_of_programms)
        main_layout.addWidget(self.statistic_of_programms_canvas, stretch=3)

        #choosing random colors for bars
        self.color_data = {
            'Game': random_bar_colors.pop(randint(0, len(random_bar_colors) - 1)),
            'Entartainment': random_bar_colors.pop(randint(0, len(random_bar_colors) - 1)),
            'Code': random_bar_colors.pop(randint(0, len(random_bar_colors) - 1)),
            'Learning': random_bar_colors.pop(randint(0, len(random_bar_colors) - 1)),
            'Browser': random_bar_colors.pop(randint(0, len(random_bar_colors) - 1)),
            'Social Network': random_bar_colors.pop(randint(0, len(random_bar_colors) - 1)),
            'Tool': random_bar_colors.pop(randint(0, len(random_bar_colors) - 1)),
        }


        if CONSUMPTION_RECALCULATOR:
            self.recalculated_norm = norm_recalculating()
            for bar in BARS:
                changes = QListWidget()
                changes_layout.addWidget(changes)
                changes.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                changes.addItems(value for key, value in self.recalculated_norm[bar].items() if key != 'sum' )
            main_statistic_layout.addLayout(changes_layout)

        self.setLayout(main_layout)
        self.plot()


    def refresh(self):
        pass


    def plot(self):
        self.statistic_in_spheres.clear()
        self.statistic_of_programms.clear()

        ax1 = self.statistic_in_spheres.add_subplot(111)
        ax2 = self.statistic_of_programms.add_subplot(111)


        time_in_sphere = {bar: sum(data[1] / 3600 for data in log.logs.values() if data[0] == bar) for bar in BARS}

        ax1.barh(list(time_in_sphere.keys()), list(time_in_sphere.values()), align='center', alpha=0.4, color=BAR1_COLORS)
        ax1.plot([NORM_SCHEDULE[str(date.today().weekday())][bar] / 60 for bar in list(time_in_sphere.keys())], list(time_in_sphere.keys()), marker='D', linestyle='none', alpha=0.8, color='red')
        #TODO make a plot-marker for changeable markers. Firstly I'll need to make a function, that will count those markers
        if CONSUMPTION_RECALCULATOR:
            recalculated_norm_list = [(NORM_SCHEDULE[str(date.today().weekday())][bar] - self.recalculated_norm[bar]['sum']) \
                for bar in list(time_in_sphere.keys())]
            recalculated_norm_list = [num / 60 if num > 0 else 0 for num in recalculated_norm_list]
            ax1.plot(recalculated_norm_list, list(time_in_sphere.keys()), marker='D', linestyle='none', alpha=0.8, color='green')

        ax1.set_xlabel('Hours spent')
        ax1.set_title('The activity in thr monitored categories')


        top_programms, bar_labels, time, bar_colors = [], [], [], []
        for i in range(10):
            try:
                values = list(log.logs.values())[i]
                top_programms.append(list(log.logs.keys())[i].strip())
                if values[0] not in bar_labels: 
                    bar_labels.append(values[0].strip())
                else:
                    bar_labels.append('_' + values[0].strip())
                time.append(int(values[1]) / 3600)
                bar_colors.append(self.color_data[values[0].strip()])
            except IndexError:
                break
        ax2.bar(top_programms, time, label=bar_labels, color=bar_colors)
        ax2.set_ylabel('')
        ax2.set_title('')
        ax2.legend(title='Type of the programm')


        #ax3 changing? Is it better to make Simple QLables with data instead of making plot?


        self.statistic_in_spheres_canvas.draw()
        self.statistic_of_programms_canvas.draw()
