from utils import Configurable, Printer

class GeneticTypeGroup(Configurable):

	#inherited
	def get_needs(self):
		return ['name', 'desc', 'list']

class GeneticType(Configurable):

	#inherited
	def get_needs(self):
		return ['name', 'others']

class Simulation(Configurable):

	#inherited
	def get_needs(self):
		return ['Genetics', 'population', ]

t = None
t = GeneticTypeGroup({'name' : 'test group', 'desc' : 'test group', 'list' : [{'name' : 'one', 'other' : None}, {'name' : 'two', 'other' : None}]})
#t.save_json('teste.json')


#t = Configurable.get_instace_json('teste.json')

t = t.treat_loadble_value([1, {'a' : [t.to_dictionary()]}, 3])


p = Configurable.get_instace_json('json/PrinterConfig.json')

p.msg(t)

t = Configurable.get_instace_json('teste.json')

p.msg(t)