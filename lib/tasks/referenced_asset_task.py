from task_base import TaskBase

class ReferencedAssetTask(TaskBase):
	
	helpers = ["dirs", "maya"]
	
	def __init__(self):
		super(ReferencedAssetTask, self).__init__()
			
	def list(self):
		scene_assets = self.dirs.list_assets("scenes/stock")
		for asset_type in scene_assets.keys():
			for asset in scene_assets[asset_type]:
				asset_path = "stock/" + asset_type + "/" + asset + "/master/" + self.dirs.last_scene(asset, asset_type)
				references = self.maya.list_references(asset_path)
				self._n.success(asset_type + " - " + asset, prefix = False)
				for reference_node in references.keys():
					if references[reference_node][2]:
						self._n.error("    -- Can't load " + reference_node + ", it's broken!", prefix = False)
					else:
						self._n.success("  -- " + references[reference_node][0], prefix = False)
						self._n.success("    |", prefix = False)
						self._n.success("    |---> " + references[reference_node][1], prefix = False)					
					print("\n")
	
	def using(self, asset, type):
		scene_assets = self.dirs.list_assets("scenes/stock")
		for asset_type in scene_assets.keys():
			for asset in scene_assets[asset_type]:
				asset_path = "stock/" + asset_type + "/" + asset + "/master/" + self.dirs.last_scene(asset, asset_type)
				references = self.maya.list_references(asset_path)
				for reference_node  in references.keys():
					print reference_node

