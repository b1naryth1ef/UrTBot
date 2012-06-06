from ..debug import log
from ..init import config

class Database():
	def __init__(self):
		config

class User():
	def __init__(self, name=None, guid=None, ip=None, group=0, password='', joincount=0, firstjoin=None, lastjoin=None):
		self.name = name
		self.guid = guid
		self.ip = ip
		self.group = group
		self.password = password
		self.joincount = joincount
		self.firstjoin = firstjoin
		self.lastjoin = lastjoin	

	def save(self): pass
	def clientJoin(self): pass
	def clientQuit(self): pass

def setup(): pass