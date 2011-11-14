import time

class Event():
	def __init__(self, Type, data):
		self.fireTime = time.time()
		self.data = data
		self.type = Type
class EventServer(Event): pass
class EventClient(Event): pass
class EventGame(Event): pass
class EventOther(Event): pass
class EventMessage(Event): pass


def CHAT_MESSAGE(data): return Event('CHAT_MESSAGE', data)
def TEAMCHAT_MESSAGE(data): return Event('TEAMCHAT_MESSAGE', data)

def CLIENT_COMMAND(data): return EventClient('CLIENT_COMMAND', data)
def CLIENT_TELL(data): pass
def CLIENT_JOIN(data): pass
def CLIENT_CONNECT(data): return EventClient('CLIENT_CONNECT', data)
def CLIENT_DISCONNECT(data): return EventClient('CLIENT_DISCONNECT', data)
def CLIENT_USERINFO(data): pass
def CLIENT_QUIT(data): pass
def CLIENT_KICKED(data): pass
def CLIENT_SWITCHTEAM(data): pass
def CLIENT_KILL(data): pass
def CLIENT_GENERICDEATH(data): pass
def CLIENT_KILLTEAM(data): pass
def CLIENT_SUICIDE(data): EventClient('CLIENT_SUICIDE', data)
def CLIENT_WORLDDEATH(data): pass
def CLIENT_HIT(data): pass
def CLIENT_PICKUPITEM(data): return EventClient('CLIENT_PICKUPITEM', data)
def CLIENT_CHANGENAME(data): pass
def CLIENT_CHANGELOADOUT(data): pass

def GAME_FLAGPICKUP(data): return EventGame('GAME_FLAGPICKUP', data)
def GAME_FLAGDROP(data): return EventGame('GAME_FLAGDROP', data)
def GAME_FLAGRETURN(data): return EventGame('GAME_FLAGRETURN', data)
def GAME_ROUND_START(data): pass
def GAME_ROUND_END(data): pass
def GAME_MATCH_END(data): pass
def GAME_MATCH_START(data): pass


EVENTS = {
	'CHAT_MESSAGE': CHAT_MESSAGE,
	'TEAMCHAT_MESSAGE': TEAMCHAT_MESSAGE,
	'CLIENT_COMMAND': CLIENT_COMMAND,
	'CLIENT_TELL':None, #
	'CLIENT_JOIN':None, #
	'CLIENT_CONNECT':CLIENT_CONNECT,
	'CLIENT_DISCONNECT':CLIENT_DISCONNECT, #
	'CLIENT_USERINFO':None, #
	'CLIENT_QUIT':None, #
	'CLIENT_KICKED':None, #
	'CLIENT_SWITCHTEAM':None, #
	'CLIENT_KILL':None, #
	'CLIENT_GENERICDEATH':None, #
	'CLIENT_KILLTEAM':None, #
	'CLIENT_SUICIDE':CLIENT_SUICIDE, #
	'CLIENT_WORLDDEATH':None,
	'CLIENT_HIT':None,
	'CLIENT_PICKUPITEM':CLIENT_PICKUPITEM,
	'CLIENT_CHANGENAME':None,
	'CLIENT_CHANGELOADOUT':None,
	'GAME_FLAGPICKUP':GAME_FLAGPICKUP,
	'GAME_FLAGDROP':GAME_FLAGDROP,
	'GAME_FLAGRETURN':GAME_FLAGRETURN,
	'GAME_ROUND_START':None,
	'GAME_ROUND_END':None,
	'GAME_MATCH_END':None,
	'GAME_MATCH_START':None,
	'GENERIC':None,
}