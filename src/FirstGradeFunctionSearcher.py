import geneticPie
from geneticPie import *

class FuncFGen(RunnableGen):

    def __init__(self):
        buff = GenBuffer(new_instace = self.get_gen, gen_class = geneticPie.Default.FracGen.__class__)
        RunnableGen.__init__(self, req_gens = {'a' : buff, 'b' : buff})

    def run(self, param):
        return self.individual.gens[self.names[0]].run(None) * param + self.individual.gens[self.names[1]].run(None)

    def get_gen(self):
        return geneticPie.Default.FracGen({})   

class FuncFInd(Individual):

    def __init__(self, gens):
        buf = GenBuffer(new_instace = FuncFGen, gen_class = FuncFGen.__class__)
        Individual.__init__(self, {'main': buf, **gens})

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
sim.population.append(FuncFInd({}))

for i in range(19):
    sim.population.append(sim.population[0].new_instace())

print(sim.population[0].gens)

for k in range(20):
    sim.sort_by_fitness(pars)
    if not sim.population[0].calculate_fitness(pars):
        print(k)
        break
    for k in range(sim.eliminate()):
        pair = random.sample(sim.population, 2)
        sim.population.append(pair[0].crossover(pair[1]))


print(pars)
print()
sim.sort_by_fitness(pars)
for ind in sim.population:
    print(str(ind.gens['a']) +'x+'  + str(ind.gens['b']))
    if (ind.calculate_fitness(pars)):
        print(' ( erro aproximado de', ind.calculate_fitness(pars), ')')
