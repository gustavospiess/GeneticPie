import utils
from utils import *

class Gen(Configurable):

    #inherited
    def get_req_configs(self):
        return {
        'req_gen' : {
            'default' : {},
            'desc' : 'A dict of names and required genetic types'
            }
        }

    #public
    def is_mutable(*param):
        raise Exception('not implemented')

    #public
    def mutate(*param):
        raise Exception('not implemented')

    #public
    def is_crossoverble(*param):
        raise Exception('not implemented')        

    #public
    def crossover(*param):
        raise Exception('not implemented')

class Individual(Configurable):

    def __init__(self, config = {}):
        super(Individual, self).__init__(config)
        map (lambda c : config.pop(c), self.keys())
        self.update(config)
        for g in self['gens']:
            if g in self.keys():
                for r in self[g]['req_gen'].keys():
                    self[r] = self[g]['req_gen'][r]


    #inherited
    def get_req_configs(self):
        return {
            'gens' : {
                'default' : [], 
                'desc' : 'A list of what other configs are gens'
            }
        }


class Simulation(Descriptble):

    #inherited
    def get_req_configs(self):
        req = super(Simulation, self).get_req_configs()
        req.update({
            'pool' : {
                'default' : [],
                'desc' : ''
            },
            'popu' : {
                'default' : [],
                'desc' : 'list of'
            }
        })
        return req