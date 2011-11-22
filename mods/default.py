import time, sys, const

_name = "Default/Built-in Plugin"
_author = "B1naryth1ef"
_version = 0.1

def cmdHelp(obj):
	#format should be !command : Info \n
	msg = obj.data["msg"].split(" ")
	sender = obj.data["sender"]
	# No argument, list all commands
	if len(msg) == 1:
		reply = ''
		cmds = api.getCmd()
		keys = cmds.keys()
		keys.sort()
		api.tell(sender, "==Commands==")
		for k in keys:
			if len(reply) + len(api.B.prefix) > 50:
				api.tell(sender, reply)
				reply = ''
			if len(reply) > 0: reply += ", "
			reply += k
		api.tell(sender, reply)
	# Argument, provide description of command
	elif len(msg) == 2:
		cmd = msg[1].rstrip().lstrip('!')
		cmdobj = api.getCmd('!' + cmd)
		if cmdobj == None:
			api.tell(sender, "Unknown command: %s" % cmd)
		else:
			api.tell(sender, "%s: %s" % (cmd, cmdobj[1]))
def cmdList(obj): pass
	#Format should be !command, !othercommand, !otherothercommand, etc
def cmdSlap(obj): pass
	#Format should be !slap int or !slap name/partial name (Use regex?)
def cmdSet(obj): pass
	#Format should be !set variable value
def cmdMap(obj): pass
	#format should be !map map gamemode(Or none)
def cmdStop(obj): pass
	#format should be !stop
def cmdRestart(obj): pass
	#format should be !restart (Both bot/server)
def cmdLoadout(obj): pass
	#format should be !loadout int, or playername (regex?)
def cmdTester(obj):
	api.say('Testing! This is just a test! Stay clam!')
	api.reboot()
def testEvent(obj):
	time.sleep(5)
	api.say('TESTING 1... 2... 3...')
def cmdTime(obj):
	global time1, time2
	if obj.data['msg'].startswith('!tstart'):
		time1 = time.time()
		api.say('Timer started!')
	elif obj.data['msg'].startswith('!tstop'):
		time2 = time.time()
		api.say('Timer Stopped!')
		time.sleep(.6)
		api.say('Timer: %s%s' % (api.BLUE, time2-time1))
		time1 = None
		time2 = None

def testPlugin(obj):
	if obj == 'init':
		pass #setup stuff
	elif obj.type == "GAME_FLAGPICKUP":
		pass
	elif obj.type == "GAME_FLAGDROP":
		pass
	elif obj.type == "GAME_FLAGRETURN":
		pass
	

def init(A):
	global api
	api = A
	api.addCmd('!help', cmdHelp, "List all commands")
	api.addCmd('!list', cmdList, "List all users (with UID's)")
	api.addCmd('!slap', cmdSlap, "Slap a player")
	api.addCmd('!set', cmdSet, "Set a Q3 Variable")
	api.addCmd('!map', cmdMap, "Load a map")
	api.addCmd('!stop', cmdStop, "Stop the server/bot")
	api.addCmd('!restart', cmdRestart, "Restart the server/bot")
	api.addCmd('!loadout', cmdLoadout, "See a players loadout")
	api.addCmd('!test', cmdTester, ">:D")
	api.addCmd('!tstart', cmdTime, "Start the timer")
	api.addCmd('!tstop', cmdTime, "Stop the timer")
	api.addEvent('CLIENT_CONNECT', testEvent)

def die(): pass #Called when we should disable/shutdown
