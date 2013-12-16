#!C:\Program Files\Autodesk\Maya2013\bin\mayapy.exe

import os
import sys
import traceback
import importlib
from notifier import Notifier
from helpers import *

from utils.text_formatter import TextFormatter
from dep_utils.maya_connector import MayaConnector
from dep_utils.yaml_handler import YamlHandler
from dep_utils.dir_handler import DirHandler

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
		task.load_helpers(map(lambda h:helpers_hash[h]().init(self.__n), task.helpers))

        def import_task_module(self, module_name):
           """ Dynamically imports a task module. """
           return importlib.import_module("tasks.%s_task" % (module_name))

	def get_task_from_module(self, obj):
		""" Gets obj class for specified object in Tasks module. If it doesn't exists, None is returned. """
		obj_class = None
		import_module = self.import_task_module(obj)
		for module_class in dir(import_module):
			if TextFormatter.camel_case(obj) + "Task" == module_class:
				obj_class = getattr(import_module, module_class)
		return obj_class
		
	def dispatch(self):
		""" Dispatches the object that handles the action to be executed. """
		task = None
		obj_class = self.get_task_from_module(self.__obj)
		if obj_class is not None:
			task = obj_class()
		else:
			raise ValueError
		self.initialize_task(task)
		task.exec_command(self.__action, self.__params)

class Main(object):
	
	def __init__(self, args):
		self.__args = args
      
        def add_dir_to_import(self, dir_to_import):
               """ Append directory to system path. """
               sys.path.append(os.path.join("~\\Documents\\maya\\2013-x64\\scripts\\sceneTasks\\lib" , dir_to_import))

        def load_app_directories(self):
                """ Loads directories used by the app, such as, utils and tasks. """
                self.add_dir_to_import("tasks")
                self.add_dir_to_import("utils")
                self.add_dir_to_import("config")
                self.add_dir_to_import(".")

	def init(self):
		" Starting point for the execution of the app."
		try:
			self.__n = Notifier()
			self.load_app_directories()
			arg_parser = ArgParser(self.__args, self.__n)
			task_dispatcher = TaskDispatcher(arg_parser.parse(), self.__n)
			task_dispatcher.dispatch()
		except Exception, ex:
			self.__n.error(traceback.format_exc())
		
if __name__ == "__main__":
	Main(sys.argv).init()


