import traceback
from task_base import TaskBase
from models.asset import Asset

class AssetTask(TaskBase):

	def __init__(self):
		super(AssetTask, self).__init__()

	def create(self, name, type):
		try:
			asset = Asset(name, type)
			asset.create()
			self._n.success(asset.type.capitalize() + " " + asset.name + " created!")
		except Exception, ex:
			self._n.error("There was a problem creating the asset.")

	def update(self, old_name, new_name, type=None):
		try:
			if new_name == '':
				new_name = None
			if type == '':
				type = None
			asset = Asset.find(name = old_name)[0]
			asset.update(new_name, type)
			self._n.success('Asset updated.')
		except Exception, ex:
			self._n.error('There was a problem updating the asset.')
			self._n.error(traceback.format_exc())

	def delete(self, name, type):
		try:
			asset = Asset.find(name = name)[0]
			asset.delete()
			self._n.success("Asset deleted.")
		except Exception, ex:
			self._n.error('There was a problem deleting the asset.')
			self._n.error(traceback.format_exc())

	def list(self, type = None):
		try:
			if type is None:
				assets = Asset.all()
			else:
				assets = Asset.find(type = type)
			self._n.success("Asset list: ", prefix = False)
			self._n.success('-' * 30, prefix = False)
			for asset in assets:
				self._n.success('  Name: ' + asset.name, prefix = False)
				self._n.success('  Type: ' + asset.type, prefix = False)
				self._n.success(' -' * 10, prefix = False)
		except Exception, ex:
			self._n.error('There was a problem listing all assets.')

	def broken(self):
		try:
			assets = Asset.list_broken()
			self._n.success("Asset list: ")
			self._n.success('-' * 30)
			for asset in assets:
				self._n.success('Name: ' + asset.name)
				self._n.success('Type: ' + asset.type)
				self._n.success('-' * 10)
		except Exception, ex:
			self._n.error('There was a problem listing all broken assets.')
