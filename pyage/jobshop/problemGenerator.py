class ProblemGenerator(object):

	def __init__(self, problemTick):
		self.problemTick = problemTick

	def step(self, step_nr):
		if check_new_problem(step_nr):
			return Problem()

	def check_new_problem(self, step_nr):
		return self.__new_problem_check(step_nr)

	def __new_problem_check(self, step_nr):
		return step_nr % self.problemTick == 0