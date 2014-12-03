'''
Created on Dec 3, 2014

@author: deltharis
'''

from random import randrange
from pyage.core.operator import Operator
import copy
from pyage.jobshop.machine import Machine
from pyage.solutions.evolution.mutation import AbstractMutation
from pyage.solutions.evolution.crossover import AbstractCrossover
from pyage.jobshop.problem import Solution

class JobShopGenotype(object):
    ''' uporzadkowana lista [Jobnumber, Jobnumber, Jobnumber,...] o długosci rownej ilosci taskow
        n-te wystapienie danego numeru joba oznacza zakolejkowanie w danej chwili n-tego taska tego joba'''
    def __init__(self, joblist):
        self.genes = joblist
        self.fitness = None
        
    def getSolutionOutOfGenotype(self):
        return BasicJobShopEvaluation.schedule(self.genes)
        
class BasicJobShopEvaluation(Operator):
    
    def __init__(self,machines_nr):
        super(BasicJobShopEvaluation, self).__init__(JobShopGenotype)
        self.machines_nr = machines_nr
        
    
    def process(self, population):
        for genotype in population:
            genotype.fitness = self.__schedule_time(genotype.genes)
            
    def __schedule_time(self, genes):
        return self.schedule(genes).get_completion_time()
        
    def schedule(self,genes):
        machines = []
        for num in xrange(self.machines_nr):
            machines.append(Machine(num))
        currentTime = 0
        lastTimeAdded = 0
        solution = Solution(self.machines_nr)
        jobs_tasks = {}
        jobList = list(copy.deepcopy(genes))
        for job in jobList:
            jobs_tasks[job.jid] = job.get_tasks_list()
        
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
            
    def __notInProgress(self, job, machines, currentTime):
        for x in machines:
            if currentTime < x.taskEndTime and x.jobInProgress == job.get_jid():
                return False
        return True

'''zamiana miejscami dwoch losowych genów'''
class BasicJobShopMutation(AbstractMutation):
    
    def __init__(self,probability=0.1):
        super(BasicJobShopMutation, self).__init__(JobShopGenotype, probability)
        
    def mutate(self, genotype):
        length = len(genotype)
        a = randrange(length)
        b = randrange(length)
        while a == b:
            b = randrange(length)
        genotype[a], genotype[b] = genotype[b], genotype[a]
        
'''Od poczatku do punktu przeciecia - pierwszy rodzic, w dal - prawy rodzic'''
class OnePointJobShopCrossover(AbstractCrossover):
    '''I don't really know yet how this size relates to amount of agents run'''
    def __init__(self, size=100):
        super(OnePointJobShopCrossover, self).__init__(JobShopGenotype, size)
        
    def cross(self, p1, p2):
        p2copy = list(copy.deepcopy(p2))
        crosspoint = randrange(len(p1))
        child = []
        for i in range(crosspoint):
            child.append(p1[i])
            p2copy.remove(p1[i])
        for job in p2copy:
            child.append(job)
        return child