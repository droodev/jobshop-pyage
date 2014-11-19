from pyage.core.address import Addressable
from pyage.core.agent.agent import AbstractAgent
from pyage.core.inject import Inject
import logging

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
                logger.debug("NEW PROBLEM: \n%s", new_problem)
            agent.step()
        self.steps += 1

    def get_agents(self):
        return self.__slaves.values()

    def get_fitness(self):
        return 0;

class SlaveAgent():
    def __init__(self):
        self.steps = 0

    def step(self):
        logger.debug("Slave step")
        self.steps += 1

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
