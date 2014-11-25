# coding=utf-8
import logging
import os
import Pyro4

from pyage.core import address
from pyage.jobshop.agents import masters_factory, slaves_factory
from pyage.core.agent.aggregate import AggregateAgent
from pyage.core.locator import  RandomLocator
from pyage.core.migration import Pyro4Migration
from pyage.core.stop_condition import StepLimitStopCondition
from pyage.jobshop.problem import  Problem
from pyage.jobshop.adjuster import  Adjuster
from pyage.jobshop.machine import  Machine
from pyage.jobshop.presolver import  Presolver
from pyage.jobshop.problemGenerator import  ProblemGenerator
from pyage.jobshop.dummyStats import DummyStats

logger = logging.getLogger(__name__)

agents_count = 1
jobshop_agents = 2
logger.debug("AGGREGATE, %s agents", agents_count)

#problem = Problem() 
adjuster = Adjuster()
#machine = Machine()
presolver= Presolver()
problemGenerator = lambda: ProblemGenerator(50)

agents = masters_factory(agents_count)
slaves = slaves_factory(jobshop_agents)

stop_condition = lambda: StepLimitStopCondition(100)

population_size = 500
operators = lambda: [FloatRastriginEvaluation(), TournamentSelection(size=55, tournament_size=30),
                     Crossover(size=population_size), Mutation()]
initializer = lambda: Initializer()

address_provider = address.SequenceAddressProvider

stats = lambda: DummyStats(40)
