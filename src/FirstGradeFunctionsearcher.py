import geneticPie
from geneticPie import *

class FuncFGen(RunnableGen):

    def __init__(self, param):
        if 'req_gens' not in param.keys():
            param['req_gens'] = {'a' : self.get_float_gen, 'b' : self.get_float_gen}
        RunnableGen.__init__(self, param)

    #public
    def run(self, param):
        return self.individual.gens['a'].value * param + self.individual.gens['b'].value

    #private
    def get_float_gen(self):
        return geneticPie.Default.IntGen({})

class FuncFInd(Individual):

    #public
    def __init__(self, gens):
        Individual.__init__(self, {'main': FuncFGen({}), **gens})

    #public
    def calculate_fitness(self, param):
        total = 0
        for sub_param in param:
            parcial = self.gens['main'].run(sub_param[0])
            if parcial < sub_param[1]:
                parcial = sub_param[1] - parcial
            else:
                parcial = parcial - sub_param[1]
            total = total + parcial

        return total

pars = [(1, 12), (2,15)]
sim = Simulation()
sim.population.append(FuncFInd({}))

for i in range(9):
    sim.population.append(sim.population[0].new_instace())

for k in range(5000):
    for individual in sim.population:
        for g in individual.gens.values():
            g.mutate()
    sim.sort_by_fitness(pars)
    for k in range(5):
        sim.population[k+5] = sim.population[k].new_instace()

sim.sort_by_fitness(pars)
for ind in sim.population:
    print((((str(ind.gens['a'].value) if ind.gens['a'].value != 1 else "") + 
        'x') if ind.gens['a'].value else "" ) + 
        ('+' if ind.gens['b'].value > 0 else "") + 
        (str(ind.gens['b'].value) if ind.gens['b'].value else ""))
    print(' ( erro aproximado de', ind.calculate_fitness(pars), ')')