import filecmp
import os
import pprint as p
import inspect
#from sets import Set

#d = dircmp('./scenes/stock/', './source_images/textures/stock/')

#print d.subdirs
#for x in d.subdirs['char'].subdirs.keys():
#	print x, d.subdirs['char'].subdirs[x]
#print d.subdirs['char'].left_list
#print d.subdirs['char'].right_list
#print d.left_list
#print d.right_list

#print Set(d.left_list).symmetric_difference(Set(d.right_list))



def compare_dirs(directory1, directory2):
	comparison_result = []
	root_comparison = filecmp.dircmp(directory1, directory2)
	compare_dirs_recur(root_comparison, comparison_result)
	return comparison_result
	
def compare_dirs_recur(comparison, comparison_result):
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
		compare_dirs_recur(subdirectory_comparison, comparison_result)


for x in compare_dirs('./scenes/stock/', './source_images/textures/stock/'):
	for y in x:
		print y
	print "-" * 20
