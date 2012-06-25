from bot.main import BOT
from bot.api import listener, Event, command, A, Q3
import bot.const as const
import random

@command('!teams', "Attempt to balance uneven teams", "", level=2)
def cmdTeams(obj, t):
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

def init(a, b): pass
def run(): pass