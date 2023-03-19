from turtle import color
from PyQt5.QtWidgets import QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from matplotlib import colors
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasAgg
from appData.constants.constants import BAR1_COLORS, BAR2_COLORS
from random import randint
from main import log
from appData.settings.settings_parser import BARS

class Management(QWidget):
    def __init__(self) -> None:
        super().__init__()
        main_layout = QVBoxLayout()
        changes_layout = QVBoxLayout()
        main_statistic_layout = QHBoxLayout()

        #plotting: plot for gaming, coding and learning
        self.statistic_in_spheres = plt.figure()
        self.statistic_in_spheres_canvas = FigureCanvasAgg(self.statistic_in_spheres)
        main_statistic_layout.addWidget(self.statistic_in_spheres_canvas, stretch=3)
        #plotting: plot for top 10 programms you waqsted time on
        random_bar_colors = BAR2_COLORS.copy()
        self.statistic_of_programms = plt.figure()
        self.statistic_of_programms_canvas = FigureCanvasAgg(self.statistic_of_programms)

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

        self.changes_list = []
        for bar in BARS:
            changes = QListWidget()
            changes.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)




    def refresh(self):
        self.plot()


    def plot(self):
        self.statistic_in_spheres.clear()
        self.statistic_of_programms.clear()

        ax1 = self.statistic_in_spheres.add_subplot(111)
        ax2 = self.statistic_of_programms.add_subplot(111)


        time_in_sphere = {bar: sum(data[1] for data in log.logs.values() if data[0] == bar) for bar in BARS}

        ax1.barh(time_in_sphere.keys(), time_in_sphere.values(), align='center', alpha=0.4, colors=BAR1_COLORS)
        ax1.plot(time_in_sphere.values(), time_in_sphere.keys(), marker='D', linestyle='none', alpha=0.8, color='green')
        #TODO make a plot-marker for changeable markers. Firstly I'll need to make a function, that will count those markers
        ax1.plot(time_in_sphere.values(), time_in_sphere.keys(), marker='D', linestyle='none', alpha=0.8, color='red')

        ax1.yticks(time_in_sphere.keys(), time_in_sphere.items())
        ax1.set_xlabel('Hours spent')
        ax1.setTitle('The activity in thr monitored categories')


        top_programms, bar_labels, time, bar_colors = [], [], [], []
        for i in range(10):
            try:
                values = log.logs.values()[i]
                top_programms.append(log.logs.keys()[i])
                if values[0] not in bar_labels:
                    bar_labels.append(values[0])
                else:
                    bar_labels.append('_' + values[0])
                time.append(values[i][1] // 3600)
                bar_colors.append(self.color_data[values[0]])
            except IndexError:
                break

        ax2.bar(top_programms, time, label=bar_labels, color=bar_colors)
        ax2.set_ylabel('')
        ax2.setTitle('')
        ax2.legend(title='Type of the programm')

        self.statistic_in_spheres_canvas.draw()
        self.statistic_of_programms_canvas.draw()
