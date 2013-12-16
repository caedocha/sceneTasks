import traceback
import yaml
import os
import shutil
from notifier import Notifier

class YamlHandler(object):
	
	def init(self, notifier):
		self.n = notifier
		self.__config_file = "config.yml"
		return self
	
	def create_config_file(self, data, path):
		"Creates project's configuration file inside config directory"
		try:
			if os.path.exists(os.path.join(path, self.__config_file)):
				self.n.neutral("Config file already exists in " + path)
			else:
				stream = file(os.path.join(path, self.__config_file), 'w')
				yaml.dump(data, stream, default_flow_style = False)
				self.n.success("Created config file in " + path)
		except yaml.YAMLError, ex:
			self.n.error(traceback.format_exc())
			
	def delete_config_file(self, path):
		"Deletes project's configuration file."
		try:
			if not os.path.exists(os.path.join(path, self.__config_file)):
				self.n.neutral("Config file doesn't exists.")
			else:
				shutil.rmtree(path)
		except IOError , ex:
			self.n.error(traceback.format_exc())
	
	def load_config_file(self):
		""" Sets the working project, all other tasks are executed based on it. """
		try:
			config_path = os.path.join(os.getcwd(), "config", self.__config_file)
			if not os.path.exists(config_path):
				self.n.error("Config file doesn't exists.")
				return []
			else:
				
				stream = file(config_path, 'r')
				return yaml.load(stream)
		except IOError, ex:
			self.n.error(traceback.format_exc())
