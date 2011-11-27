import time, sys, const

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
		cmds = api.getCommands()
		keys = cmds.keys()
		keys.sort()
		api.tell(sender, "==Commands==")
		for k in keys:
			if len(reply) + len(api.B.prefix) > 50:
				api.tell(sender, reply)
				reply = ''
			if cmds[k][2] <= api.getClient(sender).group:
				if len(reply) > 0: reply += ", "
				reply += k + "(%d)" % cmds[k][2]
		api.tell(sender, reply)
	# Argument, provide description of command
	elif len(msg) == 2:
		cmd = msg[1].rstrip().lstrip('!')
		cmdobj = api.getCmd('!' + cmd)
		if cmdobj == None:
			api.tell(sender, "Unknown command: %s" % cmd)
		else:
			api.tell(sender, "%s: %s" % (cmd, cmdobj[1]))

def cmdList(obj):
	sender = obj.data["sender"]
	api.tell(sender, "==Player List==")
	for client in api.B.Clients.values():
		api.tell(sender, "[%s] %s (%s)" (client.uid, client.name, client.team))

def cmdSlap(obj):
	msg = obj.data["msg"].split(" ")
	sender = obj.data["sender"]
	if len(msg) == 1: api.tell(sender, "Usage: !slap <user>")
	elif len(msg) == 2: api.rcon('slap %s' % (msg[1]))

def cmdSet(obj): 
	msg = obj.data["msg"].split(" ")
	sender = obj.data["sender"]
	if len(msg) == 1: api.tell(sender, "Usage: !set <cvar> <value>")
	elif len(msg) == 2:
		api.rcon('set %s %s' % (msg[1], msg[2]))

def cmdMap(obj):
	msg = obj.data["msg"].split(" ")
	sender = obj.data["sender"]
	if len(msg) == 1: api.tell(sender, "Usage: !map <map>")
	elif len(msg) == 2:
		api.rcon('map %s' % (msg[1]))

def cmdStop(obj): api.exitProc()
def cmdRestart(obj): pass
def cmdLoadout(obj): pass

def cmdTester(obj):
	api.say('Testing! This is just a test! Stay clam!')
	api.reboot() # lol, so this is why !test crashes! :D

def welcomeEvent(obj): pass
#	time.sleep(5)
#	try:
#		api.say('Everyone welcome %s to the server!' % api.B.Clients[obj.data['client']].name)
#	except:
#		welcomeEvent(obj)

def cmdTime(obj):
	global TIMERZ
	sender = obj.data['sender']
	if sender in TIMERZ:
		if TIMERZ[sender].status == 0:
			TIMERZ[sender].start()
			api.tell(sender, 'Timer Started!')
		elif TIMERZ[sender].status == 1:
			TIMERZ[sender].stop()
			api.tell(sender, 'Timer Stopped: %s%s' % (api.GREEN, TIMERZ[sender].value()))
			TIMERZ[sender].reset()
	else:
		TIMERZ[sender] = Timer()
		TIMERZ[sender].start()
		api.tell(sender, 'Timer Started!')
	
def init(A):
	global api
	api = A

	api.addCmds([['!help', cmdHelp, "List all commands, or info on a specific command. Usage: !help <cmd>", 0], 
	['!list', cmdList, "List all users. Usage: !list", 0],
	['!slap', cmdSlap, "Slap a player. Usage: !slap <NAME/UID>", 3],
	['!set', cmdSet, "Set a Q3 Variable. Usage: !set <cvar> <value>", 0],
	['!map', cmdMap, "Load a map. Usage: !map <map>", 0],
	['!stop', cmdStop, "Stop the server/bot. Usage: !stop", 0],
	['!restart', cmdRestart, "Restart the server/bot. Usage: !restart", 0],
	['!loadout', cmdLoadout, "See a players loadout. Usage: !loadout <NAME/UID>", 0],
	['!test', cmdTester, ">:D", 0],
	['!timer', cmdTime, "Start/stop the timer. Usage: !timer", 0],
	])

	api.addListener('CLIENT_CONNECT', welcomeEvent)

def die(): pass #Called when we should disable/shutdown
