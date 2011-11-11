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

class Bot():
	def __init__(self, prefix="^1[^3Boteh^1]:", ip='localhost:27960', rcon=""):
		self.prefix = prefix
		self.ip = ip
		self.rcon = rcon
		self.Q = PyQuake3(self.ip, rcon_password=self.rcon)

		self.Modules = {} #Plugins
		self.Listeners = {} #Plugins waiting for Triggers
		self.Triggers = {} #Possible Triggers
		self.Commands = {} #Commands


		self.Players = {}

BOT = Bot(rcon="Norp123")

def Listen(event, obj):
	global BOT
	if event in BOT.Listeners:
		for i in BOT.Listeners[event]:
			i(obj)
	else:
		pass

class API():
	#@DEV Can these just be api.RED???
	cRED = '^1'
	cGREEN = '^2'
	cYELLOW = '^3'
	cBLUE = '^4'
	cCYAN = '^5'
	cMAGENTA = '^6'
	cWHITE = '^7'
	cBLACK = '^8'

	def rEve(self, event, func):
		x = BOT.Listeners
		for i in x.keys():
			if i == event and x[i] != None:
				x[i].append(func)
				break
		x[event] = [func]

	def rCmd(self, cmd, func, desc="None"):
		x = BOT.Commands
		for i in x.keys():
			if i == cmd:
				print "Can't add command %s, already exsists!" % (cmd)
				break
		x[cmd] = (func,desc)

	def __init__(self, auth=None):
		self.B = BOT
		self.Q = BOT.Q
		self.auth = auth
	def tester(self): print "TESTING! 1! 2! 3!"
	def say(self,msg): self.Q.rcon("say "+self.B.prefix+" ^2"+msg)
	def tell(self,uid,msg): self.Q.rcon("tell %s %s %s " % (uid, self.B.prefix, msg))
	def rcon(self,cmd):
		time.sleep(.8) #@DEV we need a better way of doing this!
		return self.Q.rcon(cmd)
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

def spawnEvent(Type, data): 
	if data['type'] in events.evez: 
		if data['type'] in BOT.Listeners: BOT.Listeners[data['type']]
		return events.evez[data['type']](data)

#---EVENTS--- (DEP ALL THESE!)#
def _suicide(vic, meth):
	obj = Event('suicide',(vic, meth))
	Listen('suicide', obj)
	return obj

def _kill(atk,vic,meth):
	obj = Event('kill',(atk,vic,meth))
	Listen('kill',obj)
	return obj

def _msg(sen,msg,iscmd=False):
	obj = Event('msg',(sen,msg,iscmd))
	Listen('msg',obj)
	return obj

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
			print >> sys.stderr, "ERROR LOADING %s: %s" % (name, e)

def parseUserInfo(inp):
	global BOT
	varz = {}
	m = inp.split("\\")
	uid = m[0].split(" ")[1]
	x = m[1]
	y = 1
	while len(x) > y:
		varz[x[y-1]] = x[y]
		y+=2
	BOT.Players[int(uid)] = player.Player(int(uid), varz)

def parseUserInfoChange(inp):
	global BOT
	varz = {}
	varz2 = {}
	m = inp.split(" ")
	x = m[2].split("\\")
	y = 1
	while len(x) > y:
		varz[x[y-1]] = x[y]
		y+=2
	BOT.Players[int(m[1])].name = varz['n']
	BOT.Players[int(m[1])].team = varz['t']

def parse(inp):
	global BOT
	if inp.startswith("say:"):
		newy = inp.split(':',2)
		nsender = newy[1]
		nmsg = newy[2].rstrip()
		ncmd1 = nmsg.strip(" ")
		ncmd = ncmd1.split(" ")[0]
		if ncmd.lower() in BOT.Commands:
			obj = _msg(nsender,nmsg,True)
			BOT.Commands[ncmd][0](obj)
	elif inp.startswith('ClientConnect:'):
		new = inp.split(":")[1].strip()
		_conn(new)
	elif inp.startswith('ClientUserinfo:'): 
		ret = parseUserInfo(inp)
		#@DEV Add UserInfo event here
	elif inp.startswith('ClientUserinfoChanged:'): 
		ret = parseUserInfoChange(inp)
		#@DEV Add InfoChange event here
	elif inp.startswith('Kill:'):
		newy = inp.split(" ")
		x = {}
		x['type'] = newy[8]
		x['victim'] = newy[6]
		x['attacker'] = newy[4]
		spawnEvent(x)
		
def loop():
	global proc, keepLoop
	# try:
	proc = subprocess.Popen('~/UrbanTerror/ioUrTded.i386 +set dedicated 2 +exec server.cfg', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	while True:
		if keepLoop is True:
			proc_read = proc.stdout.readline()
			if proc_read:
				print proc_read.rstrip()
				parse(proc_read)
		else:
			break
	return proc
	# except Exception, e:
	# 	print e
	# 	proc.kill()
	# 	sys.exit()

if __name__ == "__main__":
	load()
	loop()
