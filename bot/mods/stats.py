from bot.config_handler import ConfigFile
from bot.main import BOT
from bot.api import listener, Event, command, A, Q3
from bot.debug import log
import bot.database as database
import bot.const as const
import sys, os, time

def parseKill(obj, f): pass
	#A.B.Clients[obj.atk]
	atk = A.getClient(obj.atk)
	atkClient = db.rowFind(atk.cid) #<<< see player.py for note on what cid should be
	atkClient["kills"] += 1
	db.rowUpdate(atkClient)
	db.commit()

def parseDeath(obj, f):
	vic = A.getClient[obj.vic]
	vicClient = db.rowFind(vic.cid)
	vicClient["deaths"] += 1
	db.rowUpdate(vicClient)
	db.commit()

def parseSuicide(obj, f): pass
def parseTeamKill(obj, f): pass

def eventHandler(obj, f):
	if obj.type == 'CLIENT_KILL': parseKill(obj)
	elif obj.type == 'CLIENT_SUICIDE': parseSuicide(obj)
	elif obj.type == 'CLIENT_GENERICDEATH': parseDeath(obj)
	elif obj.type == 'CLIENT_WORLDDEATH': parseDeath(obj)
	elif obj.type == 'CLIENT_SUICIDE': parseDeath(obj)
	elif obj.type == 'CLIENT_TEAMKILL': parseTeamKill(obj)

def onEnable(): pass
def onDisable(): pass
def onBoot(): pass