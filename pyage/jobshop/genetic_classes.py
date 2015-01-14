# -*- coding: utf-8 -*-
'''
Created on Dec 3, 2014

@author: deltharis
'''

from random import randrange
from pyage.core.operator import Operator
import copy
from pyage.solutions.evolution.mutation import AbstractMutation
from pyage.solutions.evolution.crossover import AbstractCrossover
from pyage.jobshop.problem import Solution

class JobShopGenotype(object):
    ''' uporzadkowana lista [Jobnumber, Jobnumber, Jobnumber,...] o długosci rownej ilosci taskow
        n-te wystapienie danego numeru joba oznacza zakolejkowanie w danej chwili n-tego taska tego joba'''
    def __init__(self, joblist):
        self.genes = joblist
        self.fitness = None
        
    def __init_from_problem__(self,problem):
        self.problem = problem
        self.genes = self.nonrandom_generate_genes(problem)
        self.fitness = None

    def getSolutionOutOfGenotype(self):
        return BasicJobShopEvaluation.schedule(self.genes)
        
    def nonrandom_generate_genes(self, problem):
        joblist = []
        for job in problem:
            for task in job:
                joblist.append(job.jid)
        return joblist

class BasicJobShopEvaluation(Operator):
    
    def __init__(self,machines_nr):
        super(BasicJobShopEvaluation, self).__init__(JobShopGenotype)
        self.machines_nr = machines_nr
        self.solution = None
    
    def process(self, population):
        for genotype in population:
            genotype.fitness = self.__schedule_time(genotype.genes)

    ''' arbitrary sign change to conserve bigger == better'''
    def __schedule_time(self, genes):
        return self.schedule(genes).get_completion_time() * (-1)

    def schedule(self,genes):
        ending_times = [0 for _ in xrange(self.machines_nr)]
        jobs_in_progress = [None for _ in xrange(self.machines_nr)]
        currentTime = 0
        solution = Solution(self.machines_nr)
        jobs_tasks = {}
        jobList = list(copy.deepcopy(genes))
        for job in jobList:
            jobs_tasks[job.jid] = job.get_tasks_list()
        
        while jobList:
            for job in jobList:
                task = jobs_tasks[job.jid][0]
                if currentTime >= ending_times[task.machine] and self.__notInProgress(job, ending_times, jobs_in_progress, currentTime):
                    ending_times[task.machine] = currentTime + task.get_duration()
                    jobs_in_progress[task.machine] = job
                    task.set_start_time(currentTime)
                    solution.append_task_to_machine(task)
                    jobs_tasks[job.jid].remove(task)
                if not jobs_tasks[job.jid]:
                    jobList.remove(job)
            currentTime += 1
        return solution

    '''wymogi JobShop - jeden job moze naraz isc tylko na jednej maszynie'''
    def __notInProgress(self, job, ending_times, jobs_in_progress, currentTime):
        for i in xrange(len(jobs_in_progress)):
            if currentTime < ending_times[i] and job.jid == jobs_in_progress[i].jid:
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


class BasicJobShopSelection(Operator):
    def __init__(self, type=None):
        super(BasicJobShopSelection, self).__init__()

    def process(self, population):
        p = list(population)
        population[:] = []
        gen1 = p[0]
        gen2 = p[1]
        winner = gen1 if gen1.fitness > gen2.fitness else gen2
        population.append(winner)
