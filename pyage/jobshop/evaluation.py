from math import cos, pi, sin, sqrt
from pyage.core.operator import Operator

class Evaluation(Operator):
    #TODO
    def __init__(self):
        raise NotImplementedError()
    '''
    def __init__(self):
        super(FloatRastriginEvaluation, self).__init__(FloatGenotype)

    def process(self, population):
        for genotype in population:
            genotype.fitness = - self.__rastrigin(genotype.genes)

    def __rastrigin(self, genes):
        sum = len(genes) * A
        for gene in genes:
            sum += gene ** 2 - A * cos(2 * pi * gene)
        return sum
    '''
