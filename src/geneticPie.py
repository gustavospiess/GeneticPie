import random
import copy

class Gen():
    """Public Class
    Representation of an changeble information for an possible responce."""

    def __init__(self, param):
        """Public Method
        It initiates Gen, receiving and dict as param.
        In param this method takes values with keys: 'mutation_list', 'validation_list'.
        The first two as lists of mutation and validation, and the last as an dict for the required other gens."""
        self.mutation_list = param['mutation_list'] if 'mutation_list' in param else []
        self.validation_list = param['validation_list'] if 'validation_list' in param else []

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
        """Public Method
        In 20% of times, it takes one of mutation_list and execute it.
        If there is not any Mutation avaliable, nothing happens."""
        if self.mutation_list and not random.randint(0,4):
            random.choice(self.mutation_list).mutate(self)

    def validade(self):
        """Public Method
        Execute every Validation in validation_list."""
        for val in self.validation_list:
            val.validate(self)

    def new_instace(self):
        """Public Method
        Returns a new instance of the object's class.
        The parameters will be passed as self.__dict__ to self.__init__"""
        return copy.deepcopy(self)

    def __str__(self):
        return str(self.value);



class Mutation():
    """Public Class
    Executable Mutation for a Gen, must recieve the method 'mutate' to execute when initiated
    Mutate recieve self and the gen, it must change a something in gen, in order to change its value"""

    def __init__(self, param = None, mutate = None):
        """Public Method 
        Initiate Mutation with mutate (if defined) or param['mutate'].
        mutate must be an fuction, that receives self (mutation) and gen (Gen)."""
        self.mutate = mutate if mutate else param['mutate']

    def mutate(self, gen):
        """Public Method
        change something in Gen in order to change its value.
        Must be overrided."""
        raise NotImplementedError()

class Validation():
    """Public Class
    Executable Validation for a Gen, must recieve the method 'validate' to execute when initiated.
    validate recieve self and the Gen, it must change a something in Gen,
    in order to make it have a valid value."""
    
    def __init__(self, param = None, validate = None):
        """Public Method
        Initiate Validation with validate (if defined) or param['validate'].
        validate must be an fuction, that receives self (validation) and gen (Gen)."""
        self.validate = vlaidade if validate else param['validate']

    def validate(self, gen):
        """Public Method
        validate gen in order to make it have an valid value.
        Must be overrided."""
        raise NotImplementedError()



class ValuableGen(Gen):
    """Public Class
    Gen that has a value."""

    def __init__(self, param):
        """Public Method
        Initialize ValuableGen the same way Gen, adding treatement to 'value' param.
        There's no native validation for 'value'"""
        self.value = param['value'] if 'value' in param else None
        Gen.__init__(self, param)

        @property
        def value(self): return self.__value
        @value.setter
        def value(self, v): self.__value = v

class RunnableGen(Gen):
    """Public Class
    Gen that implements an run method."""

    def __init__(self, param):
        """Public Method
        Initialize ValuableGen the same way Gen, adding treatement to 'individual' and 'req_gens' paramethers.        
        req_gens must be a dict that have functions as value, that returns Gen.
        individual must implement Individual."""
        self.names = param['names'] if 'names' in param else []
        self.individual = para['individual'] if 'individual' in param else None
        self.req_gens = param['req_gens'] if 'req_gens' in param else {}
        Gen.__init__(self, param)

        @property
        def req_gens(self): return self._req_gens

        @req_gens.setter
        def req_gen(self, rg):
            if (not all_subclass(rg.values(), Gen)):
                raise TypeError('values in req_gens must extend Gen')
            self._req_gens = rg

    def run(self, param):
        """Public Method Execute some task, returnnig or not.
        Must be overrided."""
        raise NotImplementedError()

class Individual():
    """Public Class
    Representation of an possible response."""

    def __init__(self, gens):
        """Public Method
        Initiate Individual inserting gens ant its required Gens.
        gens must be an dict of Gen objects."""

        def select_adds(self, gens):
            """Private Method"""
            def is_to_contiue(instance, name, gens, adds):
                """Private Method"""
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
        """Public Method
        Calculate and return an numerical indicator of Individual addaptability.
        Zero is te perfect response, representing that the individual is the most optimizated response.
        Must be overrided."""
        raise NotImplementedError()

    def crossover(self, partner):
        """Public Method
        Return a new instance of the Indiviual class, based on its gens end partner gens."""
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
        """Public Method
        Returns a new instance of the object's class."""
        return copy.deepcopy(self)

class Simulation():
    """Public Class
    Simulation of the blarp"""

    def __init__(self, population = None):
        """Public Method"""
        if population:
            self.population = population
        else:
            self.population = []

        self.ind_params = []

    def eliminate(self, list_selector = None, single_selector = None):
        """Public Method
        Sort population using the last value passad to this object's attribute sort_by_fitness.
        If list_selector is received, the new population is the return of it.
        list_selector must be a function that receive the current population as paramether
        Else, if single_selector is received, the new population will be the part of 
        the current that being passed to single_selector makes it return true"""
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
        """Public Method"""

        if param and not param in self.ind_params:
            self.ind_params.append(param)

        def key(ind):   return ind.calculate_fitness(self.ind_params[-1])

        self.population.sort(key = key)
        return self

class Default():
    """Public Static Class.
    Default owns Default Gen, Mutation and Validation implementations."""

    class Mut():
        """Private Class"""
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

        int_list = [Mutation({'mutate' : add_1}),
            Mutation({'mutate' : sub_1}),
            Mutation({'mutate' : mul_1}),
            Mutation({'mutate' : add_10}),
            Mutation({'mutate' : sub_10}),
            Mutation({'mutate' : mul_10}),
            Mutation({'mutate' : add_100}),
            Mutation({'mutate' : sub_100}),
            Mutation({'mutate' : mul_100}),
            Mutation({'mutate' : mod_10}),
            Mutation({'mutate' : mod_100})]

        float_list =[*int_list,
            Mutation({'mutate' : div_1}),
            Mutation({'mutate' : div_10}),
            Mutation({'mutate' : div_100}),
            Mutation({'mutate' : add_05}),
            Mutation({'mutate' : add_01}),
            Mutation({'mutate' : add_001}),
            Mutation({'mutate' : sub_05}),
            Mutation({'mutate' : sub_01}),
            Mutation({'mutate' : sub_001}),
            Mutation({'mutate' : mod_1})]

    class Val():
        """Private Class"""
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

        not_null_list = [Validation({'validate' : not_null})]
        simplify_frac_list = [Validation({'validate' : simplify_frac})]

    int_mut_list = Mut().int_list
    float_mut_list = Mut().float_list

    class IntGen(ValuableGen):
        """Public Class
        IntGen represents an integer value."""
        def __init__(self, param):
            ValuableGen.__init__(self, {'mutation_list' : Default.Mut.int_list, 'value': 0, **param}) 

    class FltGen(ValuableGen):
        """Public Class
        FltGen represents an float value."""
        def __init__(self, param):
            ValuableGen.__init__(self, {'mutation_list' : Default.Mut.float_list, 'value': 0, **param}) 
            
    class FracGen(RunnableGen):
        """Public Class
        FracGen represents an float value get by the division of two integers."""
        def __init__(self, param):
            if not 'names' in param or len(param['names']) != 2: 
                param['names'] = [str(random.randint(0,99)) + 'd' + str(x+1) for x in range(2)]

            RunnableGen.__init__(self, 
                {'req_gens' : {param['names'][0]:self.get_gen({'value' : 0}), 
                    param['names'][1]:self.get_gen({'validation_list' : Default.Val.not_null_list, 'value' : 1})},
                    'validation_list':Default.Val.simplify_frac_list,
                    **param})

        def run(self, param):
            """Public Method"""
            return self.individual.gens[self.names[0]].value/self.individual.gens[self.names[1]].value

        def get_gen(self, param):
            def get():
                return Default.IntGen(param)
            return get

        def __str__(self):
            self.validade()
            up = self.individual.gens[self.names[0]].value
            down = self.individual.gens[self.names[1]].value            
            return (str(up) + ('/' + str(down) if (down - 1) else ''))