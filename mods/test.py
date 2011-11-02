import time, sys

_name = "Default/Built-in Plugin"
_author = "B1naryth1ef"
_version = 0.1

def cmdHelp(obj): pass
def cmdList(obj): pass
def cmdSlap(obj): pass
def cmdSet(obj): pass
def cmdMap(obj): pass
def cmdStop(obj): pass
def cmdRestart(obj): pass

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
