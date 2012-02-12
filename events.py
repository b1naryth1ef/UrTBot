import time

class Event():
    def __init__(self, Type, data):
        self.fireTime = time.time()
        self.data = data
        self.type = Type
        self.updateData()
        self.__dict__.update(data)

class EventCustom(Event): pass #Is the local version of events for plugins (other plugins should NOT be able to hook into it)
class EventPlugin(Event): pass #Is the global version of events for plugins (use this if other plugins might want to hook into it)

EVENTS = ['CLIENT_BEGIN',
'GAME_MATCH_START',
'GENERIC',
'GAME_ROUND_END',
'CLIENT_KICKED',
'CLIENT_SUICIDE',
'CLIENT_CHANGELOADOUT',
'CLIENT_HIT',
'CLIENT_TEAMKILL',
'GAME_SHUTDOWN',
'CLIENT_WORLDDEATH',
'GAME_FLAGRETURN',
'GAME_ROUND_START',
'CLIENT_KILL',
'CLIENT_COMMAND',
'CLIENT_SWITCHTEAM',
'CLIENT_PICKUPITEM',
'GAME_FLAGPICKUP',
'TEAMCHAT_MESSAGE',
'GAME_FLAGCAPTURE',
'GAME_MATCH_END',
'CHAT_MESSAGE',
'CLIENT_JOIN',
'CLIENT_CONNECTED',
'CLIENT_QUIT',
'GAME_FLAGDROP',
'CLIENT_CHANGENAME',
'CLIENT_TELL',
'CLIENT_USERINFO',
'CLIENT_GENERICDEATH',
'CLIENT_CONNECT',
'GAME_FLAGRESET',
'CLIENT_DISCONNECT']

CUSTOM_EVENTS = []
PLUGIN_EVENTS = []
