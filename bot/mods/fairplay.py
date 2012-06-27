from bot.main import BOT
from bot.api import listener, Event, command, A, Q3
import bot.const as const
import random

locks = []

@command('teams', "Attempt to balance uneven teams", "", level=2)
def cmdTeams(obj):
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
		if o not in locks:
			locks.append(o)
			return obj.client.tell('Client has been locked too %s!' % (o.team))
		obj.client.tell('Client is already locked too %s!' % (o.team))
	else:
		obj.usage()

@command('unlock', "Unlock a user from a team.", "{user}", level=4)
def cmdUnlock(obj):
	m = obj.msg.split(' ')
	if len(m) == 2:
		o = Q3.getObj(m[1], obj.client)
		if not o: return
		if o in locks:
			locks.pop(locks.index(o))
			return obj.client.tell('Client has been unlocked from %s!' % (o.team))
		obj.client.tell('Client isnt locked to a team!')
	else:
		obj.usage()

@listener('CLIENT_TEAM_SWITCH')
def clientTeamSwitchListener(obj):
	if obj.client in locks:
		obj.client.force(locks.index(obj.client).team)

@listener('CLIENT_CONN_DISCONNECT')
def clientDisconnectListener(obj):
	if obj.client in locks:
		locks.pop(locks.index(obj.client))

def onEnable(): pass
def onDisable(): pass
def onBoot(): pass