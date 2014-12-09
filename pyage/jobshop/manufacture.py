import logging
import copy

from machine import Machine
from problem import Job, Problem


logger = logging.getLogger(__name__)

class Manufacture(object):
    history = []
    def __init__(self, machines_nr):
        self.machines_nr = machines_nr
        self.machines = [Machine(i) for i in xrange(machines_nr)]
        #to be fixed - workaround
        for machine in self.machines:
            machine.taskEndTime = 0
        self.time = -1

    def assign_tasks(self, solution):
        logger.debug("Manufacture solution assigned: \n%s", solution)
        self.solution = copy.deepcopy(solution)


    def time_tick(self, new_time):
        if new_time is self.time:
            return
        logger.debug("Time tick: %d->%d", self.time, new_time)
        self.time = new_time
        self.__check_and_update(self.time)

    def __check_and_update(self, old_time):
        for machine in self.machines:
            if machine.taskEndTime <= old_time:
                logger.debug("Updating machine: %d", machine.idd)
                try:
                    current_job = self.solution.get_machine_job(machine.idd)[0]
                    del self.solution.get_machine_job(machine.idd)[0]
                    task = current_job.get_task_for_machine(machine.idd)
                    machine.taskEndTime = old_time+task.get_duration()
                    logger.debug("New endtime: %d", machine.taskEndTime)
                    self.history.append([ machine.idd, current_job.get_jid(), old_time, task.get_duration(), 'Tick ' + str(old_time) ])
                except IndexError:
                    logger.debug("Nothing to add")

    def get_history(self):
        return self.history

    def get_solution_part_as_problem(self, reverse_depth):
        logger.debug("Taking part as problem")
        tasks_to_leave = 1
        tasks_list = []
        for depth in xrange(reverse_depth):
            for machine in self.machines:
                machine_jobs = self.solution.get_machine_job(machine.idd)
                if len(machine_jobs) < reverse_depth + tasks_to_leave:
                    continue
                last_job = machine_jobs[-1]
                tasks_list.append(last_job.get_task_for_machine(machine.idd))
                self.solution.remove_job_from_machine(machine.idd, last_job)
        #creating problem from tasks_list
        jobs_categorized = dict([(t.job, []) for t in tasks_list])
        for task in tasks_list:
            jobs_categorized[task.job].append(task)

        counter = 0
        jobs_lists = []
        for tlist in jobs_categorized.values():
            jobs_lists.append(Job(counter, tlist))
            counter +=1

        logger.debug("left solution: \n%s", self.solution)
        return Problem(jobs_lists)
