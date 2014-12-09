import logging
import itertools
import copy

from pyage.core.inject import Inject
from machine import Machine
from problem import Solution
from manufacture import Manufacture
from timeKeeper import TimeKeeper
from problemGenerator import PredictedProblemGenerator


logger = logging.getLogger(__name__)

class MasterAgent(object):
    @Inject("slaves:_MasterAgent__slaves")
    @Inject("problemGenerator:_MasterAgent__problemGenerator")
    def __init__(self, name=None):
        self.name = name
        super(MasterAgent, self).__init__()
        for agent in self.__slaves.values():
            agent.parent = self
        logger.debug("Slaves number: %d", len(self.__slaves.values()))
        self.steps = 1
        self.manufacture = Manufacture(4)
        self.timeKeeper = TimeKeeper(5,-1)
        self.problem = None
        self.assigned = False
        self.predictor = PredictedProblemGenerator()

    def get_history(self):
        return self.manufacture.get_history()

    def step(self):
        self.timeKeeper.step(self.steps)
        if (not self.assigned) and (self.timeKeeper.get_time() == 0):
            self.manufacture.assign_tasks(self.get_solution())
            self.assigned = True
            self.__assign_predicted_and_solution_part()


        self.manufacture.time_tick(self.timeKeeper.get_time())

        if self._MasterAgent__problemGenerator.check_new_problem(self.steps):
            new_problem = self._MasterAgent__problemGenerator.step(self.steps)
            self.problem = new_problem
            logger.debug("New problem came: \n%s", new_problem)
            if(self.steps == 1):
                for agent in self.__slaves.values():
                    agent.append_problem(new_problem, None)
            else:
                for agent in self.__slaves.values():
                    if agent.check_predicated_problem(new_problem):
                        logger.debug("Agent with good pred_problem")
                        new_solution = agent.get_solution()
                        #logger.debug("Pretty new solution\n %s",new_solution)
                        self.manufacture.assign_tasks(new_solution)
                        self.__assign_predicted_and_solution_part()
                        break

        for agent in self.__slaves.values():
            agent.step()

        self.steps += 1

    def __get_predicted_and_solution_problems(self, solution_part_problem):
        predicted = self.predictor.get_predicted_problems()
        merged_problems  = {}
        for pred in predicted:
            merged_problems[solution_part_problem.merge_with(pred)]=pred
        return merged_problems

    def __assign_predicted_and_solution_part(self):
        solution_part_problem = self.manufacture.get_solution_part_as_problem(2)
        merged_problems = self.__get_predicted_and_solution_problems(solution_part_problem)
        if len(self.__slaves) != len(merged_problems):
            raise Exception("Not equal: agents and predicted problems")
        for it in xrange(len(self.__slaves)):
            merged_problem = merged_problems.keys()[it]
            self.__slaves.values()[it].append_problem(merged_problem, merged_problems[merged_problem])
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
    def __init__(self, aid):
        self.steps = 1
        self.aid = aid

    def append_problem(self, problem, predicted_problem):
        logger.debug("%d New problem for slave appended: \n%s\n with predicted\n %s ", self.aid, problem, predicted_problem)
        self.solver = SimpleSolver(4, problem)
        self.predicted_problem = predicted_problem

    def step(self):
        #logger.debug("Slave step")
        self.solver.step()
        self.steps += 1

    def get_fitness(self):
        return self.solver.get_fitness()

    def get_solution(self):
        return self.solver.get_solution()

    def check_predicated_problem(self, checked_problem):
        if checked_problem == self.predicted_problem:
            logger.debug("%d Checked: %s\n",self.aid, checked_problem)
            logger.debug("%d predicted: %s\n",self.aid, self.predicted_problem)
            return True


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
        jobs_tasks = {}
        for job in jobList:
            jobs_tasks[job.jid] = list(copy.deepcopy(job.get_tasks_list()))
        
        while jobList:
            for job in jobList:
                task = jobs_tasks[job.jid][0]
                if currentTime >= machines[task.machine].taskEndTime and self.__notInProgress(job, machines, currentTime):
                    machines[task.machine].taskEndTime = currentTime + task.get_duration()
                    machines[task.machine].jobInProgress = job.get_jid()
                    lastTimeAdded = task.get_duration()
                    task.set_start_time(currentTime)
                    solution.append_job_to_machine(task.machine, job)
                    jobs_tasks[job.jid].remove(task)
                if not jobs_tasks[job.jid]:
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
        for i in xrange(count):
            agent = agent_type(i)
            agents["Master_" + str(i)] = agent
        return agents
    return factory
