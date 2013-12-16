import os
import config.settings as settings
import config.paths as paths
import maya.standalone as std
import maya.cmds as cmds
import maya.mel as mel
from model_base import ModelBase
#from asset import Asset

class ReferencedAsset(ModelBase):

   def __init__(self):
      self.asset = None 
      self.__using_assets = None

   
   def using_assets(self):
      """ Finds all the assets which are using this reference. """      
      if self.__using_assets is None:
         pass
      return self.__using_assets

   @staticmethod
   def all():
      """ Lists all the references in the project. """
      pass

   @staticmethod
   def list_broken():
      """ Lists all the broken references, which means that the file is missing. """
      pass
 
   @staticmethod
   def find(name):
      """ Find references used by a asset with the specified name. """
      pass

