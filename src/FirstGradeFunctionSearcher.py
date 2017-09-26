from geneticPie import *
import random

class FuncFGen(RunnableGen, RequierGen):

    def __init__(self):
        buff = GenBuffer(gen_class = Default.FracGen)
        self.req_gens = {'a' : buff, 'b' : buff}

    def run(self, param):        
        a = self.individual.gens[self.names[0]].run()
        b = self.individual.gens[self.names[1]].run()
        return a * param + b

    def get_gen(self):
        return   

class FuncFInd(Individual):

    def __init__(self, gens = None):
        a = gens if gens else {'main': FuncFGen()}
        Individual.__init__(self, a)

    def calculate_fitness(self, param):
        total = 0
        for sub_param in param:
            parcial = self.gens['main'].run(sub_param[0])
            if parcial != param[1]:
                if parcial < sub_param[1]:
                    parcial = sub_param[1] - parcial
                else:
                    parcial = parcial - sub_param[1]
            total = total + parcial

        return total

def rint():
    return random.randint(-20, 20)
def rpoint():
    return(rint(), rint())
pars = [rpoint(), rpoint()]
sim = Simulation()
sim.population.append(FuncFInd())

for i in range(19):
    sim.population.append(sim.population[0].new_instace())

for k in range(250):
    sim.sort_by_fitness(pars)
    if not sim.population[0].calculate_fitness(pars):
        break
    for k in range(sim.eliminate()):
        pair = random.sample(sim.population, 2)
        sim.population.append(pair[0].crossover(pair[1]))


print(pars)
print()
sim.sort_by_fitness(pars)
for ind in sim.population:
    a = ind.gens['main'].names[0]
    b = ind.gens['main'].names[1]
    print(str(ind.gens[a]) +'x+'  + str(ind.gens[b]))
    if (ind.calculate_fitness(pars)):
        print(' ( erro aproximado de', ind.calculate_fitness(pars), ')')

print(logger.logs)