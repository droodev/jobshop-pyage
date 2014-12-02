import matplotlib.pyplot as plt
from os import sep
from os import path
from os import makedirs
import colorsys


class GanttGenerator(object):
    __tasks = {}
    __colors = "bgrcmykw"
    __N = 50

    def __init__(self, n_machines=None, out_dir='gantt'):
        self.__out_dir = out_dir
        if n_machines is not None:
            self.__n_machines = n_machines
        if not path.exists(out_dir):
            makedirs(out_dir)

    def add_task(self, machine_nr, job_nr, start_time, duration):
        if machine_nr not in self.__tasks.keys():
            self.__tasks[machine_nr] = {}

        machine = self.__tasks[machine_nr]
        machine[start_time] = {'job_nr': job_nr, 'duration': duration}

    def generate(self, title=None):
        max_duration = 0
        for machine_nr in self.__tasks:
            machine = self.__tasks[machine_nr]
            for start_time in machine:
                job_nr = machine[start_time]['job_nr']
                duration = machine[start_time]['duration']
                color = self.__colors[job_nr % len(self.__colors)]

                plt.hlines(machine_nr, start_time, start_time + duration, colors=color, lw=50)

                if duration + start_time > max_duration:
                    max_duration = duration + start_time

        plt.margins(1)
        plt.axis([0, max_duration, 0.8, self.__n_machines])
        plt.xticks(range(0, max_duration, 1))
        if title:
            plt.title(title)
        plt.xlabel("Time")
        plt.ylabel("Machines")
        plt.yticks(range(1, self.__n_machines, 1))
        plt.savefig(self.__out_dir + sep + title + '.png')
