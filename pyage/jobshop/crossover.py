import random
from pyage.core.operator import Operator

class AbstractCrossover(Operator):
    def __init__(self, type, population_size):
        super(AbstractCrossover, self).__init__(type)
        self.__size = population_size

    def process(self, population):
        parents = list(population)
        for i in range(len(population), self.__size):
            p1, p2 = random.sample(parents, 2)
            genotype = self.cross(p1, p2)
            population.append(genotype)

class Crossover(AbstractCrossover):
    #TODO!
    def __init__(self, population_size=100):
        raise NotImplementedError()
    '''
    def __init__(self, size=100):
        super(SinglePointCrossover, self).__init__(FloatGenotype, size)


    def cross(self, p1, p2):
        crossingPoint = random.randint(1, len(p1.genes))
        return FloatGenotype(p1.genes[:crossingPoint] + p2.genes[crossingPoint:])
    '''
