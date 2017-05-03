import utils
from utils import Configurable, Printer

class GeneticTypeGroup(Configurable):

	#inherited
	def get_configs(self):
		return {'name' : {'default' : ''},
				'desc' : {'default' : ''},
				'list' : {'default' : []}}

class GeneticType(Configurable):

	#inherited
	def get_configs(self):
		return {'name' : {'default' : ''},
				'desc' : {'default' : ''},
				'gens_down' : {'default' : []},
				'gens_up' : {'default' : []}}

class GeneticType(Configurable):

	#inherited
	def get_configs(self):
		return {'name' : {'default' : ''},
				'desc' : {'default' : ''},
				'gens_down' : {'default' : []},
				'gens_up' : {'default' : []}}

class Individual(Configurable):

	#inherited
	def get_configs(self):
		return {'Gens' : {}}


class Simulation(Configurable):

	#inherited
	def get_configs(self):
		return {'name' : {'default' : ''},
				'desc' : {'default' : ''},
				'pool' : {'default' : []},
				'popu' : {'default' : []}}

a = 