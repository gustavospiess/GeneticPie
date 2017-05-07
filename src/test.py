import geneticPie
from geneticPie import *
import random
from random import *

class FloatGen(Gen):

    #public
    def get_needed_gens(self):
        return {}

    #public
    def is_mutable(self, *param):
        return True

    #public
    def mutate(self, *param):
        op = random() * 1000
        if (op < 70):
            self['value'] = self['value'] + (random() - 0.5)
        if (op >= 60 and op < 100):
            self['value'] = self['value'] * (random() - 0.5)
        if (op >= 100 and op < 102):
            self['value'] = self.get_req_configs['value']['default']

    #public
    def is_crossoverble(self, *param):
        return False      

    #public
    def crossover(self, *param):
        raise Exception('not implemented')


class FuncCalcGen(Gen):

    #inherited
    def get_req_configs(self):
        req = super(FuncCalcGen, self).get_req_configs()
        req.update({
            'run' : {
                'default' : (lambda self, x : self['a']['value']*x + self['b']['value'])
            },
            'req_gen' : {
                'default' : {'a' : FloatGen, 'b' : FloatGen}
            }
        })
        return req

    #public
    def is_crossoverble(self, *param):
        return False      

    #public
    def crossover(self, *param):
        raise Exception('not implemented')