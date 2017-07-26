import random

'''
Representation of an changeble information for an possible responce.
'''
class Gen():

    #public
    class mutation():
        def mutate(self, gen):
            raise Exception('not implemented')

    #public
    def __init__(self, param):
        self.mutation_list = param['mutation_list'] if 'mutation_list' in param else []
        self.req_gens = param['req_gens'] if 'req_gens' in param else {}
        if self.mutation_list.__class__ != list:
            raise Exception('mutation_list must be a list')
        if self.req_gens.__class__ != dict:
            raise Exception('req_gens must be a dict')

    #public
    def mutate(self):
        if (len(mutation_list) == 1):
            mutation_list[0].mutate(self)
        elif (len(mutation_list) > 1):
            random.sample(mutation_list, 1)[0].mutate(gen)
    #public
    def new_instace(self):
        return self.__class__(self.get_new_instace_param())

    #protected
    def get_new_instace_param(self):
        return {'mutation_list':self.mutation_list, 'req_gens':self.req_gens}

'''
Gen that has a value
'''
class ValuableGen(Gen):

    #public
    def __init__(self, param, value = None):
        Gen.__init__(self, param)
        self.value = value if value else param['value'] if 'value' in param else value

    #public
    def new_instace(self):
        return self.__class__(self.get_new_instace_param(), value = self.value)

'''
Gen that implements an run method
'''
class RunnableGen(Gen):

    #public
    def __init__(self, param, individual = None):
        self.individual = individual
        Gen.__init__(self, param)

    #public
    def new_instace(self):
        return self.__class__(self.get_new_instace_param(), individual =  self.individual)

    #public
    def run(self, param):
        raise Exception('not implemented')

'''
Representation of an possible response.
'''
class Individual():

    #public 
    def __init__(self, gens):
        if len([x for x in gens.values() if not issubclass(x.__class__, Gen)]) > 0:
            raise Exception('gens must extend Gen') 

        self.gens = gens
        for g in self.gens.values():
            for gen_name, new_instace in g.req_gens.items():                
                instance = new_instace()
                instance_name = gen_name
                i = 0
                while instance not in self.gens.values():
                    instance_name = gen_name + ("_"+str(i) if i else "")
                    if not instance_name in self.gens.keys() or issubclass(self.gens[instance_name].__class__, instance.__class__):
                        self.gens[instance_name] = instance
                    else:
                        i = i + 1
                if instance_name != gen_name:
                    g.req_gens[instance_name] = g.req_gens.pop(gen_name)

        for x in(x for x in self.gens.values() if issubclass(g.__class__, RunnableGen)):
            g.individual = self

    #public
    def calculate_fitness(self, param):
        raise Exception('not implemented')

    #public
    def crossover(self, partner):
        if not issubclass(partner.__class__, Individual):
            raise Exception("partner must be an Individual")
        return self.__class__({**self.gens, **partner.gens})

    #public
    def new_instace(self):
        return self.__class__({ k : v.new_instace for k, v in self.gens.items()})

class Simulation():

    #public
    def __init__(self):
        self.population = []

    #public
    def sort_by_fitness(self, param):
        def sorter(x, y):
            if x > y:
                return 1
            else:
                if x < y:
                    return -1
            return 0

        def sub_sorter(ind_x, ind_y):
            return sorter(ind_x.calculate_fitness(param), ind_y.calculate_fitness(param))

        self.population.sort(cmp = sub_sorter)
        return sel

help(Gen)