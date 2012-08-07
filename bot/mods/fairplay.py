from bot.config_handler import ConfigFile
from bot.main import BOT
from bot.api import listener, Event, command, A, Q3
import bot.const as const
import sys, os, time
import random

default_config = {
    'points_default':{
    	'hit':15,
    	'kill':100,
    	'max':300,
    },
    'groups':{
    	1:{'max': 300},
    	2:{'max': 400},
    	3:{'max': 500},
    	4:{'max': -1},
    	5:{'max': -1},
    	6:{'max': -1}
    },
    'warn_msg':'Do not attack teamates!'
}

config = ConfigFile(os.path.join(A.configs_path, 'fairplay.cfg'), default=default_config)

def getPlayerContainer(plyr):
	if not hasattr(plyr, 'points_container'):
		plyr.points_container = PointsContainer(plyr)
	return plyr.points_container

def getPoints(plyr):
	grp = BOT.config.groups[plyr.group]
	maxlvl = max([grp['maxlevel']]+grp['levels'])
	if maxlvl in config.groups.keys():
		res = {}
		for i in ['max', 'hit', 'kill']:
			if i not in config.groups[maxlvl].keys():
				res[i] = config.points_default[i]
		res.update(config.groups[maxlvl])
		return res
	else: return config.points_default

class PointsContainer(): #@FIXME Internals suck
	def __init__(self, player):
		self.player = player
		self.points = 0

		self.q = getPoints(player)
		self.tier = [i for i in range(0, self.q['max']/3)]
		self.msgs = [False, False, False]

	def addPoints(self, amount, warning):
		self.points += amount
		addpoints.fire({'client':self.player, 'amount':amount, 'reason':warning})
		if self.points >= self.tier[self.msgs.index(False)]:
			player.tell('Warning %s of 3: %s' % (self.msgs.index(False), warning))
			self.msgs[self.msgs.index(False)] = True
			if not False in self.msgs:
				player.kick('Too many warnings!') #@TODO Fix this up so we can clear users etc

addpointsaction = Event('PLUGIN_FAIRPLAY_ACTION_ADDPOINTS')
addpoints = Event('PLUGIN_FAIRPLAY_ADDPOINTS')

@listener(addpointsaction)
def addPointsListener(obj):
	getPlayerContainer(obj['client']).addPoints(obj.amount, obj.reason)

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