import time

class Event():
	def updateData(self, data=self.data): self.__dict__.update(data)

	def __init__(self, Type, data):
		self.fireTime = time.time()
		self.data = data
		self.type = Type

		self.updateData()

class EventServer(Event): pass
class EventClient(Event): pass
class EventGame(Event): pass
class EventOther(Event): pass
class EventMessage(Event): pass
class EventGenric(Event): pass
class EventCustom(Event): pass

def GENERIC(data): return EventGenric(data['event'], data)
def CHAT_MESSAGE(data): return EventServer('CHAT_MESSAGE', data)
def TEAMCHAT_MESSAGE(data): return EventServer('TEAMCHAT_MESSAGE', data)

def CLIENT_COMMAND(data): return EventClient('CLIENT_COMMAND', data)
def CLIENT_TELL(data): return EventClient('CLIENT_TELl', data)
def CLIENT_JOIN(data): return EventGame('CLIENT_JOIN', data)
def CLIENT_CONNECT(data): return EventServer('CLIENT_CONNECT', data)
def CLIENT_CONNECTED(data): return EventClient('CLIENT_CONNECTED', data)
def CLIENT_BEGIN(data): return EventClient('CLIENT_BEGIN', data)
def CLIENT_DISCONNECT(data): return EventServer('CLIENT_DISCONNECT', data)
def CLIENT_USERINFO(data): return EventClient('CLIENT_USERINFO', data)
def CLIENT_QUIT(data): return EventClient('CLIENT_QUIT', data)
def CLIENT_KICKED(data): return EventClient('CLIENT_KICKED', data)
def CLIENT_SWITCHTEAM(data): return EventClient('CLIENT_SWITCHTEAM', data)
def CLIENT_KILL(data): return EventClient('CLIENT_KILL', data)
def CLIENT_GENERICDEATH(data): return EventClient('CLIENT_GENERICDEATH', data)
def CLIENT_KILLTEAM(data): return EventClient('CLIENT_KILLTEAM')
def CLIENT_SUICIDE(data): return EventClient('CLIENT_SUICIDE', data)
def CLIENT_WORLDDEATH(data): return EventClient('CLIENT_WORLDDEATH', data)
def CLIENT_HIT(data): return EventClient('CLIENT_HIT', data)
def CLIENT_PICKUPITEM(data): return EventClient('CLIENT_PICKUPITEM', data)
def CLIENT_CHANGENAME(data): return EventClient('CLIENT_CHANGENAME', data)
def CLIENT_CHANGELOADOUT(data): return EventClient('CLIENT_CHANGELOADOUT', data)

def GAME_FLAGCAPTURE(data): return EventGame('GAME_FLAGCAPTURE', data)
def GAME_FLAGPICKUP(data): return EventGame('GAME_FLAGPICKUP', data)
def GAME_FLAGDROP(data): return EventGame('GAME_FLAGDROP', data)
def GAME_FLAGRETURN(data): return EventGame('GAME_FLAGRETURN', data)
def GAME_FLAGRESET(data): return EventGame('GAME_FLAGRESET', data)
def GAME_ROUND_START(data): return EventGame('GAME_ROUND_START', data)
def GAME_ROUND_END(data): return EventGame('GAME_ROUND_END', data)
def GAME_MATCH_END(data): return EventGame('GAME_MATCH_END', data)
def GAME_MATCH_START(data): return EventGame('GAME_MATCH_START', data)
def GAME_SHUTDOWN(data): return EventGame('GAME_SHUTDOWN', data)

EVENTS = {
	'CHAT_MESSAGE': CHAT_MESSAGE,
	'TEAMCHAT_MESSAGE': TEAMCHAT_MESSAGE,
	'CLIENT_COMMAND': CLIENT_COMMAND,
	'CLIENT_TELL':CLIENT_TELL, #
	'CLIENT_JOIN':CLIENT_JOIN, #
	'CLIENT_CONNECT':CLIENT_CONNECT,
	'CLIENT_CONNECTED':CLIENT_CONNECTED,
	'CLIENT_BEGIN':CLIENT_BEGIN,
	'CLIENT_DISCONNECT':CLIENT_DISCONNECT, #
	'CLIENT_USERINFO':CLIENT_USERINFO, #
	'CLIENT_QUIT':CLIENT_QUIT, #
	'CLIENT_KICKED':CLIENT_KICKED, #
	'CLIENT_SWITCHTEAM':CLIENT_SWITCHTEAM, #
	'CLIENT_KILL':CLIENT_KILL, #
	'CLIENT_GENERICDEATH':CLIENT_GENERICDEATH, #
	'CLIENT_KILLTEAM':CLIENT_KILLTEAM, #
	'CLIENT_SUICIDE':CLIENT_SUICIDE, #
	'CLIENT_WORLDDEATH':CLIENT_WORLDDEATH,
	'CLIENT_HIT':CLIENT_HIT,
	'CLIENT_PICKUPITEM':CLIENT_PICKUPITEM,
	'CLIENT_CHANGENAME':CLIENT_CHANGENAME,
	'CLIENT_CHANGELOADOUT':CLIENT_CHANGENAME,
	'GAME_FLAGCAPTURE':GAME_FLAGCAPTURE,
	'GAME_FLAGPICKUP':GAME_FLAGPICKUP,
	'GAME_FLAGDROP':GAME_FLAGDROP,
	'GAME_FLAGRETURN':GAME_FLAGRETURN,
	'GAME_FLAGRESET':GAME_FLAGRESET,
	'GAME_ROUND_START':GAME_ROUND_START,
	'GAME_ROUND_END':GAME_ROUND_END,
	'GAME_MATCH_END':GAME_MATCH_END,
	'GAME_MATCH_START':GAME_MATCH_START,
	'GAME_SHUTDOWN':GAME_SHUTDOWN,
	'GENERIC':GENERIC,
}
