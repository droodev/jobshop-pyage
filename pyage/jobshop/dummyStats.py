import logging
from pyage.core.statistics import Statistics

logger = logging.getLogger(__name__)

class DummyStats(Statistics):

	def __init__(self):
		pass

	def update(self, step_count, agents):
		if step_count % 50 == 0:
			best_agent = min(agents, key= lambda x: x.get_fitness)
			logger.info("\nBEST SOLUTION:\n%s",
				best_agent.get_solution())

	def summarize(self, agents):
		pass
