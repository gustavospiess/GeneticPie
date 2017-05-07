import utils
from utils import *

class Gen():

    #public
    def __init__(self, value = None):
        self.value = value

    #public
    def get_needed_gens(self):
        raise Exception('not implemented')

    #public
    def is_mutable(self, *param):
        raise Exception('not implemented')

    #public
    def mutate(self, *param):
        raise Exception('not implemented')

    #public
    def is_crossoverble(self, *param):
        raise Exception('not implemented')        

    #public
    def crossover(self, *param):
        raise Exception('not implemented')

class Individual():

    def __init__(self, gens):
        self.gens = gens
        for g in gens.values():
            for k, v in g.get_needed_gens().items():
                self[k] = v()