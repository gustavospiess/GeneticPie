import random

'''
Representation of an changeble information for an possible responce.
'''
class Gen():

    #public
    class Mutation():
        def __init__(self, param):
            self.mutate = param['mutate']

        def mutate(self, gen):
            raise Exception('not implemented')

    #public
    def __init__(self, param):
        self.mutation_list = param['mutation_list'] if 'mutation_list' in param.keys(   ) else []
        self.req_gens = param['req_gens'] if 'req_gens' in param else {}
        if self.mutation_list.__class__ != list:
            raise Exception('mutation_list must be a list')
        if self.req_gens.__class__ != dict:
            raise Exception('req_gens must be a dict')

    #public
    def mutate(self):
        if random.randint(0,9) == 0:
            if (len(self.mutation_list) == 1):
                self.mutation_list[0].mutate(self)
            elif (len(self.mutation_list) > 1):
                random.choice(self.mutation_list).mutate(self)
    #public
    def new_instace(self):
        return self.__class__(self.__dict__)

'''
Gen that has a value
'''
class ValuableGen(Gen):

    #public
    def __init__(self, param):
        Gen.__init__(self, param)
        self.value = param['value'] if 'value' in param.keys() else None

'''
Gen that implements an run method
'''
class RunnableGen(Gen):

    #public
    def __init__(self, param):
        self.individual = param['individual'] if 'individual' in param.keys() else None
        Gen.__init__(self, param)

    #public
    def new_instace(self):
        return self.__class__(self.__dict__)

    #public
    def run(self, param):
        raise Exception('not implemented')

'''
Representation of an possible response.
'''
class Individual():

    #public
    def __init__(self, gens):
        #gens = {k : v() if issubclass(self.new_instace.__class__, v.__class__) else v for k, v in gens.items()}
        if len([x for x in gens.values() if not issubclass(x.__class__, Gen)]) > 0:
            raise Exception('gens must extend Gen')

        self.gens = {}

        def add_gen(self, gens):
            adds = {}
            for g in gens.values():
                for gen_name, new_instace in g.req_gens.items():
                    instance = new_instace()
                    instance_name = gen_name
                    if (instance_name in self.gens.keys() and
                        issubclass(self.gens[instance_name].__class__, instance.__class__)):
                        continue
                    i = 0
                    while instance not in self.gens.values() and instance not in adds.values():
                        instance_name = gen_name + ("_"+str(i) if i else "")
                        if (not instance_name in self.gens.keys() or
                            issubclass(self.gens[instance_name].__class__, instance.__class__)):
                            adds[instance_name] = instance
                        else:
                            if issubclass(instance.__class__, self.gens[instance_name].__class__):
                                break
                            i = i + 1
                    if instance_name != gen_name:
                        g.req_gens[instance_name] = g.req_gens.pop(gen_name)
            return adds

        self.gens = gens
        adds = None
        first = True
        while first or adds:
            first = False
            adds = add_gen(self, gens)
            self.gens = {**self.gens, **adds}

        for w in(x for x in self.gens.values() if issubclass(x.__class__, RunnableGen)):
            w.individual = self

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
        return self.__class__({ k : v.new_instace() for k, v in self.gens.items()})

class Simulation():

    #public
    def __init__(self):
        self.population = []

    #public
    def sort_by_fitness(self, param):
        def key(ind):
            return ind.calculate_fitness(param)

        self.population.sort(key = key)
        return self

class Default():
    def add_1(gen):
        gen.value += 1
    def add_10(gen):
        gen.value += 10
    def add_100(gen):
        gen.value += 100
    def sub_1(gen):
        gen.value -= 1
    def sub_10(gen):
        gen.value -= 10
    def sub_100(gen):
        gen.value -= 100
    def mul_1(gen):
        gen.value *= 1
    def mul_10(gen):
        gen.value *= 10
    def mul_100(gen):
        gen.value *= 100

    DefaultIntMutation = [Gen.Mutation({'mutate' : add_1}),
        Gen.Mutation({'mutate' : sub_1}),
        Gen.Mutation({'mutate' : mul_1}),
        Gen.Mutation({'mutate' : add_10}),
        Gen.Mutation({'mutate' : sub_10}),
        Gen.Mutation({'mutate' : mul_10}),
        Gen.Mutation({'mutate' : add_100}),
        Gen.Mutation({'mutate' : sub_100}),
        Gen.Mutation({'mutate' : mul_100})]
    #public
    class IntGen(ValuableGen):
        def __init__(self, param):
            ValuableGen.__init__(self, {'mutation_list' : Default.DefaultIntMutation, 'value': 0, **param})