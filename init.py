#!/usr/bin/python
#---IMPORTS---#
import subprocess, time, os, sys, imp, player, string, re, socket
from events import *
import events
from rcon import RCON
import const
import database
import auth
import select
import thread


__Version__ = 0.3

#--SETTRZ--#
A = None
home = os.getcwd()
lastsent = None
keepLoop = True
botDEBUGS = []
pluginDEBUGS = []

#--GLOB--#
config_prefix = None
config_rcon = None
config_rconip = None
config_bootcommand = None
config_groups = None
config_plugins = None
config_serversocket = None

def canInt(i):
	try:
		int(i)
		return True
	except:
		return False

class GameOutput():
	def __init__(self, usockname=None):
		self.usockname = usockname
		self.usock = None
		self.buf = ''
		self.lines = []

		if self.usockname: self.connect(self.usockname)

	def connect(self, usockname):
		if self.usock: self.usock.close()
		self.usock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		self.usock.connect(usockname)

	def checkAndRead(self):
		newbuf = None
		readrdy = select.select([self.usock], [], [], 0.10)[0]
		if readrdy != []:
			self.buf += self.usock.recv(4096)
			for line in self.buf.splitlines(True):
				if line.endswith("\n"): self.lines.append(line.strip())
				else: newbuf = line
			if newbuf: self.buf = newbuf
			else: self.buf = ''

	def hasLine(self):
		if len(self.lines): return 1
		return 0

	def getLine(self):
		return self.lines.pop(0)

class Bot():
	def __init__(self, prefix="^1[^3Boteh^1]:", ip='localhost:27960', rcon="", debug=False):
		from config import UrTConfig

		self.prefix = prefix
		self.ip = ip
		self.rcon = rcon
		self.Q = RCON(self.ip, self.rcon)
		self.db = database.DB()
		self.status = 1 #1 is on, 0 is off
		self.debug = debug #False will hide messages, True will print them and log them to vars
		
		self.maplist = UrTConfig['maps']

		self.Modules = {} #Plugins
		self.Listeners = {} #Plugins waiting for Triggers
		self.Triggers = {} #Possible Triggers (Events)
		self.Commands = {} #Commands

		self.Clients = {} #AKA players
		
	def getClient(self, uid): return self.Clients[uid]

	def eventFire(self, event, data): 
		obj = events.EVENTS[event](data)
		for i in self.Listeners.keys():
			if i == event:
				for listener in self.Listeners[i]:
					thread.start_new_thread(listener, (obj, False))
				break
		return obj

	def Startup(self):
		print 'CALLED STARTUP'
		from config import UrTConfig
		self.Q.rcon("say "+self.prefix+" ^3"+"Starting up...")
		
		# Get the PK3s/maps the server has loaded
		pk3s = self.Q.rcon("sv_pakNames").split('"')[3].split()
		for ignore in UrTConfig['ignoremaps']:
			if ignore in pk3s: pk3s.remove(ignore)
		self.maplist += pk3s
		print self.maplist

		# We only take active client ids from status, everything else from dumpuser
		status = self.Q.rcon("status").splitlines(False)[4:-1]
		if status == []: return #If no users are connected, we should just ignore them...

		for uid in [info.split()[0] for info in status]:
			uid = int(uid)
			info = self.Q.rcon("dumpuser %s" % uid).splitlines(False)[3:]
			if info == []: continue
			data = {}
			for line in info:
				 line = line.split()
				 data[line[0]] = line[1]
			self.Clients[uid] = player.Player(uid, data)
			if self.Clients[uid].cl_guid != None:
				self.db.clientUpdate(self.Clients[uid])
				self.Clients[uid].group = auth.checkUserAuth(self.db, self.Clients[uid].cl_guid, self.Clients[uid].ip, self.Clients[uid].name)

		self.Q.rcon("say "+self.prefix+" ^3"+"Startup complete.")
		print 'STARTUP DONE'

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
	def debug(self, msg, plugin=None): 
		if self.B.debug is True: 
			if plugin is None:
				print '[DEBUG]', msg
				botDEBUGS.append((time.time(), msg))
			else:
				print '[DEBUG|%s] %s' % (plugin, msg)
				pluginDEBUGS.append((time.time(), plugin, msg))
	def tester(self): self.debug("TESTING! 1! 2! 3!")
	def say(self,msg): self.Q.rcon("say "+self.B.prefix+" ^3"+msg)
	def tell(self,uid,msg): self.Q.rcon("tell %s %s %s " % (uid, self.B.prefix, msg))
	def rcon(self,cmd): return self.Q.rcon(cmd)
	def getClients(self): return self.B.Clients
	def getCommands(self): return self.B.Commands
	def whatTeam(self, num): return const.teams[num]
	def exitProc(self): sys.exit()
	def bootProc(self): keepLoop = False #@DEV Need a way of rebooting el boto
	def reboot(self): handlr.initz('reboot')
	def getCmd(self, cmd): return self.B.Commands.get(cmd)
	def getClient(self, iid=0):
		if len(self.B.Clients) != 0: return self.B.Clients.get(int(iid))
		else: return None
	def findMap(self, mapname):
		maplist = []
		for name in self.B.maplist:
			if mapname == name or ("ut4_" + mapname) == name: return [name]
			elif mapname in name: maplist.append(name)
		return maplist
	def addListener(self, event, func): 
		if event in self.B.Listeners.keys():
			if self.B.Listeners[event] != None: self.B.Listeners[event].append(func)
			else: self.B.Listeners[event] = [func]
			return True
		else: self.B.Listeners[event] = [func]
	def addListeners(self, events, func):
		for i in events:
			if i in self.B.Listeners.keys():
				if self.B.Listeners[i] != None: self.B.Listeners[i].append(func)
				else: self.B.Listeners[i] = [func]
			else: self.B.Listeners[i] = [func]
	def addCmd(self, cmd, func, desc='None', level=0):
		if cmd in self.B.Commands.keys():
			self.debug("Can't add command %s, another plugin already added it!" % (cmd))
			return False
		self.B.Commands[cmd] = (func,desc,level)
		return True
	def addCmds(self, cmds):
		for i in cmds:
			if i[0] in self.B.Commands.keys(): self.debug("Can't add command %s, another plugin already added it!" % (i[0]))
			else: self.B.Commands[i[0]] = (i[1], i[2], i[3])
	def addTrigger(self, trigger):
		if trigger in self.B.Triggers.keys():
			self.debug("Can't add trigger %s, another plugin already added it!" % (trigger))
			return False
		self.B.Triggers[trigger] = []
		return True
	def retrieveTeam(self, team):
		reply = A.rcon("g_" + team + "TeamList").splitlines()[1:][0]
		players = reply.split('\"')[3].split("^")[0]
		ids = []
		for char in players:
			cid = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".find(char)
			if cid != -1: ids.append(cid)
		return ids


def parseUserInfo(inp, varz={}):
	inp2 = inp.split(' ', 2)
	uid = int(inp2[1])
	var = re.findall(r'\\([^\\]+)\\([^\\]+)', inp)
	for i in var:
		varz[i[0]] = i[1]
	return uid,varz
	
def parseUserInfoChange(inp, varz={}, vary={}):
	#r is race, n is name, t is team
	#ClientUserinfoChanged: 0 n\[WoC]*WolfXxXBunny\t\3\r\0\tl\0\f0\\f1\\f2\\a0\0\a1\0\a2\255
	inp2 = inp.split(' ', 2)
	uid = int(inp2[1])
	var = re.findall(r'([^\\]+)\\([^\\]+)', inp2[2])
	for i in var:
		varz[i[0]] = i[1]
	print varz
	if 't' in varz.keys(): vary['team'] = const.teams.get(int(varz['t']))
	if 'n' in varz.keys(): vary['name'] = varz['n']
	# probably should figure out what those other fields are?
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
	#Item: 1 ut_weapon_ump45
	inp = inp.split(' ')
	item = inp[2].strip()
	client = inp[1]
	if item in const.flagtypes.keys(): BOT.eventFire('GAME_FLAGPICKUP', {'client':client, 'flag':item, 'team':const.flagtypes[item], 'flagid':const.flagtypes[item]})
	else: 
		BOT.eventFire('CLIENT_PICKUPITEM', {'item':item, 'itemint':0, 'client':client})

def parsePlayerBegin(inp):
	#ClientBegin: 0
	print "DID IT!"
	inp = inp.split(' ')
	client = int(inp[1])
	BOT.eventFire('CLIENT_BEGIN', {'client':client})

def parseFlag(inp):
	#Flag: 0 2: team_CTF_redflag
	inp = inp.split(' ', 3)
	cid = inp[1]
	action = int(inp[2].strip(':'))
	flag = inp[3].strip()
	flagid = const.flagtypes[flag]
	if action == 0: BOT.eventFire('GAME_FLAGDROP', {'client':cid, 'actionid':action, 'action':const.flagactions[action], 'flag':flag, 'flagid':flagid}) #drop
	elif action == 1: BOT.eventFire('GAME_FLAGRETURN', {'client':cid, 'actionid':action, 'action':const.flagactions[action], 'flag':flag, 'flagid':flagid}) #return
	elif action == 2: BOT.eventFire('GAME_FLAGCAPTURE', {'client':cid, 'actionid':action, 'action':const.flagactions[action], 'flag':flag, 'flagid':flagid}) #score

def parseFlagReturn(inp):
	inp = inp.split(' ', 3)
	flag = inp[2].strip()
	BOT.eventFire('GAME_FLAGRESET', {'flag':flag, 'flagid':const.flagtypes[flag]})

def parse(inp):
	global BOT
	if inp.startswith("say:"):
		#say: 0 [WoC]*B1naryth1ef: blah blah
		inp = inp.split(" ", 3)
		inp.pop(0)
		inp[1] = inp[1].strip(':')
		if inp[2].startswith('!'):
			BOT.eventFire('CLIENT_COMMAND', {'event':'CHAT_MESSAGE', 'name':inp[1], 'sender':inp[0], 'msg':inp[2]})
			print BOT.Commands, inp[2].rstrip().split(' ')[0]
			cmd = inp[2].rstrip().split(' ')[0]
			if cmd in BOT.Commands.keys():
				uid = int(inp[0])
				#@DEV Auth is rechecked for each command; shotgun approach, do this more elegantly
				BOT.Clients[uid].group = auth.checkUserAuth(BOT.db, BOT.Clients[uid].cl_guid, BOT.Clients[uid].ip, BOT.Clients[uid].name)
				if BOT.getClient(uid).group >= BOT.Commands[cmd][2]:
					thread.start_new_thread(BOT.Commands[cmd][0], (BOT.eventFire('CLIENT_COMMAND', {'sender':inp[0], 'sendersplit':inp[0].split(' '), 'msg':inp[2], 'cmd':cmd}), True)) 
				else:
					msg = "You lack sufficient access to use %s [%s]" % (cmd, BOT.Clients[uid].group)
					BOT.Q.rcon("tell %s %s %s " % (inp[0], BOT.prefix, msg))
		BOT.eventFire('CHAT_MESSAGE', {'event':'CHAT_MESSAGE', 'sender':inp[1], 'gid':inp[0], 'msg':inp[2]})

	elif inp.startswith('ClientConnect:'):
		#ClientConnect: 0
		inp = int(inp.split(" ")[1])
		if inp in BOT.Clients.keys():
			#'til we find ways to work around the missing ClientDisconnect messages... this won't be fatal. 
			#raise const.UrTBotError('Client #%s is already connected... Something is wrong.' % (inp))
			print const.UrTBotError('Client #%s is already connected... Something is wrong. Flush \'em, danno!' % (inp))
			del BOT.Clients[inp]
		if inp >= 0: BOT.eventFire('CLIENT_CONNECT', {'client':inp})

	elif inp.startswith('ClientUserinfo:'):
		uid, varz = parseUserInfo(inp)
		print uid, varz
		if uid in BOT.Clients.keys(): BOT.Clients[uid].setData(varz)
		else:
			BOT.Clients[uid] = player.Player(uid, varz)
			if BOT.Clients[uid].cl_guid != None:
				BOT.db.clientUpdate(BOT.Clients[uid])
				BOT.Clients[uid].group = auth.checkUserAuth(BOT.db, BOT.Clients[uid].cl_guid, BOT.Clients[uid].ip, BOT.Clients[uid].name)

	elif inp.startswith('ClientUserinfoChanged:'): 
		# Different than ClientUserinfo because we don't add clients to the list or DB, just update
		uid, varz = parseUserInfoChange(inp, {}, {})
		print uid, varz
		if uid in BOT.Clients.keys(): BOT.Clients[uid].setData(varz)

	elif inp.startswith('ClientDisconnect:'):
		inp = int(inp.split(" ")[1])
		BOT.eventFire('CLIENT_DISCONNECT', {'client':inp})
		if inp in BOT.Clients.keys(): del BOT.Clients[inp]

	elif inp.startswith('Kill:'): 
		parseKill(inp)
	elif inp.startswith('Hit:'): 
		parseHit(inp)
	elif inp.startswith('Item'):
		parseItem(inp)
	elif inp.startswith('Flag:'): parseFlag(inp)
	elif inp.startswith('Flag Return:'): parseFlagReturn(inp)
	elif inp.startswith('ClientBegin:'): parsePlayerBegin(inp)

	elif inp.startswith('ShutdownGame:'):
		BOT.eventFire('GAME_SHUTDOWN', {})
		# We clear out our client list on shutdown. Doesn't happen with 'rcon map ..' but does
		# when the mapcycle changes maps? hrmph. investigate.
		# In fact I'm not sure how to detect an 'rcon map' yet! Geeeeeez.
		for key in BOT.Clients.keys():
			BOT.eventFire('CLIENT_DISCONNECT', {'client':key})
			del BOT.Clients[key]

	else: pass
		
def loadConfig():
	"""Loads the bot config"""
	global config_prefix, config_rcon, config_rconip, config_bootcommand, config_plugins, config_groups, config_serversocket, config_debugmode
	try:
		from config import botConfig
		config_prefix = botConfig['prefix']
		config_rcon = botConfig['rcon']
		config_rconip = botConfig['rconip']
		config_bootcommand = botConfig['servercommand']
		config_plugins = botConfig['plugins']
		config_groups = botConfig['groups']
		config_serversocket = botConfig['serversocket']
		config_debugmode = botConfig['debug_mode']
	except Exception, e:
		print "Error loading config! [%s]" % (e)

def loadMods():
	global BOT, A
	for i in config_plugins:
		A.debug('Loading: %s...' % (i))
		__import__('mods.'+i)
		i = sys.modules['mods.'+i]
		try: thread.start_new_thread(i.init, ())
		except Exception, e:
			A.debug('Error in loadMods() [%s]' % (e))

def loop():
	"""The entire loop"""
	global proc, keepLoop
	while True:
		proc.checkAndRead()
		while proc.hasLine():
			line = proc.getLine()
			if line != '^1Error: weapon number out of range':
				print line
			parse(line)

def Start():
	global BOT, proc, A, config_debugmode
	loadConfig()
	auth.load()
	BOT = Bot(config_prefix, config_rconip, config_rcon, debug=config_debugmode)
	A = API()
	BOT.Startup()
	loadMods()
	proc = GameOutput(config_serversocket)
	x = os.uname() #@DEV Is this windows friendly?
	A.say('UrTBot V%s loaded on %s (%s/%s)' % (__Version__, sys.platform, x[2], x[4])) 
	loop()

def Exit(): sys.exit()

if __name__ == "__main__":
	Start()
