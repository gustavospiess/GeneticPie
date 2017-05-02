import utils
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
		return ['Genetics', 'population']