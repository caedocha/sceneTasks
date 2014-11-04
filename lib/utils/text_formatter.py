import re

class TextFormatter(object):

	@staticmethod
	def camel_case(target, sep = "_"):
		""" Converts snake case string to camel case. """
		return "".join([s.capitalize() for s in target.split(sep)])

	@staticmethod
	def snake_case(target, sep = "_"):
		""" Converts camel case string to snake case. """
		return sep.join([s.lower() for s in filter(lambda s: s != "", re.split("([A-Z][a-z]*)",target))])
