from abc    import ABCMeta, abstractmethod
from copy   import deepcopy
from random import randint, choice
from time   import asctime

#Global configurations
debug = False

class Logger(object):
    """Under construction"""

    def __init__(self, print_log = False, list_log = False):
        if list_log:
            self.logs = []

        self.config = {
            'print_log' : print_log,
            'list_log' : list_log
        }

        def p_log(log): print(log)
        def l_log(log): self.logs.append(log)

        self.methods = {
            'print_log' : p_log,
            'list_log' : l_log
        }

        self.on = len([x for x in self.config.keys() if self.config[x]]) > 0

        def dec(old_method):
            if not self.on:
                return old_method
            def new_method(*args, **k_args):
                log = {'input' : str(args) + str(k_args),
                        'start_time' : str(asctime()),
                        'method' : old_method.__name__}
                output = old_method(*args, **k_args)
                log['output'] = output
                log['end_time'] = str(asctime())
                self.log(log)

                return output
            return new_method

        self.decorator = dec

    def log(self, log): 
        for method in self.config.keys():
            if self.config[method]:
                self.methods[method](log)

logger = Logger(list_log = debug)

class GenBuffer(object):
    """Public Class 
    Represents an possible instance of gen, for chromosome instance construction.
    In this process exists the possibility of not needing to instance every gen that are required.
    GenBuffer has the attributes new_instance, as callable, and gen_class, as the class of the gen.
    new_instance must be an callable, with no parameters, that returns an new instance of gen_class"""

    def __init__(self, new_instace = None, gen_class = None):
        """Public method
        Initiate Gen buffer with new_instance and gen_class as parameter.
        If there is not new_instance, gen_class will be used to instance Gen.
        If there is not gen_class, a value error will be raised."""
        if gen_class:
            self.new_instace = new_instace if new_instace else gen_class
            self.gen_class = gen_class
        else:
            raise ValueError('Tehere is not enough param')

    @classmethod
    def factory_from_gen(cls, gen = None):
        """Public class method
        Instance an GenBuffer from an Gen instance, taking its __class__ and new_instance.
        If gen is not """
        if not gen or not issubclass(gen.__class__, Gen):
            raise ValueError('gen is not defined or does not extends Gen')
        return cls(new_instace = gen.new_instace, gen_class = gen.__class__)

class Gen(object):
    """Public Class
    Representation of an changeable information for an possible response."""

    def create_buffer(self):
        """Creates and returns an GenBuffer instance for the Gen object."""
        return GenBuffer.factory_from_gen(gen = self)

    def all_subclass(self, lst, cls):
        """Protected method
        verify if all elements in iterable lst extends cls"""
        for x in lst:
            if not issubclass(x.__class__, cls): return False
        return True           

    def new_instace(self):
        """Generate an new instance of Gen class or subclass by deepcopy method"""
        return deepcopy(self)

class Mutation(object, metaclass = ABCMeta):
    """Public Class
    Executable Mutation for a Gen, must recieve the method 'mutate' to execute when initiated
    Mutate recieve self and the gen, it must change a something in gen, in order to change its value
    """

    @abstractmethod
    def mutate(self, gen):
        """Public Method
        change something in Gen in order to change its value.
        Must be overrided."""
        raise NotImplementedError()

class Validation(object, metaclass = ABCMeta):
    """Public Class
    Executable Validation for a Gen, must recieve the method 'validate' to execute when initiated.
    validate recieve self and the Gen, it must change a something in Gen,
    in order to make it have a valid value."""

    @abstractmethod
    def validate(self, gen):
        """Public Method
        validate gen in order to make it have an valid value.
        Must be overrided."""
        raise NotImplementedError()

class MutableGen(Gen):
    """Public class.
    That Gen must receive mutation process, as mutation_list (property) and mutate (method).
    When mutate is called, it checks a random value to have a 20% chance of mutating, if mutate
    it randomly take one of mutation_list and run (calling mutate method)
    """

    @property
    def mutation_list(self):
        return self.__mutation_list

    @mutation_list.setter
    def mutation_list(self, ml):
        if not ml:
            raise TypeError('MutableGen must have a not empty mutation_list')
        if (not self.all_subclass(ml, Mutation)):
            raise TypeError('elements in mutation_list must extend Mutation')
        self.__mutation_list = ml

    def mutate(self):
        """Public Method
        If there is something in mutation list, execute self.validate
        and in on in each five times, takes one of mutation_list (randomly) and execute it.
        If there is not any Mutation avaliable, nothing happens."""
        choice(self.mutation_list).mutate(self)

    @staticmethod
    def with_default(cls, mutation_list):
        class New(cls, MutableGen):
            def __init__(self, *args, **k_args):
                self.mutation_list = mutation_list
                super(New, self).__init__(*args, **k_args)
        return New

class ValidatebleGen(Gen):
    """Public class.
    That Gem must receive an validation process, as validation_list (property) and validate(method).
    When validate is called, it calls every Validation in validation_list.
    """

    @property
    def validation_list(self):
        return self.__validation_list

    @validation_list.setter
    def validation_list(self, vl):
        if not vl:
            raise TypeError('ValidatebleGen must have a not empty validaton_list')
        if not self.all_subclass(vl, Validation):
            raise TypeError('elements in validation_list must extend Validation')
        self.__validation_list = vl

    def validate(self):
        """Public Method
        Execute every Validation in validation_list."""
        for val in self.validation_list:
            val.validate(self)

    @staticmethod
    def with_default(cls, validation_list):
        class New(cls, ValidatebleGen):
            def __init__(self, *args, **k_args):
                self.validation_list = validation_list
                super(New, self).__init__(*args, **k_args)
        return New
                
class RequierGen(Gen):
    """Public Class.
    That gen must require an dictionary of other gens in the same Chromosome it belongs.
    The Gen's that are required are represented in req_gens dict and names list, both property's.
    Also, there are chromosome property, a reference to the Chromosome it belongs.
    Names must be a list of the req_gens's key"""

    @property
    def req_gens(self): 
        return self.__req_gens

    @req_gens.setter
    def req_gens(self, rg):
        if not rg:
            raise TypeError('RequierGen must have a not empty req_gens')
        if not self.all_subclass(rg.values(), GenBuffer):
            raise TypeError('values in req_gens must extend GenBuffer')
        self.__req_gens = rg

    @property
    def chromosome(self): return self.__chromosome

    @chromosome.setter
    def chromosome(self, i):
        if not i:
            raise TypeError('chromosome in RequierGen must be defined')
        if not issubclass(i.__class__, Chromosome):
            raise TypeError('chromosome in RequierGen must extend Chromosome')
        self.__chromosome = i

    @property
    def names(self):
        if ('_names' not in self.__dict__ or not self._names) and self.req_gens:
            self._names = [name for name in self.req_gens.keys()]
        return self._names

    @names.setter
    def names(self, n):
        self._names = n

    def update_requiered_name(self, new_name, old_name):
        if new_name in self.names:
            if old_name not in self.names:return
            
            raise TypeError('Cannot change '+old_name+' to '+new_name+'; '
                +new_name+' already in req_gens')
        
        self.req_gens[new_name] = self.req_gens.pop(old_name)
        name_index = self.names.index(old_name)
        self.names[name_index] = new_name

class ValuableGen(Gen):
    """Public Class
    Gen that has a value."""    

    def __init__(self, value = None):
        """Public method
        Initiate ValuableGen with value."""
        self.value = value

        @property
        def value(self): return self.__value
        @value.setter
        def value(self, v): self.__value = v

    def __str__(self):
        return str(self.value);

class RunnableGen(Gen, metaclass = ABCMeta):
    """Public Class
    Gen that implements an run method."""

    @abstractmethod
    def run(self, *args, **k_args):
        """Public Method Execute some task, returnnig or not.
        Must be overrided."""
        raise NotImplementedError()

class Chromosome(object, metaclass = ABCMeta):
    """Public Class
    Representation of an possible response."""
    
    def __init__(self, base_gen_dict):
        self.gens = base_gen_dict
        requier_list = [req for req in base_gen_dict.values() if issubclass(req.__class__, RequierGen)]
        while requier_list:
            requier = requier_list.pop(-1)
            requier.chromosome = self
            self.add_gens_from_requier(requier, requier_list.append)            
        self.validate()

    def add_gens_from_requier(self, requier, requier_list_append = None):
        req_dict = requier.req_gens
        for name, buf in req_dict.items():
            new_name = name
            if name in self.gens and issubclass(buf.gen_class, self.gens[name].__class__): 
                continue
            new_name = self.get_new_gen_name(name, buf.gen_class)
            if new_name != name:
                requier.update_requiered_name(new_name, name)
            instance = buf.new_instace()
            if requier_list_append and issubclass(instance.__class__, RequierGen):
                requier_list_append(instance)
            self.gens[new_name] = instance

    def get_new_gen_name(self, name, gen_class):
        new_name = name
        i = 1
        while new_name in self.gens:
            new_name = name+'_'+str(i)
            i = i+1
        return new_name


    def validate(self):
        for gen in [gen for gen in self.gens.values() if issubclass(gen.__class__, ValidatebleGen)]:
            gen.validate()

    def mutate(self):
        for gen in self.gens.values():
            if issubclass(gen.__class__, MutableGen):
                gen.mutate()

    @logger.decorator
    def crossover(self, partner):
        """Public Method
        Return a new instance of the Chromosome class, based on its gens end partner gens."""
        if not issubclass(partner.__class__, Chromosome):
            raise TypeError("partner must be an Chromosome")

        gen_name_list = set([*self.gens.keys(), *partner.gens.keys()])
        gen_dict = {}
        for gen_name in gen_name_list:
            if gen_name not in self.gens:
                gen_dict[gen_name] = partner.gens[gen_name]
            elif gen_name not in partner.gens:
                gen_dict[gen_name] = self.gens[gen_name]
            else:
                gen_dict[gen_name] = choice((self.gens[gen_name], partner.gens[gen_name]))


        new_chr = self.__class__({k : v.new_instace() for k,v in gen_dict.items()})
        new_chr.mutate()
        new_chr.validate()
        return new_chr

    def new_instace(self):
        """Public Method
        Returns a new instance of the object's class."""
        return deepcopy(self)

    @abstractmethod
    def calculate_fitness(self, param):
        """Public Method
        Calculate and return an numerical indicator of Chromosome addaptability.
        Zero is te perfect response, representing that the chromosome is the most optimizated response.
        Must be overrided."""
        NotImplementedError()

class Simulation(object):
    """Public Class
    Simulation of the the population and its processes"""

    def __init__(self, population = None):
        if population:
            self.population = population
        else:
            self.population = []

        self.chr_params = []

    @logger.decorator
    def eliminate(self, list_selector = None, single_selector = None):
        """Public Method
        Sort population using the last value passad to this object's attribute sort_by_fitness.
        If list_selector is received, the new population is the return of it.
        list_selector must be a function that receive the current population as parameter
        Else, if single_selector is received, the new population will be the part of 
        the current that being passed to single_selector makes it return true"""
        self.sort_by_fitness()
        before = len(self.population)
        if (list_selector):
            self.population = list_selector(self.population)
        elif single_selector:
            self.population = [chro for chro in self.population if single_selector(chro)]
        else:
            self.population = self.population[0:int((len(self.population)+1)/2)]

        return before-len(self.population)

    def sort_by_fitness(self, param = None):

        if param and not param in self.chr_params:
            self.chr_params.append(param)

        def key(chro): return chro.calculate_fitness(self.chr_params[-1])

        self.population.sort(key = key)
        return self

class Default(object):
    """Public Static Class.
    Default owns Default Gen, Mutation and Validation implementations."""

    class Mut(Mutation):

        def __init__(self, mutate_method):
            self.mutate_method = mutate_method

        def mutate(self, gen):
            self.mutate_method(gen)

        @classmethod
        def int_list(cls):       
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

            return [cls(add_1),
                    cls(sub_1),
                    cls(mul_1),
                    cls(add_10),
                    cls(sub_10),
                    cls(mul_10),
                    cls(add_100),
                    cls(sub_100),
                    cls(mul_100),
                    cls(mod_1),
                    cls(mod_10),
                    cls(mod_100)]

        @classmethod
        def float_list(cls):
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

            return [*cls.int_list(),
                    cls(div_1),
                    cls(div_10),
                    cls(div_100),
                    cls(add_05),
                    cls(add_01),
                    cls(add_001),
                    cls(sub_05),
                    cls(sub_01),
                    cls(sub_001)]

    class Val(Validation):

        def __init__(self, validate_method):
            self.validate_method = validate_method

        def validate(self, gen):
            self.validate_method(gen)

        @classmethod
        def not_null_list(cls):
            def not_null(gen):
                if gen.value == 0:
                    gen.value = 1 
            return [cls(not_null)]

        @classmethod
        def simplify_frac_list(cls):

            def negative_trate(gen):

                d1 = gen.chromosome.gens[gen.names[0]]
                d2 = gen.chromosome.gens[gen.names[1]]

                if d2.value < 0:
                    d2.value *= -1
                    d1.value *= -1

            def simplify_frac(gen):

                d1 = gen.chromosome.gens[gen.names[0]]
                d2 = gen.chromosome.gens[gen.names[1]]

                for p in range(min(abs(d1.value//2), abs(d2.value//2)), 1, -1):
                    if not (d1.value%p) and not (d2.value%p) and (d1.value) and (d2.value):
                        d1.value /= p
                        d2.value /= p

            def int_treat(gen):

                d1 = gen.chromosome.gens[gen.names[0]]
                d2 = gen.chromosome.gens[gen.names[1]]

                if d1.value and d2.value and not (d1.value%d2.value):
                    d1.value /= d2.value
                    d2.value = 1

                if d2.value and d1.value and not (d2.value%d1.value):
                    d2.value /= d1.value
                    d1.value = 1

                d1.value = int(d1.value)
                d2.value = int(d2.value)

            return [cls(simplify_frac), cls(negative_trate), cls(int_treat)]

    float_mut_list = Mut.float_list()
    int_mut_list = Mut.int_list()

    simplify_frac_val_list = Val.simplify_frac_list()
    not_null_val_list = Val.not_null_list()

    class IntGen(ValuableGen, MutableGen):
        """Public Class
        IntGen represents an integer value."""
        def __init__(self, value = 0):
            self.value = value
            self.mutation_list = Default.int_mut_list

    class FltGen(ValuableGen, MutableGen):
        """Public Class
        FltGen represents an float value."""
        def __init__(self, value = 0):
            self.value = value
            self.mutation_list = Default.float_mut_list

    class FracGen(RequierGen, RunnableGen, ValidatebleGen):
        """Public Class
        FracGen represents an float value get by the division of two integers."""
        def __init__(self):
            names = [str(randint(0,99)) + 'd' + str(x) for x in range(2)]
            down = GenBuffer(gen_class = ValidatebleGen.with_default(Default.IntGen, Default.not_null_val_list))
            up = GenBuffer(gen_class = Default.IntGen)

            self.names = names
            self.req_gens = {names[0]:up, names[1]:down}
            self.validation_list = Default.simplify_frac_val_list

        def run(self):
            up = self.chromosome.gens[self.names[0]].value
            down = self.chromosome.gens[self.names[1]].value
            return up/down

        def __str__(self):
            up = self.chromosome.gens[self.names[0]].value
            down = self.chromosome.gens[self.names[1]].value
            return (str(up) + ('/' + str(down) if (down - 1) else ''))