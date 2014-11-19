class Problem(object):
    def __init__(self, jobs_list):
        self.jobs_list = jobs_list

    def __str__(self):
    	return "\n".join(map(str,self.jobs_list))

class Job(object):
	def __init__(self, jid, tasks_list):
		self.jid = jid
		self.tasks_list = tasks_list

	def __str__(self):
		caption = "Job " + str(self.jid)
		joined = "\n\t".join(map(str,self.tasks_list))
		return caption + "\n\t" + joined


class Task(object):
	def __init__(self, machine, duration):
		self.machine = machine
		self.duration = duration

	def __str__(self):
		return "Task at machine: " + str(self.machine) + " lasting: " + str(self.duration) 
