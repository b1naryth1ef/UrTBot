#api
import main

class Mod(object):
	def __init__(self,name,version):
		self.name = name
		self.version = version
		self.cmds = {}
		self.hooks = {}
	def cmdreg(self,cmd,exe):
		self.cmds[cmd] = exe
		main.CR(cmd,exe)
	def hookreg(self,event,exe):
		if not self.hooks:
			self.hooks[event] = [exe]
		else:
			self.hooks[event].append(exe)
		main.LR(event,exe)