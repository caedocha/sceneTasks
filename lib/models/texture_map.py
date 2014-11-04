import os
import config.settings as settings
import config.paths as paths
import maya.standalone as std
import maya.cmds as cmds
import maya.mel as mel
from utils.maya_connector import MayaConnector
from utils.list_utils import ListUtils
from model_base import ModelBase

class TextureMap(ModelBase):

	def __init__(self, attr, shader, obj, version, default_dir, asset_path):
		self.attr = attr
		self.shader = shader
		self.obj = obj
		self.version = version
		self.default_dir = default_dir
		self.asset_path = asset_path

	def is_missing(self):
		""" Checks if the referenced file of the texture node is missing. """
		pass

	def is_connected(self):
		""" Checks if the map exists but is not connectedto the material for two reasons:
			 1. It hasn't been done. 2. Material doesn't exists. """
		is_connected = False
		MayaConnector.set_project()
		cmds.file(self.asset_path, open = True)
		if self.__is_valid_shader():
			node = str(cmds.listConnections('%s.%s' % (self.shader, self.attr))[0])
			if self.__is_valid_file(node):
				return True
			else:
				is_connected = False
			if self.__is_valid_gamma(node):
				value_node = str(cmds.listConnections('%s.%s' % (node, 'value'))[0])
				if self.__is_valid_file(node):
					return True
				else:
					is_connected = False
			else:
				is_connected = False
		else:
			is_connected = False
		
		return is_connected

	def is_broken(self):
		""" Checks if texture map file is not connected to a node or missing. """
		return self.is_missing() or self.is_not_connected()

	def connect(self):
		""" Connects the texture map file to the texture node if it's not connected.
		If there's no texture node, it's created too. """
		pass

	def __is_valid_shader(self):
		try:
			cmds.select(self.shader)
			cmds.select(cmds.listConnections('%s.%s' % (self.shader, self.attr))[0])
			return True
		except:
			return False

	def __is_valid_gamma(self, node):
		try:
			if cmds.nodeType(node) == 'gammaCorrect':
				value_node = cmds.listConnections('%s.%s' % (node, 'value'))[0]
				cmds.select(value_node)
				return True
			else:
				return False
		except:
			return False

	def __is_valid_file(self, node):
		try:
			if cmds.nodeType(node) == 'file':
				if cmds.getAttr('%s.fileTextureName' % (node)) != '' :
					return True
				else:
					return False
			else:
				return False
		except:
			return False
