class Problem(object):
    def __init__(self, jobs_list):
        self.jobs_list = jobs_list

    def __str__(self):
    	return "\n".join(map(str,self.jobs_list))

    def get_jobs_list(self):
    	return self.jobs_list

class Job(object):
	def __init__(self, jid, tasks_list):
		self.jid = jid
		self.tasks_list = tasks_list

	def __str__(self):
		caption = self.str_of_job_name()
		joined = "\n\t".join(map(str,self.tasks_list))
		return caption + "\n\t" + joined

	def str_of_job_name(self):
		return "Job " + str(self.jid)

	def __repr__(self):
		return self.__str__()

	def get_tasks_list(self):
		return self.tasks_list

	def get_jid(self):
		return self.jid

class Task(object):
	def __init__(self, machine, duration):
		self.machine = machine
		self.duration = duration

	def __str__(self):
		return "Task at machine: " + str(self.machine) + " lasting: " + str(self.duration) 

	def get_duration(self):
		return self.duration

	def set_start_time(self, time):
		self.start_time=time

class Solution(object):
	def __init__(self, machines_nr):
		self.machines = [[] for _ in xrange(machines_nr)]
		self.completion_time = 0
		self.machines_nr = machines_nr

	def append_job_to_machine(self, machine_nr, job):
		self.machines[machine_nr].append(job)

	def set_completion_time(self, completion_time):
		self.completion_time = completion_time

	def get_completion_time(self):
		return self.completion_time

	def __str__(self):
		machine_strings_list = []
		for m_nr in xrange(self.machines_nr):
			machine_string = "MACHINE " + str(m_nr) + ":"
			jobs_string = "\n\t".join(map(lambda x: x.str_of_job_name(),self.machines[m_nr]))
			jobs_string = "\n\t" + jobs_string
			machine_strings_list.append(machine_string+jobs_string)
		machine_strings_list = ["Completion time: " + str(self.completion_time)] + machine_strings_list
		return "\n".join(machine_strings_list)


