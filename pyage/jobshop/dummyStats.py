import logging
from pyage.core.statistics import Statistics

logger = logging.getLogger(__name__)

class DummyStats(Statistics):

	def __init__(self):
		pass

	def update(self, step_count, agents):
		pass

	def summarize(self, agents):
		pass
