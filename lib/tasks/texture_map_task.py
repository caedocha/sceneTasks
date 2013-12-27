from task_base import TaskBase
from models.asset import Asset
from models.texture_map import TextureMap

class TextureMapTask(TaskBase):

	def __init__(self):
		super(TextureMapTask, self).__init__()

	def asset(self, name):
		asset = Asset.find(name = name)[0]
		master_maps = asset.texture_maps('master')
		local_maps = asset.texture_maps('local')
		print len(master_maps)
		for master_map in master_maps:
			print master_map.attr
			print master_map.shader
			print master_map.obj
			print master_map.version
			print master_map.default_dir
			print master_map.asset_path
			print master_map.is_connected()
			print "-" * 20
		for local_map in local_maps:
			print local_map.attr
			print local_map.shader
			print local_map.obj
			print local_map.default_dir
			print local_map.asset_path
			print "-" * 20
