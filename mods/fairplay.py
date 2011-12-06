from init import A
import random

def cmdTeams(obj, f):
	msg = obj.data["msg"].split(" ")
	sender = obj.data["sender"]

	redPlayers = []
	bluePlayers = []
	toTeam = 0
	fromTeam = None

	# sort players into two lists, redPlayers & bluePlayers
	clients = A.getClients()
	for client in clients:
		if clients[client].team != None:
			if clients[client].team == 1: redPlayers.append(client)
			elif clients[client].team == 2: bluePlayers.append(client)

	difference = abs(len(redPlayers) - len(bluePlayers))
	if difference <= 1:
		A.tell(sender, "Teams are not uneven.")
		return

	if len(bluePlayers) > len(redPlayers):
		fromTeam = bluePlayers
		toTeam = 1
	elif len(redPlayers) > len(bluePlayers):
		fromTeam = redPlayers
		toTeam = 2
	
	while difference > 1:
		# pick a cid from fromTeam
		cid = random.choice(fromTeam)
		A.rcon("forceteam %s %s" % (cid, toTeam))
		difference -= 1
	
	A.say("Balanced teams.")

def init():
	A.addCmd('!teams', cmdTeams, "Attempt to balance uneven teams", 1)