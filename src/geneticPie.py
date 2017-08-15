import random

class Gen():
    """Public class
    Representation of an changeble information for an possible responce."""

    #public
    def __init__(self, *param):

        #public
        name = None

        #public
        individual = None
    class Mutation():
        """Public class
        Executable Mutation for a Gen, must recieve the method 'mutate' to execute when initiated
        Mutate recieve self and the gen, it must change a something in gen, in order to change its value"""

        def __init__(self, param):
            """Public method. Take 'mutate' from param as the method to run."""
            self.mutate = param['mutate']

        def mutate(self, gen):
            """Public Method, change something in Gen in order to change its value.
            Must be overrided."""
            raise Exception('not implemented')

    class Validation():
        """Public class.
        Executable Validation for a Gen, must recieve the method 'validate' to execute when initiated.
        validate recieve self and the Gen, it must change a something in Gen,
        in order to make it have a valid value."""
        
        def __init__(self, param):
            """Public method. Take 'validate' from param as the method to run."""
            self.validate = param['validate']

        def validate(self, gen):
            """Public Method, validate gen in order to make it have an valid value.
            Must be overrided."""
            raise Exception('not implemented')

'''
Gen that has a value
'''
class ValuableGen(Gen):
    def __init__(self, *param):
        self.value = param[0]
        Gen.__init__(self, param.__getslice__(1, param.__len__()-1))
    def treate_attr(self, atr, default, param):
        """Portected Method.
        Validate if atr is in param, and extends default.__class__.
        If param[atr] does not extend default.__class__, but is true, raise And Exeption.
        If there is no param[atr], set default to self.atr, else, set paraḿ[atr]"""
        setattr(self, atr, param[atr] if atr in param.keys() else default)
        if default != None and not issubclass(getattr(self, atr).__class__, default.__class__):
            raise Exception(str(atr) + ' must extend ' + default.__class__.__name__)

    def treate_list_class(self, lst, cls, msg):
        """Portected Method.
        Validate values in lst extend cls,
        if there is nay that does not, raise Exeption with msg."""
        if [x for x in lst if not (issubclass(x.__class__, cls))]:
            raise Exception(msg)

    def __init__(self, param):
        """Public Method.
        It initiates Gen, receiving and dict as param.
        In param this method takes values with keys: 'mutation_list', 'validation_list', 'req_gens'.
        The first two as lists of mutation and validation, and the last as an dict for the required other gens.
        'req_gens' must have functions as value, that returns Gen"""
        self.treate_attr('mutation_list', [], param)
        self.treate_attr('validation_list', [], param)
        self.treate_attr('req_gens', {}, param)
        self.treate_list_class(self.mutation_list, Gen.Mutation, 
            'elements in mutation_list must extend Mutation')
        self.treate_list_class(self.validation_list, Gen.Validation, 
            'elements in validation_list must extend Validation')
        self.treate_list_class([x() for x in self.req_gens.values()], Gen, 
            'values in req_gens must extend Gen')

    def mutate(self):
        """Public Method.
        In 20% of times, it takes one of mutation_list and execute it.
        If there is not any Mutation avaliable, nothing happens."""
        if self.mutation_list and not random.randint(0,4):
            random.choice(self.mutation_list).mutate(self)

    def validade(self):
        """Public Method.
        Execute every Validation in validation_list."""
        for val in self.validation_list:
            val.validate(self)

    def new_instace(self):
        """Public Method.
        Returns a new instance of the object's class.
        The parameters will be passed as self.__dict__ to self.__init__"""
        return self.__class__(self.__dict__)

    def __str__(self):
        return str(self.value);

'''
Gen that implements an run method
'''
class RunnableGen(Gen):
class ValuableGen(Gen):
    """Public Class.
    Gen that has a value."""

    def __init__(self, param):
        """Public Method.
        Initialize ValuableGen the same way Gen, adding treatement to 'value' param.
        There's no native validation for 'value'"""
        Gen.treate_attr(self, 'value', None, param)
        Gen.__init__(self, param)

class RunnableGen(Gen):
    """Public Class.
    Gen that implements an run method."""

    def __init__(self, param):
        """Public Method.
        Initialize ValuableGen the same way Gen, adding treatement to 'individual' param.
        individual must implement Individual."""
        Gen.treate_attr(self, 'individual', None, param)
        Gen.__init__(self, param)

    def run(self, param):
        """Public Method. Execute some task, returnnig or not.
        Must be overrided."""
        raise Exception('not implemented')

class Individual():
    """Public Class.
    Representation of an possible response."""

    def __init__(self, gens):
        """Public Method
        Initiate Individual inserting gens ant its required Gens."""

        def select_adds(self, gens):
            """Private method."""
            def is_to_contiue(instance, name, gens, adds):
                """Private method."""
                return ((instance not in self.gens.values() and instance not in adds.values()) 
                    and (not issubclass(instance.__class__, gens[name].__class__) if 
                        name in gens.keys() else True))

            adds = {}
            for g in gens.values():
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
        """Public Method.
        Calculate and return an numerical indicator of Individual addaptability.
        Zero is te perfect response, representing that the individual is the most optimizated response.
        Must be overrided."""
        raise Exception('not implemented')

    def crossover(self, partner):
        """Public Method
        Return a new instance of the Indiviual class, based on its gens end partner gens."""
        if not issubclass(partner.__class__, Individual):
            raise Exception("partner must be an Individual")
        new_ind = self.__class__({k : v.new_instace() for k,v in {**self.gens, **partner.gens}.items()})
        for gen in new_ind.gens.values():
            gen.mutate()
            gen.validade()
        return new_ind

    def new_instace(self):
        """Public Method.
        Returns a new instance of the object's class."""
        return self.__class__({ k : v.new_instace() for k, v in self.gens.items()})

class Simulation():
    """Public Class.
    Simulation of the blarp"""

    def __init__(self):
        """Public Method"""
        self.population = []

    def sort_by_fitness(self, param):
        """Public Method"""
        def key(ind):
            return ind.calculate_fitness(param)

        self.population.sort(key = key)
        return self

class Default():
    """Public Static Class.
    Default owns Default Gen, Mutation and Validation implementations."""

    class Mut():
        """Private class."""
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

        int_list = [Gen.Mutation({'mutate' : add_1}),
            Gen.Mutation({'mutate' : sub_1}),
            Gen.Mutation({'mutate' : mul_1}),
            Gen.Mutation({'mutate' : add_10}),
            Gen.Mutation({'mutate' : sub_10}),
            Gen.Mutation({'mutate' : mul_10}),
            Gen.Mutation({'mutate' : add_100}),
            Gen.Mutation({'mutate' : sub_100}),
            Gen.Mutation({'mutate' : mul_100}),
            Gen.Mutation({'mutate' : mod_10}),
            Gen.Mutation({'mutate' : mod_100})]

        float_list =[*int_list,
            Gen.Mutation({'mutate' : div_1}),
            Gen.Mutation({'mutate' : div_10}),
            Gen.Mutation({'mutate' : div_100}),
            Gen.Mutation({'mutate' : add_05}),
            Gen.Mutation({'mutate' : add_01}),
            Gen.Mutation({'mutate' : add_001}),
            Gen.Mutation({'mutate' : sub_05}),
            Gen.Mutation({'mutate' : sub_01}),
            Gen.Mutation({'mutate' : sub_001}),
            Gen.Mutation({'mutate' : mod_1})]

    class Val():
        """Private Class."""
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

        not_null_list = [Gen.Validation({'validate' : not_null})]
        simplify_frac_list = [Gen.Validation({'validate' : simplify_frac})]

    int_mut_list = Mut().int_list
    float_mut_list = Mut().float_list

    class IntGen(ValuableGen):
        """Public Class.
        IntGen represents an integer value."""
        def __init__(self, param):
            ValuableGen.__init__(self, {'mutation_list' : Default.Mut.int_list, 'value': 0, **param}) 

    class FltGen(ValuableGen):
        """Public Class.
        FltGen represents an float value."""
        def __init__(self, param):
            ValuableGen.__init__(self, {'mutation_list' : Default.Mut.float_list, 'value': 0, **param}) 
            
    class FracGen(RunnableGen):
        """Public Class.
        FracGen represents an float value get by the division of two integers."""
        def __init__(self, param):
            if 'names' in param.keys():
                self.names = param['names']
            else:
                self.names = [str(random.randint(0,99)) + 'd' + str(x+1) for x in range(2)]

            ValuableGen.__init__(self, 
                {'req_gens' : {self.names[0]:self.get_gen({'value' : 0}), 
                    self.names[1]:self.get_gen({'validation_list' : Default.Val.not_null_list, 'value' : 1})},
                    'validation_list':Default.Val.simplify_frac_list,**param})

        def run(self, param):
            return self.individual.gens[self.names[0]].value/self.individual.gens[self.names[1]].value

        def get_gen(self, param):
            def get():
                return Default.IntGen(param)
            return get

        def __str__(self):
            return (str(self.individual.gens[self.names[0]].value) + '/' +
                str(self.individual.gens[self.names[1]].value))