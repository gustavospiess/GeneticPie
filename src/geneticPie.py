import utils
from utils import *

'''
Representation of an changeble information for an possible responce.
'''
class Gen():

    #public
    def __init__(self, *param):
        pass

    #public
    def get_req_gens(self):
        raise Exception('not implemented')

    #public
    def is_mutable(self, *param):
        raise Exception('not implemented')
        
    #public
    def mutate(self, *param):
        raise Exception('not implemented')

    def new_instace(self):
        return self.__class__()

'''
Gen that has a value
'''
class ValuableGen(Gen):
    def __init__(self, *param):
        self.value = param[0]

    #public
    def is_mutable(self, *param):
        raise Exception('not implemented')

    def new_instace(self):
        return self.__class__(self.value)

'''
Gen that implements an run method
'''
class RunnableGen(Gen):

    #public
    def __init__(self, *param):
        self.individual = None
        if param and param[0]:
            self.individual = param[0]

    #public
    def run(self, *param):
        raise Exception('not implemented')

    #public
    def is_mutable(self, *param):
        return False

'''

'''
class Individual():

    #public 
    def __init__(self, gens):
        self.gens = gens
        for g in gens.values():
            for k, v in g.get_req_gens().items():
                if not k in self.gens.keys():
                    self.gens[k] = v()
            try:
                g.individual = self
            finally:
                pass

    #public
    def calculate_fitness(self, *param):
        raise Exception('not implemented')

    #public
    def is_crossoverble(self, *param):
        raise Exception('not implemented')        

    #public
    def crossover(self, *param):
        raise Exception('not implemented')

    #public
    def new_instace(self):
        return self.__class__({ k : v.new_instace() for k, v in self.gens.items()})

class Simulation():

    #public
    def __init__(self):
        self.population = []

    #public
    def sort_by_fitness(self, *param):
        def sorter(x, y):
            if x > y:
                return 1
            else:
                if x < y:
                    return -1
            return 0

        def sub_sorter(ind_x, ind_y):
            return sorter(ind_x.calculate_fitness(*param), ind_y.calculate_fitness(*param))

        self.population.sort(cmp = sub_sorter)
        return self