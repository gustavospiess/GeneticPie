import sys
import json
import os

#Extender may implement [get_condigs];
class Configurable(object):
	TYPES = [dict, list, tuple, str, unicode, int, long, float, type(True), type(None)]

	def __init__(self, config):

		#protected
		self.config = {}
		self.load(config)

	#public	
	@staticmethod
	def get_instance(config):
		module = __import__(config['init']['mod'])
		class_ = getattr(module, config['init']['class'])
		return class_(config['param'])

	#public
	@staticmethod
	def get_instace_json(src):
		return Configurable.get_instance(json.loads(open(os.path.relpath(src), 'r').read()))

	#public
	def load(self, config):
		for key in self.get_condigs().keys():
			if key in config and type(config[key]) != type(None):
				value = config[key]
				self.config[key] = self.treat_loadble_value(value)
			else:
				if self.get_condigs()[key] and 'default' in self.get_condigs()[key]:
					self.config[key] = self.get_condigs()[key]['default']
				else:
					p.log('key not found: ' + key + '. And there is not default value')


	#public
	def to_dictionary(self):
		param = {}
		for key, value in self.config.items():
			if not ('default' in self.get_condigs()[key] and self.get_condigs()[key]['default'] == value) :
				if self.is_json_type(value):
					if (self.is_list(value)):
						param[key] = []
						for element in value:
							if element in Configurable.__subclasses__():
								param[key].append(element.to_dictionary())
							else:
								if self.is_json_type(element):
									param[key].append(element)
					else:
						param[key] = value
				else:
					if type(value) in Configurable.__subclasses__():
						param[key] = value.to_dictionary()

		mod = self.__module__
		if mod == '__main__':
			filename = sys.modules[self.__module__].__file__
			mod = os.path.splitext(os.path.basename(filename))[0]

		init = {'mod' : mod, 'class' : self.__class__.__name__}
		dic = {'init' : init, 'param' : param}
		return dic

	#private
	def treat_loadble_value(self, value):

		if (self.is_instaciable_dictionary(value)):
			p.log(Configurable.get_instance(value))
			return Configurable.get_instance(value)
		if self.is_list(value):
			value_list = []
			for element in value:
				value_list.append(self.treat_loadble_value(element))
			p.log(value_list)
			return value_list
		if self.is_dict(value):
			value_dict = {}
			for key, element in value.items():
				value_dict[key] =  self.treat_loadble_value(element)
			p.log(value_dict)
			return value_dict
		return value

	#private
	def is_dict(self, var):
		return type(var) == dict

	#private
	def is_instaciable_dictionary(self, var):
		return self.is_dict(var) and 'init' in var.keys() and var['init']

	#private
	def is_list(self, var):
		return type(var) in [list, tuple]

	#private
	def is_json_type(self, var):
		return type(var) in self.TYPES

	#public
	def save_json(self, src):
		open(os.path.relpath(src), 'w').write(json.dumps(self.to_dictionary(), sort_keys = True))
		return self
		
	#public
	"""
	Unimplemented, may return an dictionary of keys/names for the required configurations and its details.
	The details can, but not obligatory will, include.
	 _______________________________________________________________
	|Detail		|	Description										|
	|___________|___________________________________________________|
	|default	|	Value to be considered when null				|
	|desc		|	Description to be printed when find an error	|
	|___________|___________________________________________________|
	"""
	def get_condigs(self):
		raise Exception('not implemented')

class Printer(Configurable):
	#public
	def msg(self, msg):
		if(self.config['msg']):
			print'Mensagem: ', msg

	#public
	def log(self, log):
		if(self.config['log']):
			print 'Log: ', log

	#inherited
	def get_condigs(self):
		return {'msg' : {
						'default' : 1, 
						'desc' : 'Boolean value that alows or not to print messages'
						},
				'log' : {
						'default' : 1,
						'desc' : 'Boolean value thar alows or not to print logs'
						}
				}

p = Configurable.get_instace_json('json/PrinterConfig.json')
