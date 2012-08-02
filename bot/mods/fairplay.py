from bot.config_handler import ConfigFile
from bot.main import BOT
from bot.api import listener, Event, command, A, Q3
import bot.const as const
import sys, os, time
import random

default_config = {
    'max_points':300,
    'points':{
    	0:{
    		'hit':35,
    		'kill':100,
    	},
    	1:{
    		'hit':30,
    		'kill': 90,
    	},
    	2:{
    		'hit':25,
    		'kill': 80,
    	},
    	3:{
    		'hit':15,
    		'kill': 40,
    	},
    	4:{
    		'hit': 5,
    		'kill': 10,
    	},
    	5:{
    		'hit': 0,
    		'kill': 0,
    	}
    }
}

config = ConfigFile(os.path.join(A.configs_path, 'fairplay.cfg'), default=default_config)

@command('teams', 'Even out the teams', '', 1)
def cmdTeams(obj): #@TODO Factor locked players in?
	m = obj.msg.split(" ")

	redPlayers = [i.cid for i in BOT.Clients.values() if i.team == const.RED_TEAM]
	bluePlayers = [i.cid for i in BOT.Clients.values() if i.team == const.BLUE_TEAM]
	
	diff = abs(len(redPlayers) - len(bluePlayers))
	if diff <= 1:
		return obj.client.tell('Teams are already balanced!')

	Q3.say('Balancing teams!')
	toteam = const.BLUE_TEAM if len(bluePlayers) < len(redPlayers) else const.RED_TEAM
	fromteam = redPlayers if toteam == const.BLUE_TEAM else bluePlayers

	while diff > 1:
		cid = random.choice(fromTeam)
		fromteam.pop(fromteam.index(cid))
		Q3.R("forceteam %s %s" % (cid, toTeam.urt))
		diff -= 1
	
	Q3.say("Teams have been balenced!")

@command('lock', "Lock a user to a team.", "{user}", level=4)
def cmdLock(obj):
	m = obj.msg.split(' ')
	if len(m) == 2:
		o = Q3.getObj(m[1], obj.client)
		if not o: return
		if getattr(obj.client, 'locked', False):
			obj.client.tell('Client is already locked too %s!' % (o.team))
		else:
			obj.client.locked = obj.client.team
			obj.client.tell('Client has been locked too %s!' % (o.team))
	else:
		obj.usage()

@command('unlock', "Unlock a user from a team.", "{user}", level=4)
def cmdUnlock(obj):
	m = obj.msg.split(' ')
	if len(m) == 2:
		o = Q3.getObj(m[1], obj.client)
		if not o: return
		if getattr(obj.client, 'locked', False):
			obj.client.locked = None
			obj.client.tell('Client has been unlocked from %s!' % (o.team))
		else:
			obj.client.tell('Client isnt locked to a team!')
	else:
		obj.usage()

@listener('CLIENT_TEAM_SWITCH')
def clientTeamSwitchListener(obj):
	if getattr(obj.client, 'locked', False):
		obj.client.force(obj.client.locked.urt)

@listener('CLIENT_CONN_DC')
def clientDisconnectListener(obj):
	obj.client.force = None

@listener('CLIENT_KILL_TK')
def clientKillTkListener(obj):
	if not hasattr(obj.client, points):
		obj.client.points = 0
	if obj.client.user.group in config.points:
		obj.client.points += config.points[obj.client.user.group]['kill']
		obj.client.tell("%s more points before you get kicked!") #@TODO Better text and coloring

#@TODO add hit listener, messages etc

def onEnable(): pass
def onDisable(): pass
def onBoot(): pass