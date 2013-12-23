import os
import config.settings as settings
import config.paths as paths
import maya.standalone as std
import maya.cmds as cmds
import maya.mel as mel
from utils.maya_connector import MayaConnector
from model_base import ModelBase
from asset import Asset

class Reference(ModelBase):

   def __init__(self, using_asset, referenced_asset, missing = False, broken = False, old_path = ''):
      self.using_asset = using_asset
      self.referenced_asset = referenced_asset 
      self.missing = missing
      self.broken = broken 
      self.old_path = old_path # If reference is broken, this is the path to old reference file.

   def is_broken(self):
      """ Checks if the reference is broken, which means that the referenced_asset is missing. """
      return self.missing or self.broken

   @staticmethod
   def all(default_dir):
      """ Lists all the references in the project. """
      references = []
      assets = Asset.all()
      for asset in assets:
         references.extend(Reference.get_references(asset), default_dir = default_dir)
      return references

   @staticmethod
   def list_broken(default_dir):
      """ Lists all the broken references, which means that the file is missing. """
      return filter(lambda r: r.is_broken(), Reference.all(default_dir))
 
   @staticmethod
   def find_by_using_asset(asset, default_dir):
      """ Find references that are included in the using asset. """
      return filter(lambda r: r.using_asset.name == asset.name, Reference.all(default_dir))

   @staticmethod
   def find_by_referenced_asset(asset, default_dir):
      """ Find references that include the referenced asset. """
      return filter(lambda r: r.referenced_asset.name == asset.name, filter(lambda r: not r.missing, Reference.all(default_dir)))

   @staticmethod
   def get_references(asset, default_dir = "master"):
      """ Fetches the references of a given asset from it's master file. """
      references = []
      if not asset.is_broken():
         if default_dir == "master":
            last_scene = asset.latest_master(full = True).replace("\\", "/")
         else:
            last_scene = asset.latest_local(full = True).replace("\\", "/")
         MayaConnector.set_project()
         cmds.file(last_scene, force = True, open = True)
         for raw_ref in cmds.ls(references = True):
	    reference = None
            broken = True
            try:
               short_name = cmds.referenceQuery(raw_ref, filename = True, shortName = True)
	       path = cmds.referenceQuery(raw_ref, filename = True).replace(os.getcwd().replace("\\", "/"), "")
	       broken = False
	    except:
	       broken = True
            referenced_assets = Asset.find(name = raw_ref.split('_')[0])
            if referenced_assets != []:
               referenced_asset = referenced_assets[0]
               if broken:
                  reference = Reference(asset, referenced_asset, missing = False, broken = True)
               else:
                  reference = Reference(asset, referenced_asset)
            else:
               reference = Reference(asset, None, missing = True, broken = True)
	    references.append(reference)
      return references

