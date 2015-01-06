class Machine(object):

    def __init__(self, idd):
        self.idd = idd
        self.taskEndTime = 0
        self.jobInProgress = None

