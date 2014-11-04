from pyage.core.address import Addressable
from pyage.core.agent.agent import AbstractAgent
from pyage.core.inject import Inject
import logging

logger = logging.getLogger(__name__)

class MasterAgent(Addressable, AbstractAgent):
    @Inject("slaves:_MasterAgent__slaves")
    def __init__(self, name=None):
        self.name = name
        super(MasterAgent, self).__init__()
        for agent in self.__slaves.values():
            agent.parent = self
        self.steps = 0

    def step(self):
        for agent in self.__slaves.values():
            agent.step()

    def remove_agent(self, agent):
        agent = self.__slaves[agent.get_address()]
        del self.__slaves[agent.get_address()]
        agent.parent = None
        return agent

    def add_agent(self, agent):
        agent.parent = self
        self.__slaves[agent.get_address()] = agent

    def get_agents(self):
        return self.__slaves.values()

    def get_fitness(self):
        try:
            return max(agent.get_fitness() for agent in self.__slaves.values())
        except ValueError:
            return None

    def get_best_genotype(self):
        return max(self.__slaves.values(), key=lambda a: a.get_fitness()).get_best_genotype()


class SlaveAgent():
    #TODO
    def __init__(self):
        raise NotImplementedError()

def masters_factory(count):
    return _agents_factory(count, MasterAgent)

def slaves_factory(count):
    #TODO
    raise NotImplementedError()

def _agents_factory(count, agent_type):
    def factory():
        agents = {}
        for name in args:
            agent = agent_type()
            agents["Master_" + str(count)] = agent
        return agents
    return factory
