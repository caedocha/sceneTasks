import os
import sys
import traceback
import tasks
from notifier import Notifier
from helpers import *

class ArgParser(object):
	
	def __init__(self, args, notifier):
		self.__args = args
		self.__n = notifier
	
	def parse(self):
		""" Parses the arguments to get the object , action and params to dispatch. """
		self.__args.pop(0)
		obj, action = self.__args.pop(0).split(":")
		params = self.__args
		if (obj == "") or (action == ""):
		 	raise ValueError
		return obj, action, params

class TaskDispatcher(object):
	
	def __init__(self, args, notifier):
		self.__obj = args[0]
		self.__action = args[1]
		self.__params = args[2]
		self.__n = notifier
		
	def initialize_task(self, task):
		""" Initialize any additional configuration the task needs before its executed."""
		helpers_hash = {"maya" : MayaConnector, "yaml" : YamlHandler, "dirs" : DirHandler}
		task.load_helpers(map(lambda h:helpers_hash[h]().init(self.__n), task.required_helpers()))
	
	def dispatch(self):
		""" Dispatchs the object that handles the action to be executed. """
		task = None
		if self.__obj == "project":
			task = tasks.Project(self.__n)
		elif self.__obj == "asset":
			task = tasks.Asset(self.__n)
		else:
			raise ValueError
		self.initialize_task(task)
		task.exec_command(self.__action, self.__params)

class Main(object):
	
	def __init__(self, args):
		self.__args = args
	
	def init(self):
		" Starting point for the execution of the script."
		try:
			self.__n = Notifier()
			arg_parser = ArgParser(self.__args, self.__n)
			task_dispatcher = TaskDispatcher(arg_parser.parse(), self.__n)
			task_dispatcher.dispatch()
		except Exception, ex:
			self.__n.error(traceback.format_exc())
		
if __name__ == "__main__":
	Main(sys.argv).init()


