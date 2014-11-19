from pyage.core.address import Addressable
from pyage.core.agent.agent import AbstractAgent
from pyage.core.inject import Inject
from machine import Machine
from problem import Solution
import logging
import itertools   
import copy

logger = logging.getLogger(__name__)

class MasterAgent(object):
    @Inject("slaves:_MasterAgent__slaves")
    @Inject("problemGenerator:_MasterAgent__problemGenerator")
    def __init__(self, name=None):
        self.name = name
        super(MasterAgent, self).__init__()
        for agent in self.__slaves.values():
            agent.parent = self
        self.steps = 0

    def step(self):
        for agent in self.__slaves.values():
            if self._MasterAgent__problemGenerator.check_new_problem(self.steps):
                new_problem = self._MasterAgent__problemGenerator.step(self.steps)
                agent.append_problem(new_problem)
                logger.debug("NEW PROBLEM: \n%s", new_problem)
            agent.step()
        self.steps += 1

    def get_agents(self):
        return self.__slaves.values()

    def get_fitness(self):
        min_fitness_agent = min(self.__slaves.values(), key=lambda x: x.get_fitness)
        logger.debug("Taken fitness is %d\n", min_fitness_agent.get_fitness())
        return min_fitness_agent.get_fitness()

    def get_solution(self):
        min_fitness_agent = min(self.__slaves.values(), key=lambda x: x.get_fitness)
        return min_fitness_agent.get_solution()

class SlaveAgent(object):
    def __init__(self):
        self.steps = 0

    def append_problem(self, problem):
        self.solver = SimpleSolver(3, problem)

    def step(self):
        logger.debug("Slave step")
        self.solver.step()
        self.steps += 1

    def get_fitness(self):
        return self.solver.get_fitness()

    def get_solution(self):
        return self.solver.get_solution()

class SimpleSolver(object):

    def __init__(self, machines_nr, problem):
        self.machines_nr = machines_nr
        self.problem = problem
        self.permutations = self.__getPermutations(problem.get_jobs_list())
        self.bestSolution = None

    def step(self):
        try:
            current_permutation = self.permutations.next()
        except(StopIteration):
            return
        solution = self.__solveStuff(list(copy.deepcopy(current_permutation)))
        if self.bestSolution is None or solution.get_completion_time() < self.bestSolution.get_completion_time():
                self.bestSolution = solution

    def get_fitness(self):
        return self.bestSolution.get_completion_time()

    def get_solution(self):
        return self.bestSolution


    '''zwraca liste [czas-rozwiazania, rozwiazanie]  '''
    def __solveStuff(self, jobList):
        machines = []
        for num in xrange(self.machines_nr):
            machines.append(Machine(num))
        currentTime = 0
        lastTimeAdded = 0
        solution = Solution(self.machines_nr)
        #machineSolutions = [[]] * len(machines)
        #for i in xrange(len(machines)):
        #   machineSolutions[i] = []
              
        while jobList:
            for job in jobList:
                task = job.get_tasks_list()[0]
                if currentTime >= machines[task.machine].taskEndTime and self.__notInProgress(job, machines, currentTime):
                    machines[task.machine].taskEndTime = currentTime + task.get_duration()
                    machines[task.machine].jobInProgress = job.get_jid()
                    lastTimeAdded = task.get_duration()
                    task.set_start_time(currentTime)
                    #machineSolutions[task.machine].append(job)
                    solution.append_job_to_machine(task.machine, job)
                    job.get_tasks_list().remove(task)
                if not job.get_tasks_list():
                    jobList.remove(job)
            currentTime += 1
        solution.set_completion_time(currentTime-1+lastTimeAdded)
        return solution

    def __getPermutations(self, jobList):
        return itertools.permutations(jobList,len(jobList))

    '''wymogi JobShop - jeden job moze naraz isc tylko na jednej maszynie'''
    def __notInProgress(self, job, machines, currentTime):
        for x in machines:
            if currentTime < x.taskEndTime and x.jobInProgress == job.get_jid():
                return False
        return True

def masters_factory(count):
    return _agents_factory(count, MasterAgent)

def slaves_factory(count):
    return _agents_factory(count, SlaveAgent)

def _agents_factory(count, agent_type):
    def factory():
        agents = {}
        for _ in xrange(count):
            agent = agent_type()
            agents["Master_" + str(count)] = agent
        return agents
    return factory
