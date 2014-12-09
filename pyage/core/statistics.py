import logging
import os
from os import sep
from os import path
from os import makedirs
import matplotlib.pyplot as plt
import urllib2
import time
import sys
from pyage.core.inject import InjectOptional, Inject

logger = logging.getLogger(__name__)


class Statistics(object):
    def update(self, step_count, agents):
        raise NotImplementedError()

    def summarize(self, agents):
        raise NotImplementedError()


class SimpleStatistics(Statistics):
    def __init__(self, plot_file_name='plot.png'):
        self.history = []
        self.plot_file_name = plot_file_name

    def update(self, step_count, agents):
        try:
            best_fitness = max(a.get_fitness() for a in agents)
            logger.info(best_fitness)
            self.history.append(best_fitness)
        except:
            logging.exception("")

    def summarize(self, agents):
        try:
            import pylab
            logger.debug(self.history)
            logger.debug("best genotype: %s", max(agents, key=lambda a: a.get_fitness).get_best_genotype())
            pylab.yscale('symlog')
            pylab.savefig(self.plot_file_name)
        except:
            logging.exception("")


class TimeStatistics(SimpleStatistics):
    @InjectOptional("notification_url")
    def __init__(self, plot_file_name='plot.png'):
        super(TimeStatistics, self).__init__(plot_file_name)
        self.times = []
        self.start = time.time()

    def update(self, step_count, agents):
        super(TimeStatistics, self).update(step_count, agents)
        try:
            self.times.append(time.time() - self.start)
        except:
            logging.exception("")

    def summarize(self, agents):
        try:
            import pylab
            pylab.plot(self.times, self.history)
            pylab.xlabel("time (s)")
            pylab.ylabel("fitness")
            pylab.yscale('symlog')
            pylab.savefig(self.plot_file_name)

            if hasattr(self, "notification_url"):
                url = self.notification_url + "?time=%s&agents=%s&conf=%s" % (
                    time.time() - self.start, os.environ['AGENTS'], sys.argv[1])
                logger.info(url)
                urllib2.urlopen(url)
            logger.debug(self.history)
            logger.debug("best genotype: %s", max(agents, key=lambda a: a.get_fitness).get_best_genotype())
        except:
            logging.exception("")


class NotificationStatistics(SimpleStatistics):
    @Inject("notification_url")
    def __init__(self):
        super(NotificationStatistics, self).__init__()
        self.start = time.time()

    def summarize(self, agents):
        try:
            url = self.notification_url + "?time=%s&agents=%s&conf=%s" % (
                time.time() - self.start, os.environ['AGENTS'], sys.argv[1])
            logger.info(url)
            urllib2.urlopen(url)

        except:
            logging.exception("")

class NoStatistics(Statistics):
    def update(self, step_count, agents):
        pass

    def summarize(self, agents):
        pass

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
        if self.__n_machines is None:
            plt.axis([0, max_duration, 0.8, 5])
        else:
            plt.axis([0, max_duration, 0.8, self.__n_machines])
        plt.xticks(range(0, max_duration, 1))
        if title:
            plt.title(title)
        plt.xlabel("Time")
        plt.ylabel("Machines")
        if self.__n_machines is None:
            plt.yticks(range(1, 5, 1))
        else:
            plt.yticks(range(1, self.__n_machines, 1))
        plt.savefig(self.__out_dir + sep + title + '.png')
