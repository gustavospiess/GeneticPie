from geneticPie import *
import random
from random import *

'''
A valuableGen that represents an Float number
'''
class FloatGen(ValuableGen):

    #public
    def __init__(self, *param):
        ValuableGen.__init__(self, param[0])
        self.default = self.value

    #public
    def get_req_gens(self):
        return {}

    #public'
    def is_mutable(self, *param):
        return True

    #public
    def mutate(self, *param):
        percent = int(random() * 100)
        mutatio = random() - 0.5
        if percent <= 10:
            self.value = {
                0 : self.default,
                1 : self.value - mutatio,
                2 : self.value + mutatio,
                3 : self.value * mutatio,
                4 : self.value / mutatio,
                5 : int(self.value),
                6 : int(self.value) + 0.5,
                7 : int(self.value) - 0.5,
                8 : int(self.value) + 0.1,
                9 : int(self.value) - 0.1,
                10: int(self.value)
            }[percent]

    #public
    def new_instace(self):
        return self.__class__(self.value)