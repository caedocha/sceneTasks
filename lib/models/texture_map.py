import os
import config.settings as settings
import config.paths as paths
import maya.standalone as std
import maya.cmds as cmds
import maya.mel as mel
from utils.maya_connector import MayaConnector
from model_base import ModelBase

class TextureMap(ModelBase):

   def __init__(self, attr, shader, obj, default_dir, asset_path):
      self.attr = attr
      self.shader = shader
      self.obj = obj
      self.default_dir = default_dir
      self.asset_path = asset_path

   def is_missing(self):
      """ Checks if the referenced file of the texture node is missing. """
      pass

   def is_broken(self):
      """ Checks if the map exists but is not connectedto the material for two reasons:
         1. It hasn't been done. 2. Material doesn't exists. """
      pass
   
   def is_broken(self):
      """ Checks if texture map file is not connected to a node or missing. """
      return self.is_missing() or self.is_broken()

   def connect(self):
      """ Connects the texture map file to the texture node if it's not connected. 
      If there's no texture node, it's created too. """
      pass

