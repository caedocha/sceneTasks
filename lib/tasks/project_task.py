import datetime
from task_base import TaskBase
from models.project import Project
from utils.notifier import Notifier

class ProjectTask(TaskBase):
	
	def __init__(self):
		self._n = Notifier()
		super(ProjectTask, self).__init__()
	
	def info(self):
		try:
			project = Project.get()
			self._n.success("Project created!")
			self._n.success('Name: ' + project.name, prefix = False)
			self._n.success('Created on: ' + project.created_on.strftime('%d-%m-%Y'), prefix = False)
			self._n.success('Existing directories: ', prefix = False)
			self._n.success("-" * 30, prefix = False)
			for existing_dir in project.directories().existing():
				self._n.success('\t - ' + existing_dir, prefix = False)
			if len(project.directories().missing()) > 0:
				self._n.success('\n Missing directories: ', prefix = False)
				self._n.success("-" * 30, prefix = False)
				for missing_dir in project.directories().missing():
					self._n.success('\t - ' + missing_dir, prefix = False)
		except Exception, ex:
			self._n.error("There was a problem fetching the project's info")  

	def create(self, name):
		try:
			project = Project(name, datetime.datetime.now())
			project.create()
			self.info()
		except Exception, ex:
			self._n.error('There was a problem creating the project.')

	def delete(self):
		try:
			project = Project.get()
			project.delete()
			self._n.success("Project deleted!")
		except Exception, ex:
			self._n.error("There was a problem deleting the project.")

