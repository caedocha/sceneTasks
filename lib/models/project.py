import yaml
import os
import shutil
import config.settings as settings
import config.paths as paths
import traceback
from model_base import ModelBase
from asset import Asset

class DefaultDirectory(object):

   def defaults(self):
      """ Returns the project's default file structure in form of a dictionary. """
      return {"scenes": paths.SCENE_HASH, "source_images" : paths.SOURCE_IMG_HASH} 

   def existing(self):
      """ Returns the project's existing default directories. """
      pass

   def missing(self):
      """ Returns the project's missing default directories. """
      pass

   def root(self):
      """ Returns the root path of the project. """
      return os.getcwd()

class Project(ModelBase):

   def __init__(self, name, created_on):
      self.name = name
      self.created_on = created_on 
      self.__directories = None
      self.__assets = None
      self.__references = None
      super(Project, self).__init__()

   def create(self):
      """ Creates a project in a maya directory, includes default directories and yaml configuration files. """
      try:
         default_dirs = self.directories().defaults()
         os.makedirs(os.path.join(self.directories().root(), paths.SCENES_PATH, 'work'))
         os.makedirs(os.path.join(self.directories().root(), paths.SOURCE_IMG_PATH, 'footage'))
         os.makedirs(os.path.join(self.directories().root(), 'config'))
         for asset_dir in default_dirs['scenes']['stock']:
            asset_path = os.path.join(self.directories().root(), paths.SCENES_STOCK, asset_dir)
            os.makedirs(asset_path)
         for asset_dir in default_dirs['source_images']['stock']:
            asset_path = os.path.join(self.directories().root(), paths.SOURCE_IMG_STOCK, asset_dir)
            os.makedirs(asset_path)
         stream = file(os.path.join(self.directories().root(), paths.CONFIG_FILE), 'w')
         yaml.dump(self.to_yaml(), stream, default_flow_style = False)
      except IOError, ex:
         raise
      except yaml.YAMLError, ex:
         raise

   def update(self):
      """ Updates(Overwrites) the entire configuration file with the current object's state. """
      try:
         stream = file(os.path.join(self.directories().root(), paths.CONFIG_FILE), 'w')
         yaml.dump(self.to_yaml(), stream, default_flow_style = False)
      except yaml.YAMLError, ex:
         raise

   def delete(self):
      """ Deletes all files related to the project including default directories, maya scenes and configuration files. """
      try:
         shutil.rmtree(os.path.join(self.directories().root(), 'config'))
         shutil.rmtree(os.path.join(self.directories().root(), paths.SCENES_PATH, 'work'))
         shutil.rmtree(os.path.join(self.directories().root(), paths.SOURCE_IMG_PATH, 'footage'))
         shutil.rmtree(os.path.join(self.directories().root(), paths.SCENES_STOCK))
         shutil.rmtree(os.path.join(self.directories().root(), paths.SOURCE_IMG_STOCK))
      except IOError, ex:
         raise

   @staticmethod
   def get():
      """ Returns an intance of the project. """
      temp_directories = DefaultDirectory()
      if(os.path.exists(os.path.join(temp_directories.root(), paths.CONFIG_FILE))):
         stream = file(os.path.join(temp_directories.root(), paths.CONFIG_FILE), 'r')
         data = yaml.load(stream)
         return Project(data['project']['name'], data['project']['created_on'])
      else:
         return None

   def assets(self):
      """ Returns all the assets in the project. """
      if self.__assets is None:
         self.__assets = Asset.all()
      return self.__assets

   def references(self):
      """ Returns all referenced assets in the project."""
      pass

   def directories(self):
      """ Returns a default directory object which has the project's directory structure information. """
      if self.__directories is None:
         self.__directories = DefaultDirectory()
      return self.__directories

   def to_yaml(self):
      """ Returns the object state in a yaml friendly format. """
      return {'project' : {'name' : self.name, 'created_on' : self.created_on} }