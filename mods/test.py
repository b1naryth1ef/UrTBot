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

def init(A):
	global api
	api = A
	api.rCmd('!help', cmdHelp, "List all commands")
	api.rCmd('!list', cmdList, "List all users (with UID's)")
	api.rCmd('!slap', cmdSlap, "Slap a player")
	api.rCmd('!set', cmdSet, "Set a Q3 Variable")
	api.rCmd('!map', cmdMap, "Load a map")
	api.rCmd('!stop', cmdStop, "Stop the server/bot")
	api.rCmd('!restart', cmdRestart, "Restart the server/bot")
	api.rCmd('!loadout', cmdRestart, "See a players loadout")
