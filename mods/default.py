import time, sys, const
from init import canInt, A, command, listener, __Version__
import database
from datetime import datetime, timedelta

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

@command('!test', 'Test Command', 0)
def tester(obj, t):
	print A.B.getStatus()
	print A.B.dumpUser(0)

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
	for c in A.getClients().values():
		A.tell(sender, "[%s] %s (%s)" % (c.uid, c.name, c.ip))

@command('!kick', 'Kick a user. Usage: !kick <player>', 3)
def cmdKick(obj, t):
	msg = obj.data["msg"].split(" ")
	sender = obj.data["sender"]
	if len(msg) == 1: A.tell(sender, "Usage: !kick <user>")
	elif len(msg) == 2:
		if msg[1].isdigit():
			kick = int(msg[1]) #@DEV This needs a check to see if players name is 0 or something annoying like that
		else:
			cli = A.findClient(msg[1])
			if cli != None:
				kick = cli.uid
		A.rcon('clientkick %d' % kick)

@command('!kickall', 'Kick everyone but yourself. Usage: !kickall', 4)
def cmdKickAll(obj, t):
	msg = obj.data["msg"].split(" ")
	sender = obj.data["sender"]
	for i in A.B.Clients.values():
		if i.uid != int(sender):
			A.kick(i.uid)

@command('!slap', 'Slap a player. Usage: !slap <NAME/UID>', 3)
def cmdSlap(obj, t):
	msg = obj.data["msg"].split(" ")
	sender = obj.data["sender"]
	if len(msg) == 1: A.tell(sender, "Usage: !slap <user> <count>")
	else:
		if msg[1].isdigit():
			slap = int(msg[1])
		else:
			cli = A.findClient(msg[1])
			if cli != None:
				slap = cli.uid
			else: return None
		count = 1
		if len(msg) == 3:
			if canInt(msg[2]): count = int(msg[2])
		for i in range(count):
			A.rcon('slap %d' % slap)
			time.sleep(.8)

@command('!nuke', 'Nuke a player. Usage: !nuke <NAME/UID>', 3)
def cmdNuke(obj, t):
	msg = obj.data["msg"].split(" ")
	sender = obj.data["sender"]
	if len(msg) == 1: A.tell(sender, "Usage: !nuke <user> <count>")
	else:
		if msg[1].isdigit():
			nuke = int(msg[1])
		else:
			cli = A.findClient(msg[1])
			if cli != None:
				nuke = cli.uid
		count = 1
		if len(msg) == 3:
			if canInt(msg[2]): count = int(msg[2])
		for i in range(count):
			A.rcon('nuke %d' % nuke)
			time.sleep(.8)

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

# Of course CLIENT_BEGIN has nothing to do with the client connect protocol. Frackin UrT.
@listener('CLIENT_CONNECTED')
def welcomeEvent(obj, t):
	time.sleep(8)
	A.say('Everyone welcome ^1%s ^3to the server!' % A.B.Clients[obj.data['client']].name)

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

@command('!ban', 'Ban a player. Usage: !ban <player> [reason]', 4)
def cmdBan(obj, t):
	#!ban Joey He's an idiot
	db = database.DB()
	db.tableSelect('clients')
	msg = obj.data["msg"].split(" ", 2)
	sender = obj.data['sender']
	senderobj = A.findClient(sender)
	ctime = datetime.now()

	if len(msg) == 2: #!ban joey
		reason = 'No Reason Given'
	elif len(msg) == 3: #!ban joey my special reason
		reason = msg[2].strip()
	else: A.tell(sender, 'Usage: !ban <player> [reason]')

	if 1 < len(msg) < 4:
		banr = A.findClient(msg[1])
		if banr != None:
			banrdb = db.rowFind(banr.cid)
			db.tableSelect('penalties')
			db.rowCreate({'userid':banr.cid, 'adminid':senderobj.cid, 'type':'ban', 'reason':reason, 'time':ctime, 'expiration':-1, 'status':1})
			db.commit()
			A.kick(banr.uid)
			A.tell(sender, 'Banned %s!' % banr.name)
		else:
			A.tell(sender, 'No users matching %s' % msg[1])

@command('!tempban', 'Temporarily ban a player. Usage: !tempban <player> <duration> [reason]', 3)
def cmdTempBan(obj, t): 
	#!tempban Joey length reason
	db = database.DB()
	db.tableSelect('clients')
	msg = obj.data["msg"].split(" ", 3)
	sender = obj.data['sender']
	senderobj = A.findClient(sender)

	if len(msg) == 3: #!ban joey
		reason = 'No Reason Given'
	elif len(msg) == 4: #!ban joey my special reason
		reason = msg[2].strip()
	else: A.tell(sender, 'Usage: !tempban <player> <duration> [reason]')

	if 1 < len(msg) < 5:
		ctime = datetime.now()
		etime = datetime(ctime.year, ctime.month, ctime.day, ctime.hour, ctime.minute, ctime.second) + timedelta(minutes=const.timeparse(msg[2]))
		exptime = time.mktime(etime.timetuple())
		banr = A.findClient(msg[1])
		if banr != None:
			banrdb = db.rowFind(banr.cid)
			db.tableSelect('penalties')
			db.rowCreate({'userid':banr.cid, 'adminid':senderobj.cid, 'type':'tempban', 'reason':reason, 'time':ctime, 'expiration':exptime, 'status':1})
			db.commit()
			A.tell(banr.uid, 'Temp Banned tell %s' % etime.__str__())
			A.kick(banr.uid)
			A.tell(sender, 'Temp Banned %s tell %s!' % (banr.name, etime.__str__()))
	else: A.tell(sender, 'Usage: !tempban <player> <duration> [reason]')

@command('!unban', 'Unban a temp, or permabanned player. Usage: !unban <player>', 3)
def cmdUnBan(obj, t):
	#!unban blah
	db = database.DB()
	db.tableSelect('clients')
	sender = obj.data['sender']
	senderobj = A.findClient(sender)
	msg = obj.data["msg"].split(" ", 1)
	rid = None

	if len(msg) == 2:
		if msg[0].isdigit():
			rid = int(msg[0])
		else:
			entr = db.rowFindAll(msg[1], 'nick')
			print db.rowsGetAll()
			if entr == None:
				A.tell(sender, 'Couldnt find a ban for user with nickname %s' % msg[1])
			elif len(entr) > 1:
				A.tell(sender, 'Multiple users found... listing...')
				if len(entr) <= 15:
					for i in entr:
						objz = A.findClient(i)
						A.tell(sender, '[%s] %s' % (objz.cid, objz.name))
				else:
					A.tell(sender, 'Too many (<15) users to list...')
			elif len(entr) == 1:
				rid = entr['id']
		
		if rid != None:
			objz = A.findClient(rid)
			db.tableSelect('penalties')
			entr = db.rowFindAll(rid, 'userid')
			if entr is None:
				return A.tell(sender, 'No bans found for userid %s' % rid)
			elif len(entr) == 1:
				entr[0]['status'] = 0
				db.rowUpdate(entr[0])
			elif len(entr) > 1:
				for i in entr:
					if i['type'] in ('ban', 'tempban'):
						r = db.rowFind(i['id'])
						r['status'] = 0
						db.rowUpdate(r)
			db.commit()
			A.tell(sender, 'Unbanned %s' % objz.name)
	else:
		return A.tell(sender, 'Usage: !unban <player>')

@command('!loadout', 'See a players loadout. Usage: !loadout <player>', 3)
def cmdLoadout(obj, t):
	msg = obj.msg.split(' ', 1)
	m = []
	if len(msg) == 2:
		usr = A.findClient(msg[1])
		if usr != None:
			A.B.Clients[usr.uid].updateData(A.B.dumpUser(usr.uid))
			A.tell(obj.sender, 'Loadout for %s:' % A.B.Clients[usr.uid].name)
			for i in A.B.Clients[usr.uid].gear:
				A.tell(obj.sender, '%s' % const.gearInfo[i]['name'])
		else:
			A.tell(obj.sender, 'Unknown user %s' % msg[1])
	else:
		A.tell(obj.sender, 'Usage: !loadout <player>')

def cmdIDDQD(obj, t):
	sender = obj.data['sender']
	client = A.getClient(sender)

	db = database.DB()
	db.tableSelect("clients")
	entry = db.rowFind(client.cl_guid, 'guid')
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
