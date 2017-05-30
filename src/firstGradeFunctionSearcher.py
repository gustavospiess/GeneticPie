from defaultGens import *

class FuncFGen(RunnableGen):

    #public
    def run(self, *param):
        return self.individual.gens['a'].value * param[0] + self.individual.gens['b'].value

    #public
    def get_req_gens(self):
        return {'a' : self.get_float_gen, 'b' : self.get_float_gen}

    #private
    def get_float_gen(self):
        return FloatGen(0)

    #public
    def is_mutable(self, *param):
        return False

class FuncFInd(Individual):

    #public
    def __init__(self, gens):
        if gens:
            g = gens
        else:
            g = {}
        g['main'] = FuncFGen(self)
        Individual.__init__(self, g)

    #public
    def calculate_fitness(self, *param):
        total = 0
        for sub_param in param:
            parcial = self.gens['main'].run(sub_param[0])
            if parcial < sub_param[1]:
                parcial = sub_param[1] - parcial
            else:
                parcial = parcial - sub_param[1]
            total = total + parcial

        return total

pars = [(3, 1), (6, 2)]
sim = Simulation()
sim.population.append(FuncFInd(None))

for i in range(9):
    sim.population.append(sim.population[0].new_instace())

for k in range(5000):
    for individual in sim.population:
        for g in individual.gens.values():
            if g.is_mutable():
                g.mutate()
    sim.sort_by_fitness(*pars)
    for k in range(5):
        sim.population[k+5] = sim.population[k].new_instace()

for ind in sim.population:
    print ind.calculate_fitness(*pars), 'a = ', ind.gens['a'].value, 'b = ', ind.gens['b'].value