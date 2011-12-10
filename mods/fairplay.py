from init import A
import random

def cmdTeams(obj, f):
	msg = obj.data["msg"].split(" ")
	sender = obj.data["sender"]

	redPlayers = A.retrieveTeam('red')
	bluePlayers = A.retrieveTeam('blue')
	toTeam = 0
	fromTeam = None
	
	difference = abs(len(redPlayers) - len(bluePlayers))
	if difference <= 1:
		A.tell(sender, "Teams are already balanced.")
		return

	A.rcon('bigtext "AUTO-BALANCING TEAMS')

	if len(bluePlayers) > len(redPlayers):
		fromTeam = bluePlayers
		toTeam = 1
	elif len(redPlayers) > len(bluePlayers):
		fromTeam = redPlayers
		toTeam = 2
	
	while difference > 1:
		# pick a cid from fromTeam
		cid = random.choice(fromTeam)
		fromTeam.remove(cid)
		A.rcon("forceteam %s %s" % (cid, toTeam))
		difference -= 1
	
	A.say("Balanced teams.")

def init():
	A.addCmd('!teams', cmdTeams, "Attempt to balance uneven teams", 1)