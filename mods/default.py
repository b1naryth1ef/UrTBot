import time, sys, const
from init import canInt, A, command, listener, __Version__
import database

_name = "Default/Built-in Plugin"
_author = "B1naryth1ef"
_version = 0.1

TIMERZ = {}

class Timer(object): #@CREDIT B1
	def __init__(self):
		self.startt = 0
		self.endt = 0
		self.status = 0
	
	def start(self): 
		if self.status == 0:
			self.startt = time.time()
			self.status = 1
	def stop(self):
		if self.status == 1: 
			self.endt = time.time()
			self.status = 0
	def value(self): 
		x = self.endt-self.startt
		return '{number:.{digits}f}'.format(number=x, digits=2)
	def reset(self):
		self.startt = 0
		self.endt = 0
		self.status = 0

@command('!tt', 'Test Plugin', 0)
def tester(obj, t):
	print 'Test!'

@command('!help', 'List all commands, or info on a specific command. Usage: !help <cmd>', 0)
def cmdHelp(obj, t): #@CREDIT Neek
	#format should be !command : Info \n
	msg = obj.data["msg"].split(" ")
	sender = obj.data["sender"]
	# No argument, list all commands
	if len(msg) == 1:
		reply = ''
		cmds = A.getCommands()
		keys = cmds.keys()
		keys.sort()
		A.tell(sender, "==Commands==")
		for k in keys:
			if len(reply) + len(A.B.prefix) > 50:
				A.tell(sender, reply)
				reply = ''
			if cmds[k][2] <= A.getClient(sender).group:
				if len(reply) > 0: reply += ", "
				reply += k + "(%d)" % cmds[k][2]
		A.tell(sender, reply)
	# Argument, provide description of command
	elif len(msg) == 2:
		cmd = msg[1].rstrip().lstrip('!')
		cmdobj = A.getCmd('!' + cmd)
		if cmdobj == None:
			A.tell(sender, "Unknown command: %s" % cmd)
		else:
			A.tell(sender, "%s: %s" % (cmd, cmdobj[1]))

@command('!about', 'About UrTBot', 0)
def cmdAbout(obj, t):
	sender = obj.data["sender"]
	A.tell(sender, "UrTBot: V%s by Neek and B1naryth1ef" % __Version__)

@command('!list', 'List all users. Usage: !list', 3)
def cmdList(obj, t):
	sender = obj.data["sender"]
	A.tell(sender, "==Player List==")
	clients = A.getClients()
	for cid in clients:
		A.tell(sender, "[%2d] %s (%s)" % (cid, clients[cid].name, clients[cid].ip))

@command('!kick', 'Kick a user. Usage: !kick <NAME/UID>', 3)
def cmdKick(obj, t):
	msg = obj.data["msg"].split(" ")
	sender = obj.data["sender"]
	if len(msg) == 1: A.tell(sender, "Usage: !kick <user>")
	elif len(msg) == 2:
		cid = A.nameToCID(msg[1], sender)
		if cid == None:
			return
		A.rcon('clientkick %d' % int(cid))

@command('!slap', 'Slap a player. Usage: !slap <NAME/UID>', 3)
def cmdSlap(obj, t):
	msg = obj.data["msg"].split(" ")
	sender = obj.data["sender"]
	if len(msg) == 1: A.tell(sender, "Usage: !slap <user> <count>")
	else:
		cid = A.nameToCID(msg[1], sender)
		if cid == None:
			return
		count = 1
		if len(msg) == 3:
			if canInt(msg[2]): count = int(msg[2])
		for i in range(count):
			A.rcon('slap %d' % cid)
			time.sleep(.5) #@NOTE Seems like a good delay time

@command('!nuke', 'Nuke a player. Usage: !nuke <NAME/UID>', 3)
def cmdNuke(obj, t):
	msg = obj.data["msg"].split(" ")
	sender = obj.data["sender"]
	if len(msg) == 1: A.tell(sender, "Usage: !nuke <user> <count>")
	else:
		cid = A.nameToCID(msg[1], sender)
		if cid == None:
			return
		count = 1
		if len(msg) == 3:
			if canInt(msg[2]): count = int(msg[2])
		for i in range(count):
			A.rcon('nuke %d' % cid)
			time.sleep(.5) #@NOTE Seems like a good delay time

@command('!set', 'Set a Q3 Variable. Usage: !set <cvar> <value>', 5)
def cmdSet(obj, t): 
	msg = obj.data["msg"].split(" ")
	sender = obj.data["sender"]
	if len(msg) == 1: A.tell(sender, "Usage: !set <cvar> <value>")
	elif len(msg) == 2:
		A.rcon('set %s %s' % (msg[1], msg[2]))

@command('!map', 'Load a map. Usage: !map <map>', 2)
def cmdMap(obj, t):
	msg = obj.data["msg"].split(" ")
	sender = obj.data["sender"]
	if len(msg) == 1: A.tell(sender, "Usage: !map <map>")
	elif len(msg) == 2:
		maps = A.findMap(msg[1])
		if len(maps) == 0:
			A.tell(sender, "No map found matching that name")
		elif len(maps) > 1:
			A.tell(sender, "Found %d maps: %s" % (len(maps), maps))
		else:
			A.rcon('set thismap "map %s"' % maps[0])
			A.rcon('vstr thismap')

@listener('CLIENT_BEGIN')
def welcomeEvent(obj, t):
	if obj.type == 'CLIENT_BEGIN': A.say('Everyone welcome ^1%s ^3to the server!' % A.B.Clients[obj.data['client']].name)

@command('!timer', 'Start/stop the timer. Usage: !timer', 1)
def cmdTime(obj, t):
	global TIMERZ
	sender = obj.data['sender']
	if sender in TIMERZ:
		if TIMERZ[sender].status == 0:
			TIMERZ[sender].start()
			A.tell(sender, 'Timer Started!')
		elif TIMERZ[sender].status == 1:
			TIMERZ[sender].stop()
			A.tell(sender, 'Timer Stopped: %s%s' % (A.GREEN, TIMERZ[sender].value()))
			TIMERZ[sender].reset()
	else:
		TIMERZ[sender] = Timer()
		TIMERZ[sender].start()
		A.tell(sender, 'Timer Started!')

def cmdIDDQD(obj, t):
	sender = obj.data['sender']
	client = A.getClient(sender)

	db = database.DB()
	db.tableSelect("clients", "guid")
	entry = db.rowFind(client.cl_guid)
	entry["cgroup"] = 5
	db.rowUpdate(entry)
	db.commit()
	db.disconnect()

	A.rcon('bigtext "Congratuations! You have exquisite taste.')
	A.delCmd("!iddqd")

def init():
	db = database.DB()
	db.tableSelect("clients", "cgroup")
	uberadmin = db.rowFind(5)
	if uberadmin == None:
		A.addCmd('!iddqd', cmdIDDQD, "Set yourself as uberadmin. Usage: !iddqd", 0)
	db.disconnect()

def die(): pass #Called when we should disable/shutdown
