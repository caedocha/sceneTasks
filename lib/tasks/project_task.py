import datetime
from task_base import TaskBase

class ProjectTask(TaskBase):
	
	helpers = ["yaml", "dirs"]
	
	def __init__(self):
		self.__projects_dirs = {"scenes" : 
							{
							"stock": 
								["char", "prop", "scenery", "util"]
							, "work" : None
							} 
					,"source_images" : 
						{
						"textures": 
							{
							"stock" : 
								["char", "prop", "scenery", "util"] 
							}
						, "footage" : None
						} 
					}
		super(ProjectTask, self).__init__()
	
	def which(self):
		config_data = self.yaml.load_config_file()
		project_name = config_data['project']['name']
		self._n.success("Project name: " + project_name, prefix = False)
		
	def created_on(self, format = None):
		config_data = self.yaml.load_config_file()
		created_on_date = config_data['project']['created_on']
		if format is None:
			self._n.success("Created on: " + str(created_on_date.strftime("%d-%m-%Y")), prefix = False)
		else:
			self._n.success("Created on: " + str(created_on_date.strftime(format	)), prefix = False)
		
	
	def create(self, name):
		data = dict(
			project = dict(
				name= name,
				created_on= datetime.datetime.now() 
			)
		)
		self.dirs.create_hash_hierarchy(self.__projects_dirs)
		self.dirs.create_dir_if_doesnt_exists("./config/")
		self.yaml.create_config_file(data, "./config/")
		self._n.success("Project created!")
		
	def delete(self):
		self.dirs.delete_hash_hierarchy(self.__projects_dirs.keys())
		self.yaml.delete_config_file("./config/")
		self._n.success("Project deleted!")

