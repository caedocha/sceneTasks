from task_base import TaskBase
from models.reference import Reference
from models.asset import Asset

class ReferencedAssetTask(TaskBase):

	def __init__(self):
		super(ReferencedAssetTask, self).__init__()

	def __format_reference(reference):
		""" Prints the reference with format """
		self._n.success("Using asset: %s:%s" % (reference.using_asset.name, reference.using_asset.type))
		self._n.success("Referenced asset: %s:%s" % (reference.referenced_asset.name, reference.referenced_asset.type))
		self._n.success('-' * 10)

	def list(self):
		try:
			master_references = Reference.all('master')
			local_references = Reference.all('local')
			self._n.success('List of master references:')
			for ref in master_references:
				self.__format_reference(ref)
			self._n.success('\n List of local references:')
			for ref in local_references:
				self.__format_reference(ref)
		except Exception, ex:
			self._n.error('There was a problem listing all the references in the project.')

	def list_using(self, asset):
		try:
			asset = Asset.find(name = asset)
			master_references = Reference.find_by_referenced_asset(asset, 'master')
			local_references = Reference.find_by_referenced_asset(asset, 'local')
			self._n.success('List of master references:')
			for ref in master_references:
				self.__format_reference(ref)
			self._n.success('\n List of local references:')
			for ref in local_references:
				self.__format_reference(ref)
		except Exception, ex:
			self._n.error('There was a problem listing the using references in the project.')

	def list_references(self, asset):
		try:
			asset = Asset.find(name = asset)
			master_references = Reference.find_by_using_asset(asset, 'master')
			local_references = Reference.find_by_using_asset(asset, 'local')
			self._n.success('List of master references:')
			for ref in master_references:
				self.__format_reference(ref)
			self._n.success('\n List of local references:')
			for ref in local_references:
				self.__format_reference(ref)
		except Exception, ex:
			self._n.error('There was a problem listing all the	referenced references in the project.')

	def list_broken(self):
		try:
			master_references = Reference.list_broken('master')
			local_references = Reference.list_broken(asset, 'local')
			self._n.success('List of master references:')
			for ref in master_references:
				self.__format_reference(ref)
			self._n.success('\n List of local references:')
			for ref in local_references:
				self.__format_reference(ref)
		except Exception, ex:
			self._n.error('There was a problem listing all the broken references in the project.')
