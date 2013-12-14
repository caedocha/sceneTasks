import traceback
from notifier import Notifier
from scene_base import SceneBase

class TaskBase(SceneBase):
         
        helpers = []
	
	def __init__(self):
		self._n = Notifier()
		super(TaskBase, self).__init__()
		
	def exec_command(self, command, params):
		try:
			getattr(self, command)(*params)
		except Exception, ex:
			self._n.error(traceback.format_exc())
			
	def load_helpers(self, helpers_obj):
		for helper, obj in zip(self.helpers, helpers_obj):
		   setattr(self, helper, obj)
		
	def helpers(self):
		return self.helpers
