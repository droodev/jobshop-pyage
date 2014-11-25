from problem import Job, Task, Problem
import copy
import random

class ProblemGenerator(object):

	def __init__(self, problemTick):
		self.problemTick = problemTick
		self.predefined_jobs = PredictedProblemGenerator().predefined_jobs

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
		job0 = Job(0,
					[Task(1,8), Task(2,3)]
					)
		job1 = Job(1,
					[Task(2,7), Task(0,3), Task(1,9)]
					)
		job2 = Job(2,
					[Task(0,1), Task(2,7), Task(1,10)]
					)
		job3 = Job(3,
					[Task(1,2), Task(2,3), Task(0,1)]
					)
		return Problem([job0, job1, job2, job3])

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