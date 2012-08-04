from bot.config_handler import ConfigFile
from bot.main import BOT
from bot.api import listener, Event, command, A, Q3
import sys, os, time

class Timer(object):
	def __init__(self, name=None):
		self.name = name
		self.startt = 0
		self.endt = 0
		self.running = False
	
	def start(self): 
		if not self.running:
			self.startt = time.time()
			self.running = True

	def stop(self):
		if self.running: 
			self.endt = time.time()
			self.running = False

	def value(self): 
		x = self.endt-self.startt
		return '{number:.{digits}f}'.format(number=x, digits=2)

	def reset(self):
		self.startt = 0
		self.endt = 0
		self.running = False

redFlag = Timer('Blue Flag')
blueFlag = Timer('Red Flag')

@listener('GAME_FLAG')
def eventListener(obj):
	flags = {1:redFlag, 2:blueFlag}
	if obj._name == "GAME_FLAG_PICKUP":
		if not flags[obj.flagid].running:
			flags[obj.flagid].start()

	elif obj._name == "GAME_FLAG_CAPTURE":
		if flags[obj.flagid].running:
			o = flags[obj.flagid]
			o.stop()
			A.say('%s captured in %s seconds' % (o.name, o.value())) #@TODO add color

	elif obj._name in ['GAME_FLAG_RETURN', 'GAME_FLAG_HOTPOTATO']:
		if flags[obj.flagid].running:
			flags[obj.flagid].reset()

def onEnable(): pass
def onDisable(): pass
def onBoot(): pass