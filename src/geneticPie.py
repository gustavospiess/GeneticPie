import random
import copy

class Gen(object):

    def __init__(self, mutation_list = [], validation_list = []):
        self.mutation_list = mutation_list
        self.validation_list = validation_list

    def all_subclass(self, lst, cls):
        for x in lst:
            if not issubclass(x.__class__, cls): return False
        return True

    @property
    def validation_list(self): return self.__validation_list

    @validation_list.setter
    def validation_list(self, vl):
        if (not self.all_subclass(vl, Validation)):
            raise TypeError('elements in validation_list must extend Validation')
        self.__validation_list = vl

    @property
    def mutation_list(self): return self.__mutation_list

    @mutation_list.setter
    def mutation_list(self, ml):
        if (not self.all_subclass(ml, Mutation)):
            raise TypeError('elements in mutation_list must extend Mutation')
        self.__mutation_list = ml

    def mutate(self):
        if self.mutation_list and not random.randint(0,4):
            random.choice(self.mutation_list).mutate(self)

    def validade(self):
        for val in self.validation_list:
            val.validate(self)

    def new_instace(self):
        return copy.deepcopy(self)

    def __str__(self):
        return str(self.value);

class ValuableGen(Gen):

    def __init__(self, value = None, mutation_list = [], validation_list = []):
        self.value = value
        Gen.__init__(self, mutation_list = mutation_list, validation_list = validation_list)

        @property
        def value(self): return self.__value
        @value.setter
        def value(self, v): self.__value = v

class RunnableGen(Gen):

    def __init__(self, names = [], individual = None, req_gens = {},mutation_list = [], validation_list = []):
        self.names = names if names else [k for k in req_gens.keys()]
        self.individual = individual
        self.req_gens = req_gens
        Gen.__init__(self, mutation_list = mutation_list, validation_list = validation_list)

        @property
        def req_gens(self): return self._req_gens

        @req_gens.setter
        def req_gen(self, rg):
            if (not all_subclass(rg.values(), Gen)):
                raise TypeError('values in req_gens must extend Gen')
            self._req_gens = rg

    def run(self, param):
        raise NotImplementedError()

class Mutation(object):

    def __init__(self, mutate = None):
        self.mutate = mutate if mutate else param['mutate']

    def mutate(self, gen):
        raise NotImplementedError()

class Validation(object):
    
    def __init__(self, validate = None):
        self.validate = validate if validate else param['validate']

    def validate(self, gen):
        raise NotImplementedError()

class Default():

    class Mut():
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
        def div_1(gen):
            gen.value /= 1
        def div_10(gen):
            gen.value /= 10
        def div_100(gen):
            gen.value /= 100
        def add_05(gen):
            gen.value += 0.5
        def add_01(gen):
            gen.value += 0.1
        def add_001(gen):
            gen.value += 0.01
        def sub_05(gen):
            gen.value -= 0.5
        def sub_01(gen):
            gen.value -= 0.1
        def sub_001(gen):
            gen.value -= 0.01
        def mod_001(gen):
            gen.value = gen.value - gen.value%0.01
        def mod_01(gen):
            gen.value = gen.value - gen.value%0.1
        def mod_1(gen):
            gen.value = gen.value - gen.value%1
        def mod_10(gen):
            gen.value = gen.value - gen.value%10
        def mod_100(gen):
            gen.value = gen.value - gen.value%100

        int_list = [Mutation(mutate = add_1),
            Mutation(mutate = sub_1),
            Mutation(mutate = mul_1),
            Mutation(mutate = add_10),
            Mutation(mutate = sub_10),
            Mutation(mutate = mul_10),
            Mutation(mutate = add_100),
            Mutation(mutate = sub_100),
            Mutation(mutate = mul_100),
            Mutation(mutate = mod_10),
            Mutation(mutate = mod_100)]

        float_list =[*int_list,
            Mutation(mutate = div_1),
            Mutation(mutate = div_10),
            Mutation(mutate = div_100),
            Mutation(mutate = add_05),
            Mutation(mutate = add_01),
            Mutation(mutate = add_001),
            Mutation(mutate = sub_05),
            Mutation(mutate = sub_01),
            Mutation(mutate = sub_001),
            Mutation(mutate = mod_1)]

    class Val():
        def not_null(gen):
            if not gen.value:
                gen.value = 1 

        def simplify_frac(gen):
            d1 = gen.individual.gens[gen.names[0]]
            d2 = gen.individual.gens[gen.names[1]]

            primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
                53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

            for p in primes:
                while True:
                    if not (d1.value%p) and not (d2.value%p):
                        d1.value /= p
                        d2.value /= p
                        continue
                    break

            if d2.value < 0:
                d2.value *= -1
                d1.value *= -1

            d1.value = int(d1.value)
            d2.value = int(d2.value)

        not_null_list = [Validation(validate = not_null)]
        simplify_frac_list = [Validation(validate = simplify_frac)]

    int_mut_list = Mut().int_list
    float_mut_list = Mut().float_list

    class IntGen(ValuableGen):
        def __init__(self, mutation_list = None, value = 0, validation_list = []):
            if not mutation_list: mutation_list = Default.int_mut_list
            ValuableGen.__init__(self, mutation_list = mutation_list, value = value, validation_list = validation_list) 

    class FltGen(ValuableGen):
        def __init__(self, mutation_list = None, value = 0, validation_list = []):
            if not mutation_list: mutation_list = Default.float_list
            ValuableGen.__init__(self, mutation_list = mutation_list, value = value, validation_list = validation_list) 
            
    class FracGen(RunnableGen):
        def __init__(self, names = [], individual = None, req_gens = {},mutation_list = [], validation_list = []):
            if names or len(names) != 2: 
                names = [str(random.randint(0,99)) + 'd' + str(x+1) for x in range(2)]

            r1 = self.get_gen(validation_list =  Default.Val.not_null_list, value = 1)
            r2 = self.get_gen(value = 1)

            RunnableGen.__init__(self, 
                req_gens = {names[0]:r2, names[1]:r1},
                    validation_list = Default.Val.simplify_frac_list,
                    names = names, individual = individual, mutation_list = mutation_list)

        def run(self, param):
            return self.individual.gens[self.names[0]].value/self.individual.gens[self.names[1]].value

        def get_gen(self, **param):
            def get():
                return Default.IntGen(**param)
            return get

        def __str__(self):
            self.validade()
            up = self.individual.gens[self.names[0]].value
            down = self.individual.gens[self.names[1]].value            
            return (str(up) + ('/' + str(down) if (down - 1) else ''))

class Individual(object):

    def __init__(self, gens):

        def select_adds(self, gens):
            def is_to_contiue(instance, name, gens, adds):
                return ((instance not in self.gens.values() and instance not in adds.values()) 
                    and (not issubclass(instance.__class__, gens[name].__class__) if 
                        name in gens.keys() else True))

            adds = {}
            for g in [g for g in gens.values() if issubclass(g.__class__, RunnableGen)]:
                for gen_name, new_instace in g.req_gens.items():
                    instance = new_instace()
                    instance_name = gen_name
                    i = 0
                    while is_to_contiue(instance, instance_name, gens, adds):
                        instance_name = gen_name + ("_"+str(i) if i else "")
                        if (not instance_name in self.gens.keys() or
                            issubclass(self.gens[instance_name].__class__, instance.__class__)):
                            adds[instance_name] = instance
                        i += 1
                    if instance_name != gen_name:
                        g.req_gens[instance_name] = g.req_gens.pop(gen_name)
                        g.names[g.names.index(gen_name)] = instance_name
            return adds

        self.gens = gens
        adds = None
        first = True
        while first or adds:
            first = False
            adds = select_adds(self, gens)
            self.gens = {**self.gens, **adds}
            gens = adds

        for w in(x for x in self.gens.values() if issubclass(x.__class__, RunnableGen)):
            w.individual = self

    def calculate_fitness(self, param):
        raise NotImplementedError()

    def crossover(self, partner):
        if not issubclass(partner.__class__, Individual):
            raise TypeError("partner must be an Individual")

        gen_name_list = [*self.gens.keys(), *partner.gens.keys()]
        gen_dict = { name : random.choice((self.gens[name], self.gens[name])) for name in gen_name_list}
        new_ind = self.__class__({k : v.new_instace() for k,v in gen_dict.items()})
        for gen in new_ind.gens.values():
            gen.mutate()
            gen.validade()
        return new_ind

    def new_instace(self):
        return copy.deepcopy(self)

class Simulation(object):

    def __init__(self, population = None):
        if population:
            self.population = population
        else:
            self.population = []

        self.ind_params = []

    def eliminate(self, list_selector = None, single_selector = None):
        self.sort_by_fitness()
        before = len(self.population)
        if (list_selector):
            self.population = list_selector(self.population)
        elif single_selector:
            self.population = [ind for ind in self.population if single_selector(ind)]
        else:
            self.population = self.population[0:int((len(self.population)+1)/2)]

        return before-len(self.population)

    def sort_by_fitness(self, param = None):

        if param and not param in self.ind_params:
            self.ind_params.append(param)

        def key(ind):   return ind.calculate_fitness(self.ind_params[-1])

        self.population.sort(key = key)
        return self
