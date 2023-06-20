from thread import *
import os, sys


class Logger:
	def __init__(self, file=os.path.abspath("log.txt")):
		self._file = file

	def init(self):
		self.queue = []
		self.busy = False

	def log(self, *string, end="\n", sep=" "):
		string = sep.join(tuple(string))+end
		while self.busy: pass
		self.busy = True
		# self.file.write(string)
		# self.file.flush()
		print(string, end="")
		self.busy = False
