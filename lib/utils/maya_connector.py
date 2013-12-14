import maya.standalone as std
import maya.cmds as cmds
import maya.mel as mel
import os

class MayaConnector(object):
   
	def __init__(self):
	   pass
		
        
        def init(self, notifier):
           std.initialize(name='python')
           self.n = notifier
           return self

	def set_project(self):
		current_directory = os.getcwd().replace("\\", "/")
		mel.eval('setProject "' + current_directory + '";')	
	
	def create_scene(self, scene):
		cmds.file(new = True)
		cmds.file(rename = scene.replace("\\", "/"))
		cmds.file(save = True)
		
	def list_references(self, scene):
		references = {}
		self.set_project()
		cmds.file(scene, force = True, open = True)
		raw_references = cmds.ls(references = True)
		for ref in raw_references:
			short_name = ""
			path = ""
			try:
				short_name = cmds.referenceQuery(ref, filename = True, shortName = True)
				path = cmds.referenceQuery(ref, filename = True).replace(os.getcwd().replace("\\", "/"), "")
				broken = False
			except:
				broken = True
			references[ref] = [short_name, path, broken]
		return references
		

