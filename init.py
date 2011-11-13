#---IMPORTS---#
import subprocess, time, os, sys, imp, player
from events import *
import events
from pyquake3 import PyQuake3
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

class Bot():
	def __init__(self, prefix="^1[^3Boteh^1]:", ip='localhost:27960', rcon=""):
		self.prefix = prefix
		self.ip = ip
		self.rcon = rcon
		self.Q = PyQuake3(self.ip, rcon_password=self.rcon)

		self.Modules = {} #Plugins
		self.Listeners = {} #Plugins waiting for Triggers
		self.Triggers = {} #Possible Triggers (Events)
		self.Commands = {} #Commands

		self.Clients = {} #AKA players

	def eventFire(event, data): pass

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
	def plist(self):
		self.Q.update()
		return self.Q.players
	def getPlayer(self, iid=0):
		if len(self.B.Players) != 0: return self.B.Players[iid]
		else: return None
	def getPlayers(self): return self.B.Players
	def getCommands(self): return self.B.Commands
	def whatTeam(self, num): return const.teams[num]
	def exitProc(self): proc.kill()
	def bootProc(self): keepLoop = False #@DEV Need a way of rebooting el boto
	def addEvent(self, event, func):
		for i in self.B.Listeners.keys():
			if i == event and self.B.Listeners[i] != None:
				self.B.Listeners[i].append(func)
				return True
		self.B.Listeners[event] = [func]

	def addCmd(self, cmd, func, desc='None'):
		if cmd in self.B.Commands.keys():
			print "Can't add command %s, another plugin already added it!" % (cmd)
			return False
		self.B.Commands[cmd] = (func,desc)
		return True

	def addTrigger(self, trigger):
		if trigger in self.B.Triggers.keys():
			print "Can't add trigger %s, another plugin already added it!" % (trigger)
			return False
		self.B.Triggers[trigger] = []
		return True

def _conn(uid):
	global BOT
	BOT.Q.rcon_update()
	for i in BOT.Q.players:
		if i.uid == uid:
			name = i.name
			ip = i.ip
	obj = Event('conn',(uid,name,ip))
	Listen('conn',obj)
	return obj

def load():
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

def parseUserInfo(inp): #@DEV Replace with regex
	varz = {}
	inp = inp.split("\\")
	uid = int(inp[0].split(" ")[1])
	x = inp[1]
	y = 1
	while len(x) > y:
		varz[x[y-1]] = x[y]
		y+=2
	return uid,varz

def parseUserInfoChange(inp): #@DEV Replace with regex
	global BOT
	varz = {}
	varz2 = {}
	m = inp.split(" ")
	uid = int(m[1])
	x = m[2].split("\\")
	y = 1
	while len(x) > y:
		varz[x[y-1]] = x[y]
		y+=2
	return uid,varz

def parseKill(attacker,victim,method):
	if method in [1, 3, 9, 39]:
		BOT.eventFire('CLIENT_WORLDDEATH', {'vic':victim, 'meth':method})
	elif method in [7, 6, 10, 31, 320]:
		BOT.eventFire('CLIENT_SUICIDE', {'vic':victim, 'meth':method})
	else:
		BOT.eventFire('CLIENT_KILL', {'atk':attacker, 'vic':victim, 'meth':method})
		BOT.eventFire('CLIENT_GENERICDEATH', {'vic':victim})

def parse(inp):
	global BOT
	if inp.startswith("say:"):
		#say: 0 [WoC]*B1naryth1ef: blah blah
		#['0', '[WoC]*B1naryth1ef', 'blah blah']
		inp = inp.split(" ", 3)
		inp.pop(0)
		inp[1] = inp[1].strip(':') 
		eventTrigger('CHAT_MESSAGE', {'event':'CHAT_MESSAGE', 'sender':inp[1], 'gid':inp[0], 'msg':inp[2]})

	elif inp.startswith('ClientConnect:'):
		#ClientConnect: 0
		inp = inp.split(" ")
		inp = int(inp[1])
		if inp >= 0: BOT.eventFire('CLIENT_CONNECT', inp)

	elif inp.startswith('ClientUserinfo:'):
		uid, varz = parseUserInfo(inp)
		if uid in BOT.Clients.keys(): BOT.Clients[uid] = player.Player(uid, varz)

	elif inp.startswith('ClientUserinfoChanged:'):
		uid, varz = parseUserInfoChange(inp)

	elif inp.startswith('ClientDisconnect:'): pass
	elif inp.startswith('Kill:'):
		#Kill: 1 0 15: WolfXxXBunny killed [WoC]*B1naryth1ef by UT_MOD_DEAGLE
		inp = inp.split(" ")
		inp.pop(0)
		attacker = int(inp[0])
		victim = int(inp[1])
		method = int(inp[2])
		parseKill(attacker, victim, method)

	elif inp.startswith('Hit:'): pass
	elif inp.startswith('Item'): pass
	elif inp.startswith('Flag:'): pass
	else: pass

	# if inp.startswith("say:"):
	# 	newy = inp.split(':',2)
	# 	nsender = newy[1]
	# 	nmsg = newy[2].rstrip()
	# 	ncmd1 = nmsg.strip(" ")
	# 	ncmd = ncmd1.split(" ")[0]
	# elif inp.startswith('ClientConnect:'):
	# 	new = inp.split(":")[1].strip()
	# 	_conn(new)
	# elif inp.startswith('ClientUserinfo:'): 
	# 	ret = parseUserInfo(inp)
	# 	#@DEV Add UserInfo event here
	# elif inp.startswith('ClientUserinfoChanged:'): 
	# 	ret = parseUserInfoChange(inp)
	# 	#@DEV Add InfoChange event here
	# elif inp.startswith('Kill:'):
	# 	newy = inp.split(" ")
	# 	x = {}
	# 	x['type'] = newy[8]
	# 	x['victim'] = newy[6]
	# 	x['attacker'] = newy[4]
	# 	spawnEvent(x)
		
def loadConfig():
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
	pass

def loop():
	global proc, keepLoop
	while True:
		if keepLoop is True:
			proc_read = proc.stdout.readline()
			if proc_read:
				print proc_read.rstrip()
				parse(proc_read)
		else:
			break
	return proc

if __name__ == "__main__":
	loadConfig()
	BOT = Bot(config_prefix, config_rconip, config_rcon)
	load()
	proc = subprocess.Popen(config_bootcommand, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	loop()
