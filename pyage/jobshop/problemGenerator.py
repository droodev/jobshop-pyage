from problem import Job, Task, Problem
import copy
import random
from time import time

class Randomized(object):

	def init_random(self, random_obj):
		self.random = random_obj

	def random_check(self):
		if "random" not in self.__dict__:
			raise Exception("Randomized object not initialized properly")

class Distribution(Randomized):

	def next(self):
		self.random_check()
		return self.getRandom()

	def getRandom(self):
		raise NotImplementedException()

class UniformIntDistribution(Distribution):

	def __init__(self, start_in, end_in):
		self.start = start_in
		self.end = end_in

	def getRandom(self):
		return self.random.randint(self.start, self.end)


class ProblemGenerator(object):

	def __init__(self, problemTick):
		self.problemTick = problemTick
		self.predefined_jobs = PredictedProblemGenerator().predefined_jobs
		self.__gen = NewProblemGenerator(
				machines_number = 3,
				jobs_number = 5,
				job_duration_distrib = UniformIntDistribution(7,10),
				tasks_number_distrib = UniformIntDistribution(2,3),
				tasks_provider = TasksProvider(3)
			)

	def step(self, step_nr):
		if self.check_new_problem(step_nr):
			if step_nr == 1:
				return self.__create_initial_problem()
			else:
				#new_job = random.choice(self.predefined_jobs)
				new_job = self.predefined_jobs[6]
				return Problem([new_job])


	def check_new_problem(self, step_nr):
		return self.__new_problem_check(step_nr)

	def __new_problem_check(self, step_nr):
		return step_nr % self.problemTick == 1

	def __create_initial_problem(self):
		return self.__gen.generate_problem()

class PredictedProblemGenerator(object):

	def __init__(self):
		self.predefined_jobs = [
			Job(1, [Task(0,2), Task(1,3)]),
			Job(2, [Task(0,1), Task(1,2), Task(2,3)]),
			Job(3, [Task(0,2), Task(1,1), Task(2,3)]),
			Job(4, [Task(0,3), Task(1,1), Task(2,2)]),
			Job(5, [Task(0,2), Task(1,3), Task(2,2)]),
			Job(6, [Task(0,4), Task(1,1), Task(2,2)]),
			Job(7, [Task(0,4), Task(1,1), Task(2,2), Task(3,1)]),
			Job(8, [Task(0,2), Task(1,2), Task(2,2), Task(3,1)]),
			Job(9, [Task(0,3), Task(1,3)]),
			Job(10, [Task(0,2), Task(0,5)]),
		]

	def get_predicted_problems(self):
		problems = []
		for job in self.predefined_jobs:
			problems.append(Problem([copy.deepcopy(job)]))
		return problems



class NewProblemGenerator(object):

	def __init__(self, machines_number, jobs_number, job_duration_distrib, tasks_number_distrib, tasks_provider, seed=None):
		self.__machines_nr = machines_number
		self.__jobs_nr = jobs_number
		self.__jobs_distrib = job_duration_distrib
		self.__tasks_distrib = tasks_number_distrib
		self.__tasks_provider = tasks_provider
		self.__counter = 0
		random.seed(seed)
		self.__init_randoms()

	def __init_randoms(self):
		self.__tasks_provider.init_random(random)
		self.__tasks_distrib.init_random(random)
		self.__jobs_distrib.init_random(random)

	def generate_problem(self):
		return Problem([self.__generate_job() for _ in xrange(self.__jobs_nr)])

	def __generate_job(self):
		job_duration = self.__jobs_distrib.next()
		tasks_number = self.__tasks_distrib.next()
		tasks = self.__tasks_provider.provide(job_duration=job_duration, tasks_number=tasks_number)
		new_job = Job(self.__counter, tasks)
		self.__counter += 1
		return new_job

class TasksProvider(object):

	def __init__(self, machines_number):
		self.__machines_nr = machines_number

	def init_random(self, random_obj):
		self.__random = random_obj

	def provide(self, job_duration, tasks_number):

		#TODO remove this, bacause jobshop definition allows,
		#depend on model, so it has to be refactored before
		if tasks_number > self.__machines_nr:
			raise Exception("Tasks number cannot be grater than machines number")

		average = job_duration/tasks_number
		std_dev = average/2
		remaining_duration = job_duration
		tasks = []
		for task_counter in xrange(tasks_number):
			task_machine = task_counter % self.__machines_nr
			task_duration = int(self.__random.gauss(average, std_dev))
			positive_task_duration = max(1, task_duration)
			if task_counter == tasks_number-1:
				task_real_duration = remaining_duration
			else:
				task_real_duration = min(remaining_duration, positive_task_duration)
			remaining_duration -= task_real_duration
			tasks.append(Task(task_machine, task_real_duration))
			if remaining_duration ==0:
				break
		return tasks

