#!/usr/bin/python
#---IMPORTS---#
import subprocess, time, os, sys, imp, player, string, re, socket
from events import *
import events
from rcon import RCON
import const

#--SETTRZ--#
home = os.getcwd()
lastsent = None
keepLoop = True

#--GLOB--#
config_prefix = None
config_rcon = None
config_rconip = None
config_bootcommand = None
config_groups = None
config_plugins = None

def canInt(i):
	try:
		int(i)
		return True
	except:
		return False

class Bot():
	def __init__(self, prefix="^1[^3Boteh^1]:", ip='localhost:27960', rcon=""):
		self.prefix = prefix
		self.ip = ip
		self.rcon = rcon
		self.Q = RCON(self.ip, self.rcon)

		self.Modules = {} #Plugins
		self.Listeners = {} #Plugins waiting for Triggers
		self.Triggers = {} #Possible Triggers (Events)
		self.Commands = {} #Commands

		self.Clients = {} #AKA players

	def eventFire(self, event, data): 
		obj = events.EVENTS[event](data)
		for i in self.Listeners.keys():
			if i == event:
				for listener in self.Listeners[i]:
					listener(obj)
				break
		return obj
		
class API():
	RED = '^1'
	GREEN = '^2'
	YELLOW = '^3'
	BLUE = '^4'
	CYAN = '^5'
	MAGENTA = '^6'
	WHITE = '^7'
	BLACK = '^8'

	def __init__(self, auth=None):
		self.B = BOT
		self.Q = BOT.Q
		self.auth = auth
	def tester(self): print "TESTING! 1! 2! 3!"
	def say(self,msg): self.Q.rcon("say "+self.B.prefix+" ^2"+msg)
	def tell(self,uid,msg): self.Q.rcon("tell %s %s %s " % (uid, self.B.prefix, msg))
	def rcon(self,cmd): return self.Q.rcon(cmd)
	def getPlayer(self, iid=0):
		if len(self.B.Players) != 0: return self.B.Players[iid]
		else: return None
	def getPlayers(self): return self.B.Players
	def getCommands(self): return self.B.Commands
	def whatTeam(self, num): return const.teams[num]
	def exitProc(self): proc.kill()
	def bootProc(self): keepLoop = False #@DEV Need a way of rebooting el boto
	def reboot(self): handlr.initz('reboot')
	def addEvent(self, event, func): #Add a listener (confusing? Rename?)
		for i in self.B.Listeners.keys():
			if i == event and self.B.Listeners[i] != None:
				self.B.Listeners[i].append(func)
				return True
		self.B.Listeners[event] = [func]
	def addCmd(self, cmd, func, desc='None', level=0):
		if cmd in self.B.Commands.keys():
			print "Can't add command %s, another plugin already added it!" % (cmd)
			return False
		self.B.Commands[cmd] = (func,desc,level)
		return True
	def addTrigger(self, trigger):
		if trigger in self.B.Triggers.keys():
			print "Can't add trigger %s, another plugin already added it!" % (trigger)
			return False
		self.B.Triggers[trigger] = []
		return True

def loadMods():
	global BOT
	fn = []
	modx = []
	county = 0
	for i in os.listdir(os.path.join(home, 'mods')):
		if i.endswith('.py') and not i.startswith("_"):
			fn.append(os.path.join(home, 'mods', i))
	for f in fn:
		fname = os.path.basename(f)[:-3]
		try:
			mod = imp.load_source(fname, f)
			name = getattr(mod, "_name")
			author = getattr(mod, "_author")
			version = getattr(mod, "_version")
			mod.init(API())
			print "Loaded: %s (Version: %s) by %s" % (name, version, author)
		except Exception, e:
			print "ERROR LOADING %s: %s" % (name, e)	

def parseUserInfo(inp, varz={}):
	inp2 = inp.split(' ', 2)
	uid = int(inp2[1])
	var = re.findall(r'\\([^\\]+)\\([^\\]+)', inp)
	for i in var:
		varz[i[0]] = i[1]
	return uid,varz
	
def parseUserInfoChange(inp, varz={}, vary={}): #@DEV Replace with regex
	#r is race, n is name, t is team
	#ClientUserinfoChanged: 0 n\[WoC]*WolfXxXBunny\t\3\r\0\tl\0\f0\\f1\\f2\\a0\0\a1\0\a2\255
	inp2 = inp.split(' ', 2)
	uid = int(inp2[1])
	var = re.findall(r'\\([^\\]+)\\([^\\]+)', inp)
	for i in var:
		varz[i[0]] = i[1]
	if 't' in varz.keys(): vary['team'] = varz['t']
	if 'n' in varz.keys(): vary['name'] = varz['n']
	return uid,vary

def parseKill(inp):
	#Kill: 1 0 15: WolfXxXBunny killed [WoC]*B1naryth1ef by UT_MOD_DEAGLE
	inp = inp.split(" ")
	inp.pop(0)
	attacker = int(inp[0])
	victim = int(inp[1])
	method = int(inp[2].strip(':'))
	if method in [1, 3, 9, 39]: BOT.eventFire('CLIENT_WORLDDEATH', {'vic':victim, 'meth':method})
	elif method in [7, 6, 10, 31, 320]: BOT.eventFire('CLIENT_SUICIDE', {'vic':victim, 'meth':method})
	else:
		BOT.eventFire('CLIENT_KILL', {'atk':attacker, 'vic':victim, 'meth':method})
		BOT.eventFire('CLIENT_GENERICDEATH', {'vic':victim})

def parseHit(inp):
	#Hit: 1 0 2 21: Skin_antifa(fr) hit Antho888 in the Torso
	inp = inp.split(' ')
	attacker = inp[1]
	victim = inp[2]
	hitloc = inp[3]
	method = inp[4]
	BOT.eventFire('CLIENT_HIT', {'atk':attacker, 'vic':victim, 'loc':hitloc, 'meth':method})

def parseItem(inp):
	inp = inp.split(' ')
	item = inp[2]
	client = inp[1]
	BOT.eventFire('CLIENT_PICKUPITEM', {'item':item, 'client':client})

def parse(inp):
	global BOT
	if inp.startswith("say:"):
		#say: 0 [WoC]*B1naryth1ef: blah blah
		#['0', '[WoC]*B1naryth1ef', 'blah blah']
		inp = inp.split(" ", 3)
		inp.pop(0)
		inp[1] = inp[1].strip(':')
		if inp[2].startswith('!'):
			BOT.eventFire('CLIENT_COMMAND', {'event':'CHAT_MESSAGE', 'name':inp[1], 'sender':inp[0], 'msg':inp[2]})
			print BOT.Commands, inp[2].rstrip().split(' ')[0]
			if inp[2].rstrip().split(' ')[0] in BOT.Commands.keys():
				print "Natural fire"
				BOT.Commands[inp[2].rstrip().split(' ')[0]][0](BOT.eventFire('CLIENT_COMMAND', {'sender':inp[0], 'msg':inp[2]})) #@TEMP 0 should become chat object
		BOT.eventFire('CHAT_MESSAGE', {'event':'CHAT_MESSAGE', 'sender':inp[1], 'gid':inp[0], 'msg':inp[2]})

	elif inp.startswith('ClientConnect:'):
		#ClientConnect: 0
		inp = int(inp.split(" ")[1])
		if inp >= 0: BOT.eventFire('CLIENT_CONNECT', inp)

	elif inp.startswith('ClientUserinfo:'):
		uid, varz = parseUserInfo(inp)
		print uid, varz
		if uid in BOT.Clients.keys(): BOT.Clients[uid].setData(varz)
		else: BOT.Clients[uid] = player.Player(uid, varz)

	elif inp.startswith('ClientUserinfoChanged:'): 
		uid, varz = parseUserInfoChange(inp)

	elif inp.startswith('ClientDisconnect:'):
		inp = int(inp.split(" ")[1])
		BOT.eventFire('CLIENT_DISCONNECT', inp)
		if inp in BOT.Clients.keys(): del BOT.Clients[inp]

	elif inp.startswith('Kill:'): 
		parseKill(inp)

	elif inp.startswith('Hit:'): 
		parseHit(inp)
	elif inp.startswith('Item'):
		parseItem(inp)
	elif inp.startswith('Flag:'): pass
	else: pass
		
def loadConfig():
	"""Loads the bot config"""
	global config_prefix, config_rcon, config_rconip, config_bootcommand, config_plugins, config_groups
	try:
		from config import botConfig
		config_prefix = botConfig['prefix']
		config_rcon = botConfig['rcon']
		config_rconip = botConfig['rconip']
		config_bootcommand = botConfig['servercommand']
		config_plugins = botConfig['plugins']
		config_groups = botConfig['groups']
	except Exception, e:
		print "Error loading config! %s" % (e)
		print "Exiting..."

def loadDatabase():
	"""Should load db.py"""
	pass

def loop():
	"""The entire loop"""
	global proc, keepLoop
	while True:
		if keepLoop is True:
			proc_read = proc.readline()
			if proc_read:
				print proc_read.rstrip()
				parse(proc_read)
		else:
			break
	return proc

def Start(func, nothing):
	global BOT, proc, handlr
	handlr = func
	loadConfig()
	BOT = Bot(config_prefix, config_rconip, config_rcon)
	loadMods()
	#proc = subprocess.Popen(config_bootcommand, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	procsocket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	procsocket.connect('/tmp/quake3stdout')
	proc = os.fdopen(procsocket.fileno())
	loop()

def Exit():
	sys.exit()

# Just using this while the handler code is a WIP
class DUMMY:
	def __init__(self): pass
	def initz(self, arg):
		pass

if __name__ == "__main__":
	dummy = DUMMY()
	Start(dummy, None)
