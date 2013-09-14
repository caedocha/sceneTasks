import traceback
import datetime
from notifier import Notifier

class Task(object):
	
	handlers = []
	
	def __init__(self, notifier):
		self._n = notifier
		
	def exec_command(self, command, params):
		try:
			getattr(self, command)(*params)
		except Exception, ex:
			self._n.error(traceback.format_exc())
			
	def load_helpers(self, helpers_obj):
		for helper, obj in zip(self.helpers, helpers_obj):
			setattr(self, helper, obj)
		
	def required_helpers(self):
		return self.helpers

class Project(Task):
	
	helpers = ["yaml", "dirs"]
	
	def __init__(self, notifier):
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
		super(Project, self).__init__(notifier)
	
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
		
class Asset(Task):
	
	helpers = ["yaml", "dirs"]
	
	def __init__(self, notifier):
		super(Asset, self).__init__(notifier)
		
	def create(self, name, type):
		local_dirs = ["master", "local"]
		scenes_path = "./scenes/stock/" + type + "/" + name
		source_images_path = "./source_images/textures/stock/" + type + "/" + name
		self.dirs.create_dir_if_doesnt_exists(scenes_path)
		self.dirs.create_dir_if_doesnt_exists(source_images_path)
		[self.dirs.create_dir_if_doesnt_exists(scenes_path + "/" + local_dir) for local_dir in local_dirs]
		[self.dirs.create_dir_if_doesnt_exists(source_images_path + "/" + local_dir) for local_dir in local_dirs]
		self._n.success(type.capitalize() + " " + name + " created!")
		
	def rename(self, old_name, new_name, type):
		old_scenes_path = "./scenes/stock/" + type + "/" + old_name
		new_scenes_path = "./scenes/stock/" + type + "/" + new_name
		old_source_images_path = "./source_images/textures/stock/" + type + "/" + old_name
		new_source_images_path = "./source_images/textures/stock/" + type + "/" + new_name
		self.dirs.rename_dir(old_scenes_path, new_scenes_path)
		self.dirs.rename_dir(old_source_images_path, new_source_images_path)
	
	def delete(self, name, type):
		scenes_path = "./scenes/stock/" + type + "/" + name
		source_images_path = "./source_images/textures/stock/" + type + "/" + name
		if self.dirs.delete_dir_if_exists(scenes_path):
			self._n.success(type.capitalize() + " " + name + "'s scenes dir was deleted!")
		else:
			self._n.neutral("Could not delete " + type.capitalize() + " " + name + "'s scenes dir.")
		if self.dirs.delete_dir_if_exists(source_images_path):
			self._n.success(type.capitalize() + " " + name + "'s source_images dir was deleted!")
		else:
			self._n.neutral("Could not delete " + type.capitalize() + " " + name + "'s source_images dir.")
			
	def list(self, type = None):
		if type is None:
			scene_assets = self.dirs.list_assets("scenes/stock")
			source_images_assets = self.dirs.list_assets("source_images/textures/stock")
		else:
			scene_assets = self.dirs.list_assets("scenes/stock/" + type)
			source_images_assets = self.dirs.list_assets("source_images/textures/stock/" + type)
		if len(scene_assets) != len(source_images_assets):
			self._n.error("There are broken assets. Run 'main.py asset:broken' ")
		else:
			total_assets = 0
			for asset_type in scene_assets.keys():
				for asset in scene_assets[asset_type]:
					total_assets = total_assets + 1 
			self._n.success("Total number of assets: " + str(total_assets), prefix = False)
			self._n.success("-" * 30, prefix = False)
			for asset_type in scene_assets.keys():
				self._n.success(asset_type.capitalize(), prefix = False)
				self._n.success("-" * 30, prefix = False)
				for asset in scene_assets[asset_type]:
					self._n.success("- " + asset, prefix = False)
				self._n.success(" ", prefix = False)
			
	def broken(self):
		self._n.success("Broken assets:", prefix = False)
		self._n.success("-" * 30, prefix = False)
		comparison_results = self.dirs.compare_dirs('./scenes/stock/', './source_images/textures/stock/')
		for comparisons in comparison_results:
			for results in comparisons:
				if results[0] == 0:
					self._n.error("- Missing in " + results[1], prefix = False)
				else:
					self._n.success("+ File existing in " + results[1], prefix = False)
			print("\n")
			
			
