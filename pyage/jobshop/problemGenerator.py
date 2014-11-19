from problem import Job, Task, Problem

class ProblemGenerator(object):

	def __init__(self, problemTick):
		self.problemTick = problemTick

	def step(self, step_nr):
		if self.check_new_problem(step_nr):
			if step_nr == 0:
				return self.__create_initial_problem()
			else:
				new_job = Job(step_nr/self.problemTick,
							[Task(0,2), Task(2,2), Task(1,2)]
							)

				return Problem([new_job])


	def check_new_problem(self, step_nr):
		return self.__new_problem_check(step_nr)

	def __new_problem_check(self, step_nr):
		return step_nr % self.problemTick == 0

	def __create_initial_problem(self):
		job0 = Job(0,
					[Task(0,5), Task(1,8), Task(2,3)]
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