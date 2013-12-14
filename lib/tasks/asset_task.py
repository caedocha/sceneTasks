from task_base import TaskBase

class AssetTask(TaskBase):
	
	helpers = ["yaml", "dirs", "maya"]
	
	def __init__(self):
		super(AssetTask, self).__init__()
		
	def create(self, name, type):
		local_dirs = ["master", "local"]
		scenes_path = "scenes/stock/" + type + "/" + name
		source_images_path = "source_images/textures/stock/" + type + "/" + name
		master_asset_file = scenes_path + "/master/" + name + "_init_000.ma"
		local_asset_file = scenes_path + "/local/" + name + "_init_000.ma"
		self.dirs.create_dir_if_doesnt_exists(scenes_path)
		self.dirs.create_dir_if_doesnt_exists(source_images_path)
		[self.dirs.create_dir_if_doesnt_exists(scenes_path + "/" + local_dir) for local_dir in local_dirs]
		[self.dirs.create_dir_if_doesnt_exists(source_images_path + "/" + local_dir) for local_dir in local_dirs]
		self.maya.set_project()
		self.maya.create_scene(master_asset_file)
		self.maya.create_scene(local_asset_file)
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
