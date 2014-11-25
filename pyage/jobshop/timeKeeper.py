class TimeKeeper(object):
	def __init__(self, resolution, init_time):
		self.time = init_time
		self.resolution = resolution

	def step(self, step):
		if step % self.resolution == 0:
			self.time += 1

	def get_time(self):
		return self.time