import os
import shutil
import traceback
import maya.standalone as std
import maya.cmds as cmds
import maya.mel as mel
import config.settings as settings
import config.paths as paths
from model_base import ModelBase
from texture_map import TextureMap
from utils.maya_connector import MayaConnector

class DefaultDirectory(object):

   def __init__(self, path, asset):
      self.__asset = asset
      self.__path = path

   def path(self):
      return os.path.join(os.getcwd(), self.__path, self.__asset.type, self.__asset.name)

   def defaults(self):
      """ Returns a list of the asset's default paths. """
      master_path = os.path.join(os.getcwd(), self.__path, self.__asset.type, self.__asset.name, 'master')
      local_path = os.path.join(os.getcwd(), self.__path, self.__asset.type, self.__asset.name, 'local')
      return [master_path, local_path]

   def is_missing_any(self):
      """ Checks if any of the default directories are missing. """
      return self.which_missing() != [] 

   def which_missing(self):
      """ Returns a list of the missing default directories. """
      missing = []
      if not os.path.isdir(self.master()):
         missing.append('master')
      if not os.path.isdir(self.local()):
         missing.append('local')
      return missing

   def is_empty_any(self):
      """ Checks if any of the default directories are empty."""
      return self.which_empty() != []
      
   def which_empty(self):
      """ Returns a list of the empty default directories. """
      empty = []
      if not 'master' in self.which_missing():
         if os.listdir(self.master()) == []:
            empty.append('master')
      if not 'local' in self.which_missing():
         if os.listdir(self.local()) == []:
            empty.append('local')
      return empty

   def master(self):
      """ Shortcut to return only the master directory path. """
      return self.defaults()[0]
   
   def local(self):
      """ Shotcut to return only the local directory path. """
      return self.defaults()[1]
   
   def refresh(self, asset):
      """ Refreshes the asset instance, in case it has change. """
      self.__asset = asset

class Asset(ModelBase):

   def __init__(self, name, type):
      self.name = name
      self.type = type
      self.__source_images = None
      self.__scenes = None
      super(Asset, self).__init__()

   def create(self):
      """ Creates an asset in a maya directory, which includes default directories and maya scenes. """
      try:
         os.makedirs(self.scenes().master())
         os.makedirs(self.scenes().local())
         os.makedirs(self.source_images().master())
         os.makedirs(self.source_images().local())
         MayaConnector.set_project()
         master_file = os.path.join(self.scenes().master(), settings.SCENE_FILE % (self.name.lower(), '000', 'init')).replace('\\', '/')
         local_file = os.path.join(self.scenes().local(), settings.SCENE_FILE % (self.name.lower(), '000', 'init')).replace('\\', '/')
         cmds.file(new = True)
         cmds.file(rename = master_file)
         cmds.file(save = True)
         cmds.file(new = True)
         cmds.file(rename = local_file)
         cmds.file(save = True)
      except IOError, ex:
         raise

   def update(self, name = None, type = None):
      """ Updates the name of the asset, this includes the directory and maya scene file. Also, if the type is updated, it's moved to the new type's directory. """
      if name is not None:
         for msd in os.listdir(self.scenes().master()):
            if msd.split("_")[0] == self.name:
               shutil.move(os.path.join(self.scenes().master(), msd), os.path.join(self.scenes().master(), msd.replace(self.name, name)))
         for lsd in os.listdir(self.scenes().local()):
            if lsd.split("_")[0] == self.name:
               shutil.move(os.path.join(self.scenes().local(), lsd), os.path.join(self.scenes().local(), lsd.replace(self.name, name)))
         shutil.move(self.scenes().path(), self.scenes().path().replace(self.name, name))
         shutil.move(self.source_images().path(), self.source_images().path().replace(self.name, name))
         self.name = name
      if type is not None:
         shutil.move(self.scenes().path(), self.scenes().path().replace(self.type, type))         
         shutil.move(self.source_images().path(), self.source_images().path().replace(self.type, type))         
         self.type = type
      self.scenes().refresh(self)
      self.source_images().refresh(self)

   def delete(self):
      """ Deletes all the directory related to the asset. """
      shutil.rmtree(self.scenes().path())
      shutil.rmtree(self.source_images().path())

   def is_broken(self):
      """ Checks if the asset is broken: has any missing or empty default directory. """
      return self.scenes().is_missing_any() or self.scenes().is_empty_any() or self.source_images().is_missing_any()
   
   def latest_local(self, full = False):
      """ Get the latest file path of local directory. If full = True, returns absolute path. """ 
      try:
         if full:
            return os.path.join(self.scenes().local(), os.listdir(self.scenes().local())[-1])
         else:
            return os.listdir(self.local())[-1]
      except Exception, ex:
         return []

   def latest_master(self, full = False):
      """ Get the latest file path of master directory. If full = True, returns absolute path. """ 
      try:
         if full:
            return os.path.join(self.scenes().master(), os.listdir(self.scenes().master())[-1])
         else:
            return os.listdir(self.scenes().master())[-1]
      except Exception, ex:
         return []

   @staticmethod
   def all():
      """ Returns all the project's assets. """
      assets = []
      asset_dir = os.path.join(os.getcwd(), paths.SCENES_STOCK)
      for asset_type in os.listdir(asset_dir):
         for asset in os.listdir(os.path.join(asset_dir, asset_type)):
            assets.append(Asset(asset, asset_type))
      return assets
   
   @staticmethod
   def find(type = None, name = None):
      """ Finds assets by name or type. Name has priority over type if both parameters are given. """
      assets = [] 
      all_assets = Asset.all()
      if type is not None:
         assets = filter(lambda a: a.type == type, all_assets)
      if name is not None:
         assets = filter(lambda a: a.name == name, all_assets)
      return assets

   @staticmethod
   def list_broken():
      """ Finds all broken assets. """
      return filter(lambda a: a.is_broken(), Asset.all()) 

   def references(self):
      """ Lists the references used by the asset. """
      pass

   def source_images(self):
      """ Returns a default directory object which has all the information regarding source_images paths. """
      if self.__source_images is None:
         self.__source_images = DefaultDirectory(paths.SOURCE_IMG_STOCK, self)
      return self.__source_images

   def scenes(self):
      """ Returns a default directory object which has all the information regarding scenes paths. """
      if self.__scenes is None:
         self.__scenes = DefaultDirectory(paths.SCENES_STOCK, self)
      return self.__scenes

   def texture_maps(self, default_dir):
      pass


