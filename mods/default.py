import time, sys, const
from init import canInt, A

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

def cmdHelp(obj): #@CREDIT Neek
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

def cmdList(obj):
	sender = obj.data["sender"]
	A.tell(sender, "==Player List==")
	clients = A.getClients()
	for cid in clients:
		A.tell(sender, "[%2d] %s (%s)" % (cid, clients[cid].name, clients[cid].ip))

def cmdSlap(obj):
	msg = obj.data["msg"].split(" ")
	sender = obj.data["sender"]
	if len(msg) == 1: A.tell(sender, "Usage: !slap <user> <count>")
	elif len(msg) == 2: A.rcon('slap %s' % (msg[1]))
	elif len(msg) == 3:
		if canInt(msg[2]):
			for i in range(int(msg[2])):
				A.rcon('slap %s' % (msg[1]))
				time.sleep(.5) #@NOTE Seems like a good delay time

def cmdNuke(obj):
	msg = obj.data["msg"].split(" ")
	sender = obj.data["sender"]
	if len(msg) == 1: A.tell(sender, "Usage: !nuke <user> <count>")
	elif len(msg) == 2: A.rcon('nuke %s' % (msg[1]))
	elif len(msg) == 3:
		if canInt(msg[2]):
			for i in range(int(msg[2])):
				A.rcon('nuke %s' % (msg[1]))
				time.sleep(.5) #@NOTE Seems like a good delay time

def cmdSet(obj): 
	msg = obj.data["msg"].split(" ")
	sender = obj.data["sender"]
	if len(msg) == 1: A.tell(sender, "Usage: !set <cvar> <value>")
	elif len(msg) == 2:
		A.rcon('set %s %s' % (msg[1], msg[2]))

def cmdMap(obj):
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

def cmdStop(obj): A.exitProc()
def cmdRestart(obj): pass
def cmdLoadout(obj): pass

def cmdTester(obj):
	A.say('Testing! This is just a test! Stay clam!')
	A.reboot() # lol, so this is why !test crashes! :D

def welcomeEvent(obj): pass
#	time.sleep(5)
#	try:
#		A.say('Everyone welcome %s to the server!' % A.B.Clients[obj.data['client']].name)
#	except:
#		welcomeEvent(obj)

def cmdTime(obj):
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
	
def init():
	A.addCmds([['!help', cmdHelp, "List all commands, or info on a specific command. Usage: !help <cmd>", 0], 
	['!list', cmdList, "List all users. Usage: !list", 3],
	['!slap', cmdSlap, "Slap a player. Usage: !slap <NAME/UID>", 3],
	['!nuke', cmdNuke, "Nuke a player. Usage: !nuke <NAME/UID>", 3],
	['!set', cmdSet, "Set a Q3 Variable. Usage: !set <cvar> <value>", 5],
	['!map', cmdMap, "Load a map. Usage: !map <map>", 2],
	['!stop', cmdStop, "Stop the server/bot. Usage: !stop", 0],
	['!restart', cmdRestart, "Restart the server/bot. Usage: !restart", 0],
	['!loadout', cmdLoadout, "See a players loadout. Usage: !loadout <NAME/UID>", 0],
	['!test', cmdTester, ">:D", 0],
	['!timer', cmdTime, "Start/stop the timer. Usage: !timer", 0],
	])

	A.addListener('CLIENT_CONNECT', welcomeEvent)

def die(): pass #Called when we should disable/shutdown
