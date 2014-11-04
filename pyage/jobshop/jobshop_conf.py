# coding=utf-8
import logging
import os
import Pyro4

from pyage.core import address
from pyage.jobshop.agents import masters_factory
from pyage.core.agent.aggregate import AggregateAgent
from pyage.core.locator import  RandomLocator
from pyage.core.migration import Pyro4Migration
from pyage.core.statistics import  TimeStatistics
from pyage.core.stop_condition import StepLimitStopCondition
from pyage.jobshop.crossover import  Crossover
from pyage.jobshop.evaluation import  Evaluation
from pyage.jobshop.initializer import  Initializer
from pyage.jobshop.mutation import  Mutation
from pyage.jobshop.selection import TournamentSelection

logger = logging.getLogger(__name__)

agents_count = 1
number_of_islands = 2
logger.debug("AGGREGATE, %s agents", agents_count)

agents = masters_factory(agents_count)
aggregated_agents = slave_factory(number_of_islands)

stop_condition = lambda: StepLimitStopCondition(100)

population_size = 500
operators = lambda: [FloatRastriginEvaluation(), TournamentSelection(size=55, tournament_size=30),
                     Crossover(size=population_size), Mutation()]
initializer = lambda: Initializer()

address_provider = address.SequenceAddressProvider

migration = Pyro4Migration
locator = RandomLocator

ns_hostname = lambda: os.environ['NS_HOSTNAME']
pyro_daemon = Pyro4.Daemon()
daemon = lambda: pyro_daemon

stats = TimeStatistics
