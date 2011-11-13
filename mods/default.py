import time, sys

_name = "Default/Built-in Plugin"
_author = "B1naryth1ef"
_version = 0.1

def cmdHelp(obj): pass
	#format should be !command : Info \n
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
	global api
	for client in api.B.Clients:
		print client.uid,":",client.name,":",client.ip
		print client.gear

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
	api.addCmd('!loadout', cmdRestart, "See a players loadout")
	api.addCmd('!test', cmdTester, ">:D")

def die(): pass #Called when we should disable/shutdown