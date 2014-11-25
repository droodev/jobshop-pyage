import logging
from pyage.core.statistics import Statistics

logger = logging.getLogger(__name__)

class DummyStats(Statistics):

	def __init__(self, step_res):
		self.step_res = step_res

	def update(self, step_count, agents):
		if step_count % self.step_res == 0:
			best_agent = min(agents, key= lambda x: x.get_fitness)
			logger.info("\nBEST SOLUTION:\n%s",
				best_agent.get_solution())

	def summarize(self, agents):
		pass
