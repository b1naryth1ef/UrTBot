from init import A
from database import handler

def parseSkill(obj): pass

def parseKill(obj, tk=False):
	#A.B.Clients[obj.atk]
	atk = A.B.Clients[obj.atk]
	atkClient = T.searchEntries(atk.cid) #<<< see player.py for note on what cid should be
	atkClient.kills += 1
	if tk: atkClient.tks += 1
	atk.Client.score = parseSkill(atkClient)

	atkClient.commit()

def parseDeath(obj):
	vic = A.B.Clients[obj.vic]
	vicClient = T.searchEntries(vic.cid)
	vicClient.deaths += 1
	vicClient.commit()

def parseSuicide(obj): pass
def parseTeamKill(obj): pass

def eventHandler(obj):
	if obj.type == 'CLIENT_KILL': parseKill(obj)
	elif obj.type == 'CLIENT_SUICIDE': parseSuicide(obj)
	elif obj.type == 'CLIENT_GENERICDEATH': parseDeath(obj)
	elif obj.type == 'CLIENT_WORLDDEATH': parseDeath(obj)
	elif obj.type == 'CLIENT_SUICIDE': parseDeath(obj)
	elif obj.type == 'CLIENT_TEAMKILL': parseTeamKill(obj)

def init():
	global T
	if handler.tableExsists('stats_main'): T = tableSelect('stats_main')
	else: T = tableCreate('stats_main', {'id':'int', 'kills':'int', 'deaths':'int', 'tks':'int', 'suicides':'int', 'score':'int'}) #<<< make int/str map too correct Sqlite shit
	A.addlisteners(['CLIENT_KILL', 'CLIENT_SUICIDE', 'CLIENT_GENERICDEATH', 'CLIENT_WORLDDEATH', 'CLIENT_SUICIDE', 'CLIENT_TEAMKILL'])
	
def die(): pass