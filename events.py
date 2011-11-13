import time

class Event():
	def __init__(self, data):
		self.fireTime = time.time()
		self.data = data
class EventServer(): pass
class EventClient(): pass
class EventOther(): pass
class EventMessage(): pass


def CHAT_MESSAGE(data): pass
def TEAMCHAT_MESSAGE(data): pass

def CLIENT_COMMAND(data): pass
def CLIENT_SAY(data): pass
def CLIENT_SAYTEAM(data): pass
def CLIENT_TELL(data): pass
def CLIENT_JOIN(data): pass
def CLIENT_CONNECT(data): pass
def CLIENT_USERINFO(data): pass
def CLIENT_QUIT(data): pass
def CLIENT_KICKED(data): pass
def CLIENT_SWITCHTEAM(data): pass
def CLIENT_KILL(data): pass
def CLIENT_GENERICDEATH(data): pass
def CLIENT_KILLTEAM(data): pass
def CLIENT_SUICIDE(data): pass
def CLIENT_WORLDDEATH(data): pass
def CLIENT_INFLICTDAMAGE(data): pass
def CLIENT_DAMAGED(data): pass
def CLIENT_PICKUPITEM(data): pass
def CLIENT_CHANGENAME(data): pass
def CLIENT_CHANGELOADOUT(data): pass

EVENTS = {
	'CHAT_MESSAGE':None, #
	'TEAMCHAT_MESSAGE':None,#
	'CLIENT_COMMAND':None, #
	'CLIENT_SAY':None, # 
	'CLIENT_SAYTEAM':None, #
	'CLIENT_TELL':None, #
	'CLIENT_JOIN':None, #
	'CLIENT_CONNECT':None, #
	'CLIENT_USERINFO':None, #
	'CLIENT_QUIT':None, #
	'CLIENT_KICKED':None, #
	'CLIENT_SWITCHTEAM':None, #
	'CLIENT_KILL':None, #
	'CLIENT_GENERICDEATH':None, #
	'CLIENT_KILLTEAM':None, #
	'CLIENT_SUICIDE':None, #
	'CLIENT_WORLDDEATH':None,
	'CLIENT_INFLICTDAMAGE':None,
	'CLIENT_DAMAGED':None,
	'CLIENT_PICKUPITEM':None,
	'CLIENT_CHANGENAME':None,
	'CLIENT_CHANGELOADOUT':None,
	'GAME_ROUND_START':None,
	'GAME_ROUND_END':None,
	'GAME_MATCH_END':None,
	'GAME_MATCH_START':None,
	'GENERIC':None,
}