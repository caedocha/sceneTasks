from ctypes import *

class Notifier(object):

	def __init__(self):
		windll.Kernel32.GetStdHandle.restype = c_ulong
		self.__h = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))
		self.__term_color = 15
		self.__checkpoint_counter = 1
		self.__mute = False

	def error(self, msg, prefix = True):
		self.__term_color = 12
		if prefix:
			msg = "- ERROR: " + msg
		self.notify(msg)

	def neutral(self, msg, prefix = True):
		self.__term_color = 14
		if prefix:
			msg = "* ACTION: " + msg
		self.notify(msg)

	def success(self, msg, prefix = True):
		self.__term_color = 10
		if prefix:
			msg = "+ SUCCESS: " + msg
		self.notify(msg)

	def notify(self, msg, pretty_print=False):
		if pretty_print:
			pprint.pprint(msg)
		else:
			windll.Kernel32.SetConsoleTextAttribute(self.__h, self.__term_color)
			print(msg)
			windll.Kernel32.SetConsoleTextAttribute(self.__h, 15)

	def checkpoint(self, msg):
		self.__term_color = 9
		msg = "!CHECKPOINT %i: %s" % (self.__checkpoint_counter, msg)
		self.notify(msg)
		self.__checkpoint_counter += 1

	def mute(self):
		self.__mute = True
	
	def unmute(self):
		self.__mute = False
