from turtle import color
from PyQt5.QtWidgets import QWidget, QListWidget, QLabel, QListView, QVBoxLayout, QHBoxLayout
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasAgg
from appData.constants.constants import bar1_colors, bar2_colors
from random import randint
from main import log

class Helper(QWidget):
    pass

class Management(QWidget):
    def __init__(self):
        main_layout = QVBoxLayout()

        #plotting: plot for gaming, coding and learning
        self.statistic_in_spheres = plt.figure()
        self.statistic_in_spheres_canvas = FigureCanvasAgg(self.statistic_in_spheres)
        #plotting: plot for top 10 programms you waqsted time on
        random_bar_colors = bar2_colors.copy()
        self.statistic_of_programms = plt.figure()
        self.statistic_of_programms_canvas = FigureCanvasAgg(self.statistic_of_programms)
        self.color_data = {
            'Game': random_bar_colors.pop(randint(0, len(random_bar_colors) - 1)),
            'Entartainment': random_bar_colors.pop(randint(0, len(random_bar_colors) - 1)),
            'Code': random_bar_colors.pop(randint(0, len(random_bar_colors) - 1)),
            'Learning': random_bar_colors.pop(randint(0, len(random_bar_colors) - 1)),
            'Browser': random_bar_colors.pop(randint(0, len(random_bar_colors) - 1)),
            'Social Network': random_bar_colors.pop(randint(0, len(random_bar_colors) - 1)),
            'Tools': random_bar_colors.pop(randint(0, len(random_bar_colors) - 1)),
        }

    def refresh(self):
        self.plot()


    def parse(self):
        pass



    def plot(self):
        self.statistic_in_spheres.clear()
        self.statistic_of_programms.clear()

        ax1 = self.statistic_in_spheres.add_subplot(111)
        ax2 = self.statistic_of_programms.add_subplot(111)

        '''
        Depending on the setting user will be able to choose, what stitistic they wanna see in programm. So, I'll need suitable version of the next coded
        for future versions. 

        time_container = {
            'Game': 0,
            'Entartainment': 0,
            'Code': 0,
            'Learning': 0,
            'Browser': 0,
            'Social Network': 0,
            'Tools': 0,
        }

        '''

        ax1.barh()
        ax1.plot()

        ax1.set_ylabel('')
        ax1.setTitle('')
        ax1.legend(title='')


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
