import os

#Default scene path.
SCENES_PATH = 'scenes'
SCENES_STOCK = os.path.join(SCENES_PATH, 'stock') 
#Default source_images path.
SOURCE_IMG_PATH = 'source_images'
SOURCE_IMG_STOCK = os.path.join(SOURCE_IMG_PATH, 'stock')
#Default asset directories.
ASSET_DIRS = ['master', 'local']
#Default config file path
CONFIG_FILE = os.path.join('config', 'config.yml')
#Default project's scene directory structure.
SCENE_HASH = {
      "stock" : ["char", "prop", "scenery", "util"],
      "work" : None
      }
#Default project's source_images directory structure.
SOURCE_IMG_HASH = {
      "stock" : ["char", "prop", "scenery", "util"],
      "footage" : None
      }
