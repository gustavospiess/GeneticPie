import geneticPie
from geneticPie import *

class FuncFGen(RunnableGen):

    def __init__(self, param):
        if 'req_gens' not in param.keys():
            param['req_gens'] = {'a' : self.get_gen, 'b' : self.get_gen}
        RunnableGen.__init__(self, param)

    #public
    def run(self, param):
        return self.individual.gens['a'].run(None) * param + self.individual.gens['b'].run(None)

    #private
    def get_gen(self):
        return geneticPie.Default.FracGen({})   

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

pars = [(5, -5), (15,-15)]
sim = Simulation()
sim.population.append(FuncFInd({}))

for i in range(9):
    sim.population.append(sim.population[0].new_instace())

for k in range(2000):
    sim.sort_by_fitness(pars)
    if not sim.population[0].calculate_fitness(pars):
        break
    for k in range(5):
        sim.population[k+5] = sim.population[k].crossover(sim.population[k+1])

sim.sort_by_fitness(pars)
for ind in sim.population:
    print((((str(ind.gens['a'])) + 
        'x')) + 
        ('+' ) + 
        (str(ind.gens['b']) ))
    if (ind.calculate_fitness(pars)):
        print(' ( erro aproximado de', ind.calculate_fitness(pars), ')')