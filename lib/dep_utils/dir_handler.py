import os
import sys
import traceback
import filecmp
import shutil

class DirHandler(object):
	
	def init(self, notifier):
	   self.n = notifier
	   return self

	def create_dir_if_doesnt_exists(self, directory):
		""" Creates a directory if it doesn't exists already. """
		result = True
		scene_dir_exists = lambda x : True if (os.path.exists(x)) else False
		if not scene_dir_exists(directory):
			os.makedirs(directory)
			result = True
		else:
			result = False
		return result	
	
	def create_hash_hierarchy(self, directories):
		""" Creates a directory hierarchy based on a hash that represents it. """
		roots = directories.keys()
		for root in roots:
			self.__create_hash_hierarchy_recur(None, root, directories[root])
	
	def __create_hash_hierarchy_recur(self, parent, directory, children):
		""" Recursive counterpart of create_hash_hierarchy method. """
		try:
			if self.create_dir_if_doesnt_exists(directory):
				self.n.success("Directory created: " + directory)
			else:
				self.n.neutral("Couldn't create directory: " + directory)
			if isinstance(children, dict):
				for child in children.keys():
					os.chdir(directory)
					self.__create_hash_hierarchy_recur(directory, child, children[child])
					os.chdir("..")
			elif isinstance(children, list):
				for child in children:
					if self.create_dir_if_doesnt_exists(directory + "/" + child):
						self.n.success("Directory created: " + child)
					else:
						self.n.neutral("Couldn't create directory: " + child)
		except OSError:
			self.n.error(traceback.format_exc())
		
	def delete_hash_hierarchy(self, roots):
		"Deletes all content inside root directories."
		try:
			for root in roots:
				directory = "./" + root
				if os.path.exists(directory):
					shutil.rmtree(directory)
		except OSError:
			self.n.error(traceback.format_exc())	
	
	def delete_dir_if_exists(self, directory):
		"""Deletes a directory if it exists"""
		result = True
		dir_exists = lambda x : True if (os.path.exists(x)) else False
		if dir_exists(directory):
			shutil.rmtree(directory)
			result = True
		else:
			result = False
		return result

	def rename_dir(self, old_directory, new_directory):
		try:
			shutil.move(old_directory, new_directory)
		except OSError, ex:
			self.n.error(traceback.format_exc())
		
	def list_assets(self, path):
		assets = {}
		for root, dirs, files in os.walk(path):
			if("master" in dirs) and ("local" in dirs):
				splitted_root = root.split(os.sep)
				asset_name = splitted_root.pop()
				asset_type = splitted_root.pop()
				if not asset_type in assets.keys():
					assets[asset_type] = []
				assets[asset_type].append(asset_name)
		return assets
		
	def compare_dirs(self, directory1, directory2):
		comparison_result = []
		root_comparison = filecmp.dircmp(directory1, directory2)
		self.__compare_dirs_recur(root_comparison, comparison_result)
		return comparison_result
	
	def __compare_dirs_recur(self, comparison, comparison_result):
		left_dirs = comparison.left_list
		right_dirs = comparison.right_list
		subdirectories = comparison.subdirs
		if len(left_dirs) != len(right_dirs):
			temp_comparison_result = []
			left_set = set(left_dirs)
			right_set = set(right_dirs)
			left_only_dirs = list(left_set.difference(right_set))
			right_only_dirs = list(right_set.difference(left_set))
			if left_only_dirs != []:
				for l in left_only_dirs:
					temp_comparison_result.append((1, comparison.left.replace("\\", "/") + "/" + l))
			else:
				temp_comparison_result.append((0, comparison.left.replace("\\", "/")))
			if right_only_dirs != []:
				for r in right_only_dirs:
					temp_comparison_result.append((1, comparison.right.replace("\\", "/") + "/" + r))
			else:
				temp_comparison_result.append((0, comparison.right.replace("\\", "/")))
			comparison_result.append(temp_comparison_result)
		for key in subdirectories.keys():
			subdirectory_comparison = subdirectories[key]
			self.__compare_dirs_recur(subdirectory_comparison, comparison_result)
			
	def last_scene(self, asset, asset_type):
		asset_master_path = "scenes/stock/" + asset_type + "/" + asset + "/master/"
		master_files = [f for f in os.listdir(asset_master_path) if os.path.isfile(asset_master_path + f)]
		return master_files[0]

