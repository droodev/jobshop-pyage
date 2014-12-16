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
from pyage.jobshop.problemGenerator import  ProblemGenerator, UniformIntDistribution, RandomizedTasksProvider, PredictedProblemGenerator, RandomizedProblemProvider
from pyage.jobshop.dummyStats import DummyStats
from pyage.core.statistics import  GanttGenerator
from pyage.core.statistics import  GanttStatistics

logger = logging.getLogger(__name__)

agents_count = 1
jobshop_agents = 10
machines_number = 4
logger.debug("AGGREGATE, %s agents", agents_count)

start_problem_provider = RandomizedProblemProvider(
				machines_number = machines_number,
				jobs_number = 5,
				job_duration_distrib = UniformIntDistribution(7,10),
				tasks_number_distrib = UniformIntDistribution(2,3),
				tasks_provider = RandomizedTasksProvider(machines_number)
			)
predicted_problem_provider = RandomizedProblemProvider(
				machines_number = machines_number,
				jobs_number = 1,
				job_duration_distrib = UniformIntDistribution(5,5),
				tasks_number_distrib = UniformIntDistribution(1,3),
				tasks_provider = RandomizedTasksProvider(machines_number)
			)

problemGenerator = lambda: ProblemGenerator(50, start_problem_provider, predicted_problem_provider)

predictedProblemGenerator = lambda: PredictedProblemGenerator(predicted_problem_provider, jobshop_agents)

agents = masters_factory(agents_count)
slaves = slaves_factory(jobshop_agents)

stop_condition = lambda: StepLimitStopCondition(100)

population_size = 500
operators = lambda: [FloatRastriginEvaluation(), TournamentSelection(size=55, tournament_size=30),
                     Crossover(size=population_size), Mutation()]
initializer = lambda: Initializer()

address_provider = address.SequenceAddressProvider

stats = GanttStatistics #lambda: DummyStats(10000000000)
