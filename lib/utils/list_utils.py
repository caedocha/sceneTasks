class ListUtils(object):

	@staticmethod
	def pairwise(items):
		""" Genenator which returns the current iterated item of a list, and the next one. """
		iterate = True
		i = 0
		if items != []:
			while iterate:
				if i < (len(items) - 1):
					yield items[i], items[i + 1]
				else:
					iterate = False
				i += 1
			yield items[len(items) - 1], None
		else:
			raise IndexError
