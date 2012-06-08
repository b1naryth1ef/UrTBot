from debug import log
from player import Player
import sys, os, time

class Q3API():
    def __init__(self, bot):
        self.B = bot
        self.Q = bot.Q
        self.R = bot.Q.rcon

    def tell(self, plyr, msg):
        if isinstance(plyr, Player): plyr = plyr.cid
        self.R("tell %s %s" % (plyr, msg))

    def say(self, msg):
        self.R("say %s" % msg)

class API():
    def __init__(self):
        self.commands = {}
        self.aliases = {}
        self.events = {}
        self.listeners = {'cats':{}, 'eves':{}}

    def addCommand(self, cmd, func, desc='', level=0, alias=[]):
        if self.commands.get(cmd):
            return log.warning("Command %s has already been registered!" % cmd)
        self.commands[cmd] = (func,desc,level)
        for i in alias:
            self.aliases[i] = (func,desc,level,cmd)

    def addEvent(self, name, func):
        if self.events.get('_'.join(name)): return log.warning("Event %s has already been registered!" % name)
        self.events['_'.join(name)] = func
        self.listeners['eves']['_'.join(name)] = []
        n = '_'.join(name[:-1])
        if not self.listeners['cats'].get(n):
            self.listeners['cats'][n] = []

    def addListener(self, name, func):
        if name.contains('_'):
            n = name.split('_')
            self.listeners['cats']['_'.join(n[:-1])].append(func)
        if self.listeners['eves'].get(name):
            self.listeners['eves'][name].append(func)
        else:
            log.warning("Event %s has not been registered!" % (name))

    def fireEvent(self, name, data):
        log.debug('Firing event %s' % name)
        obj = self.events['eves'][name].fire(data)
        self.listeners['eves'][name](obj)
        if obj.cat:
            for i in self.listeners['cats'][obj.cat]:
                i(obj)

    def fireCommand(self, cmd, data): pass

A = API()

def command(cmd, desc='None', level=0, alias=[]):
    def decorator(target):
        A.addCommand(cmd, target, desc, level, alias)
        return target
    return decorator

def listener(event):
    def decorator(target):
        A.addListener(event, target)
        return target
    return decorator

def event(event):
    def decorator(target):
        A.addEvent(event)
        return target
    return decorator

class FiredEvent():
    def __init__(self, name, data, cats=[]):
        self.name = name
        self.data = data
        self.cats = cats
        self.__dict__.update(data)

class Event():
    def __init__(self, name):
        self.n = name.split('_')
        self.name = self.n[-1]
        self.cats = '_'.join(self.n[:-1])
        A.addEvent(self.n, self)

    def fire(self, data):
        return FiredEvent(self.name, data, self.cats)

EVENTS = {
'CLIENT_BEGIN':Event('CLIENT_BEGIN'),
'CLIENT_KICKED':Event('CLIENT_KICKED'),
'CLIENT_SUICIDE':Event('CLIENT_SUICIDE'),
'CLIENT_CHANGE_LOADOUT':Event('CLIENT_CHANGE_LOADOUT'),
'CLIENT_HIT_DO':Event('CLIENT_HIT_DO'),
'CLIENT_HIT_GET':Event('CLIENT_HIT_GET'),
'CLIENT_DIE_TK':Event('CLIENT_DIE_TK'),
'CLIENT_DIE_WORLD':Event('CLIENT_DIE_WORLD'),
'CLIENT_DIE_GEN':Event('CLIENT_DIE_GEN'),
'CLIENT_KILL_TK':Event('CLIENT_KILL_TK'),
'CLIENT_KILL_GEN':Event('CLIENT_KILL_GEN'),
'CLIENT_SAY_CMD':Event('CLIENT_SAY_CMD'), #
'CLIENT_SAY_GLOBAL':Event('CLIENT_SAY_GLOBAL'),
'CLIENT_SAY_TEAM':Event('CLIENT_SAY_TEAM'),
'CLIENT_SAY_TELL':Event('CLIENT_SAY_TELL'),
'CLIENT_TEAM_SWITCH':Event('CLIENT_TEAM_SWITCH'),
'CLIENT_TEAM_JOIN':Event('CLIENT_TEAM_JOIN'),
'CLIENT_TEAM_QUIT':Event('CLIENT_TEAM_QUIT'),
'CLIENT_ITEM_PICKUP':Event('CLIENT_ITEM_PICKUP'),
'CLIENT_CONN_JOIN':Event('CLIENT_CONN_JOIN'),
'CLIENT_CONN_QUIT':Event('CLIENT_CONN_QUIT'),
'CLIENT_CONN_TIMEOUT':Event('CLIENT_CONN_TIMEOUT'),
'CLIENT_CONN_DENIED':Event('CLIENT_CONN_DENIED'),
'CLIENT_CONN_CONNECT':Event('CLIENT_CONN_CONNECT'),
'CLIENT_CONN_CONNECTED':Event('CLIENT_CONN_CONNECTED')
'CLIENT_INFO_SET':Event('CLIENT_INFO_SET'),
'CLIENT_INFO_CHANGE':Event('CLIENT_INFO_CHANGE'),
'CLIENT_INFO_NAME':Event('CLIENT_INFO_NAME'),
'GAME_MATCH_START':Event('GAME_MATCH_START'),
'GAME_ROUND_START':Event('GAME_ROUND_START'),
'GAME_ROUND_END':Event('GAME_ROUND_END'),
'GAME_MATCH_END':Event('GAME_MATCH_END'),
'GAME_SHUTDOWN':Event('GAME_SHUTDOWN'),
'GAME_STARTUP':Event('GAME_STARTUP'),
'GAME_FLAG_RETURN':Event('GAME_FLAG_RETURN'),
'GAME_FLAG_PICKUP':Event('GAME_FLAG_PICKUP'),
'GAME_FLAG_CAPTURE':Event('GAME_FLAG_CAPTURE'),
'GAME_FLAG_DROP':Event('GAME_FLAG_DROP'),
'GAME_FLAG_RESET':Event('GAME_FLAG_RESET'),
}

def setup(BOT):
    global API
    API = Q3API(BOT)
