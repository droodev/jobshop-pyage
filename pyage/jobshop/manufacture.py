import logging
from machine import Machine
import copy

logger = logging.getLogger(__name__)

class Manufacture(object):

	def __init__(self, machines_nr):
		self.machines_nr = machines_nr
		self.machines = [Machine(i) for i in xrange(machines_nr)]
		#to be fixed - workaround
		for machine in self.machines:
			machine.taskEndTime = -1
		self.time = -1

	def assign_tasks(self, solution, problem):
		self.solution = copy.deepcopy(solution)
		self.problem = problem


	def time_tick(self, new_time):
		if new_time is self.time:
			return
		logger.debug("Time tick: %d->%d", self.time, new_time)
		self.__check_and_update(self.time)
		self.time = new_time

	def __check_and_update(self, old_time):
		logger.debug("Updating!")
		for machine in self.machines:
			if machine.taskEndTime is old_time:
				logger.debug("Updating machine: %d", machine.idd)
				try:
					current_job = self.solution.get_machine_job(machine.idd)[0]
					del self.solution.get_machine_job(machine.idd)[0]
					task = current_job.get_task_for_machine(machine.idd)
					machine.taskEndTime = old_time+1+task.get_duration()
					logger.debug("New endtime: %d", machine.taskEndTime)
				except IndexError:
					logger.debug("Nothing to add")