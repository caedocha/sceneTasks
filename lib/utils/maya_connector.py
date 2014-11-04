import sys
import os
import maya.standalone as std
import maya.cmds as cmds
import maya.mel as mel

class MayaConnector(object):

	 @staticmethod
	 def initialize_maya():
			std.initialize(name = 'name')

	 @staticmethod
	 def set_project():
			MayaConnector.initialize_maya()
			mel.eval('setProject "%s";' % (os.getcwd().replace('\\', '/')))
