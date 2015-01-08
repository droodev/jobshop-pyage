import copy
from pyage.jobshop.machine import Machine
from pyage.core.operator import Operator
import logging

logger = logging.getLogger(__name__)


class Problem(object):
    def __init__(self, jobs_list):
        self.jobs_list = jobs_list

    def __str__(self):
    	return "Problem consisted of: \n" + "\n".join(map(str,self.jobs_list))

    def get_jobs_list(self):
    	return list(copy.deepcopy(self.jobs_list))

    def get_job_by_jid(self, jid):
    	for job in self.jobs_list:
    		if job.jid == jid:
    			return job

    def merge_with(self, prob):
    	new_jobs_list = self.get_jobs_list() + prob.get_jobs_list()
    	return Problem(new_jobs_list)

    def __eq__(self, other):
    	return self.jobs_list == other.jobs_list

    def represents_same(self, other):
    	for job in self.get_jobs_list():
    		for other_job in other.get_jobs_list():
    			if other_job.represents_same(job):
    				break
    			return False
    	return True


class Job(object):
	def __init__(self, jid, tasks_list):
		self.jid = jid
		self.tasks_list = tasks_list
		for task in tasks_list:
			task.job = self

	def __str__(self):
		caption = self.str_of_job_name()
		joined = "\n\t".join(map(lambda x: x.get_str_without_jobnr(),self.tasks_list))
		return caption + "\n\t" + joined

	def str_of_job_name(self):
		return "Job " + str(self.jid)

	def __repr__(self):
		return self.__str__()

	def get_tasks_list(self):
		return self.tasks_list

	def get_jid(self):
		return self.jid

	def get_task_for_machine(self, mid):
		for task in self.tasks_list:
			if task.get_task_machine() is mid:
				return task
		raise Exception()

	def __eq__(self, other):
		#return self.tasks_list == other.tasks_list
		return self.jid == other.jid

	def represents_same(self, other):
		return self.tasks_list == other.tasks_list

class Task(object):
	def __init__(self, machine, duration):
		self.machine = machine
		self.duration = duration

	def __str__(self):
		return "Task of job: " + str(self.job.jid) +" at machine: " + str(self.machine) + " lasting: " + str(self.duration) 

	def get_str_without_jobnr(self):
		return "Task at machine: " + str(self.machine) + " lasting: " + str(self.duration) 


	def get_duration(self):
		return self.duration

	def set_start_time(self, time):
		self.start_time=time

	def get_task_machine(self):
		return self.machine

	def get_task_job(self):
		return self.job

	def __eq__(self, other):
		return self.machine == other.machine and self.duration == other.duration

class Solution(object):

	def __init__(self, machines_nr):
		self.__machines_nr = machines_nr
		self.__machines_end_times = {}
		self.__machines_tasks = {}
		self.__initialize_machines_dicts(machines_nr)

	def __initialize_machines_dicts(self, machines_nr):
		for i in xrange(machines_nr):
			self.__machines_tasks[i] = []
			self.__machines_end_times[i] = 0

	def append_task_to_machine(self, task):
		machine_nr = task.get_task_machine()
		self.__machines_tasks[machine_nr].append(task)
		self.__machines_end_times[machine_nr] += task.get_duration()
		
	def get_completion_time(self):
		return max(self.__machines_end_times.values())

	def pop_head_task(self, machine_number):
		head_task = self.__machines_tasks[machine_number][0]
		self.__remove_first_task(machine_number)
		return head_task

	def get_tasks(self, machine_number):
		return self.__machines_tasks[machine_number]

	def remove_last_task(self, machine_number):
		self.__machines_tasks[machine_number]=self.__machines_tasks[machine_number][:-1]

	def __remove_first_task(self, machine_number):
		self.__machines_tasks[machine_number].remove(self.__machines_tasks[machine_number][0])

	def append_clone_more_solution_part(self, new_solution):
		raw_tasks = []
		for m_nr in xrange(self.__machines_nr):
			old_tasks = self.get_tasks(m_nr)
			new_tasks = new_solution.get_tasks(m_nr)
			raw_tasks.append(copy.deepcopy(old_tasks+new_tasks))
		new_solution = Solution(self.__machines_nr)
		for m_nr in xrange(self.__machines_nr):
			for task in raw_tasks[m_nr]:
				new_solution.append_task_to_machine(task)

		return new_solution


	def __str__(self):
		machine_strings_list = []
		for m_nr in xrange(self.__machines_nr):
			machine_string = "MACHINE " + str(m_nr) + ":"
			jobs_string = "\n\t".join(map(str,self.__machines_tasks[m_nr]))
			jobs_string = "\n\t" + jobs_string
			machine_strings_list.append(machine_string+jobs_string)
		machine_strings_list = ["Completion time: " + str(self.get_completion_time())] + machine_strings_list
		return "\n".join(machine_strings_list)


#################################################################
#			CLASSES OF GENETIC ALGORITHM APPROACH				#
#################################################################
class JobShopGenotype(object):
    ''' uporzadkowana lista [Jobnumber, Jobnumber, Jobnumber,...] o dlugosci rownej ilosci taskow
        n-te wystapienie danego numeru joba oznacza zakolejkowanie w danej chwili n-tego taska tego joba'''
    def __init__(self, joblist):
        self.genes = joblist
        self.fitness = None
        
class BasicJobShopEvaluation(Operator):
    
    def __init__(self,machines_nr):
        super(BasicJobShopEvaluation, self).__init__(JobShopGenotype)
        self.machines_nr = machines_nr
        
    
    def process(self, population):
        for genotype in population:
            genotype.fitness = self.__schedule(genotype.genes)
        
    def __schedule(self,genes):
        machines = []
        for num in xrange(self.machines_nr):
            machines.append(Machine(num))
        currentTime = 0
        lastTimeAdded = 0
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
                    jobs_tasks[job.jid].remove(task)
                if not jobs_tasks[job.jid]:
                    jobList.remove(job)
            currentTime += 1
        return currentTime-1+lastTimeAdded
            
    def __notInProgress(self, job, machines, currentTime):
        for x in machines:
            if currentTime < x.taskEndTime and x.jobInProgress == job.get_jid():
                return False
        return True
class BasicJobShopMutation(Operator):
    
    def __init__(self,probability=0.1):
        super(BasicJobShopMutation, self).__init__(JobShopGenotype, probability)
