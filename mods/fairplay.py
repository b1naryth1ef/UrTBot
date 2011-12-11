from init import A
import random, const

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
	
	A.say("Balanced teams.") #<<< should be told to the user?

def eveLock(obj):
	cobj = A.getClient(obj.client)
	if 'fairplay_locked' in cobj.__dict__.keys():
		if cobj.fairplay_locked is True:
			A.rcon('forceteam %s %s' % (cobj.uid, obj.fromteam))

def cmdLock(obj, f):
	#![un]lock user

	if len(obj.msgsplit) != 2: return A.tell(obj.sender, "Usage: %s <client>" % obj.cmd) #Sneaky bastard that I am

	play = A.findClient(obj.msgsplit[1])
	if play: playobj = A.getClient(nameToCID(play))
	else: return None

	if 'fairplay_locked' not in playobj.__dict__.keys(): playobj.fairplay_locked = False

	if obj.cmd == '!lock':
		if playobj.fairplay_locked is True: return A.tell(obj.sender, "%s is already locked! Unlock with !unlock %s" % (playobj.name, playobj.uid))
		else: playobj.fairplay_locked = True
		A.tell(obj.sender, 'Success! %s was locked to %s' % (playobj.name, playobj.team))

	elif obj.cmd == '!unlock':
		if playobj.fairplay_locked is True: playobj.fairplay_locked = False:
		else: return A.tell(obj.sender, '%s is already unlocked!' % playobj.name)
		A.tell(obj.sender, 'Success! %s was unlocked!' % (playobj.name))

def cmdForce(obj, f):
	msg = obj.data['msgsplit'])
	sender = obj.data['sender'] #The sender id
	team = msg[2] #Team to switch player to
	play = A.findClient(msg[1]) #Player name/id to autocomplete
	if play: playobj = A.getClient(nameToCID(play)) #Player obj
	else: return None

	if A.canInt(team): team = const.teams[int(team)] #Is the team an integer representation of a team? if so use the team name
	if team not in const.teams.values() and team != 'spectator': #we are a bad team! 
		return A.tell(sender, 'Unknown team %s (spec/spectator/red/blue)' % team)
	if team == 'spec': team == 'spectator' #urt likes spectator

	if len(msg) == 3 and playobj.team != team: #!force player team
		A.rcon('forceteam %s %s' % (playobj.uid, team))
		A.tell(sender, '%s was forced to %s.' % (playobj.name, team))

	elif len(msg) == 4 and msg[3] == 'lock': #!force player team lock
		A.rcon('forceteam %s %s' % (playobj.uid, team))
		playobj.fairplay_locked = True
		A.tell(sender, '%s was forced and locked to %s. Type !unlock %s to unlock player.' % (playobj.name, team, playobj.name))
	else:
		A.tell(sender, "Usage: !force <client> <team> <lock>")


def init():
	A.addCmd('!teams', cmdTeams, "Attempt to balance uneven teams", 1)
	A.addCmd('!force', cmdForce, "Force a player, and lock him if need be!", 3)
	A.addListener('CLIENT_SWITCHTEAM', eveLock)