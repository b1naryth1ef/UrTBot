from debug import log
from player import Player
import sys, os, time
import thread_handler as thread

class Q3API():
    def __init__(self, bot):
        self.B = bot
        self.Q = bot.Q
        self.R = bot.Q.rcon

    def tell(self, plyr, msg):
        if isinstance(plyr, Player): plyr = plyr.cid
        self.R("tell %s ^3%s" % (plyr, msg)) #@DEV check if R.format() works on tell

    def say(self, msg):
        self.R("say %s" % self.R.format('^3'+msg))

class API():
    def __init__(self):
        self.commands = {}
        self.aliases = {}
        self.events = {}
        self.listeners = {'cats':{}, 'eves':{}}
        self.booted = False
        self.listenActions = []
        self.B = None
        self.config = None

    def finishBooting(self):
        self.booted = True
        for i in self.listenActions:
            self.addListener(*i)

    def addCommand(self, cmd, func, desc='', level=0, alias=[]):
        if self.commands.get(cmd):
            return log.warning("Command %s has already been registered!" % cmd)
        self.commands[cmd] = {'exec':func, 'desc':desc, 'level':level}
        for i in alias:
            self.aliases[i] = cmd

    def addEvent(self, name, func):
        if self.events.get('_'.join(name)): return log.warning("Event %s has already been registered!" % name)
        self.events['_'.join(name)] = func
        self.listeners['eves']['_'.join(name)] = []
        for i in name[:-1]:
            if not self.listeners['cats'].get(i):
                self.listeners['cats'][i] = []
        log.debug('Event %s has been registered!' % '_'.join(name))

    def addListener(self, name, func):
        if not self.booted: 
            self.listenActions.append((name, func))
            return
        if name in self.listeners['cats']:
            return self.listeners['cats'][name].append(func)
        if name in self.listeners['eves'].keys():
            return self.listeners['eves'][name].append(func)
        log.warning("Event %s has not been registered!" % (name))

    def fireEvent(self, name, data={}, obj=None):
        log.debug('Firing event %s' % name)
        if not obj: 
            try: obj = self.events[name].getObj(data)
            except:
                return log.debug('Cannot find event %s!' % name)
        [thread.fireThread(i, obj) for i in self.listeners['eves'][name]]
        if obj.cats:
            for cat in obj.cats.split('_'):
                [thread.fireThread(i, obj) for i in self.listeners['cats'][cat]]

    def fireCommand(self, cmd, data):
        user = data['client']
        log.debug('Group: %s' % user.group)
        log.debug('Groups: %s' % self.config.botConfig['groups'])
        _min = self.config.botConfig['groups'][user.group]['minlevel']
        _max =  self.config.botConfig['groups'][user.group]['maxlevel']
        if cmd in self.commands.keys(): obj = self.commands.get(cmd)
        elif cmd in self.aliases.keys(): obj = self.aliases.get(cmd)
        else: return API.tell(user, '^1No such command ^3%s^1!' % cmd)
        if _min <= obj['level'] <= _max:
            thread.fireThread(self.commands.get(cmd), data)
        else:
            log.debug('No access: %s < %s < %s' % (_min, obj['level'], _max))
            API.tell(user, '^1You do not have sufficient access to use ^3%s^1!' % cmd)

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

class FiredEvent():
    def __init__(self, name, data, cats=[]):
        self.name = name
        self.data = data
        self.cats = cats
        self.__dict__.update(data)

class Event():
    def __init__(self, name):
        name = name.upper()
        self.n = name.split('_')
        self.name = name
        self.cats = '_'.join(self.n[:-1])
        A.addEvent(self.n, self)

    def getObj(self, data={}):
        return FiredEvent(self.name, data, self.cats)

    def fire(self, data={}):
        A.fireEvent(self.name, obj=self.getObj(data))

EVENTS = {
'CLIENT_HIT_DO':Event('CLIENT_HIT_DO'),
'CLIENT_HIT_GET':Event('CLIENT_HIT_GET'),
'CLIENT_DIE_TK':Event('CLIENT_DIE_TK'),
'CLIENT_DIE_WORLD':Event('CLIENT_DIE_WORLD'),
'CLIENT_DIE_SUICIDE':Event('CLIENT_DIE_SUICIDE'),
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
'CLIENT_CONN_TIMEOUT':Event('CLIENT_CONN_TIMEOUT'),
'CLIENT_CONN_DENIED':Event('CLIENT_CONN_DENIED'),
'CLIENT_CONN_CONNECT':Event('CLIENT_CONN_CONNECT'),
'CLIENT_CONN_DISCONNECT':Event('CLIENT_CONN_DISCONNECT'),
'CLIENT_CONN_CONNECTED':Event('CLIENT_CONN_CONNECTED'),
'CLIENT_CONN_KICKED':Event('CLIENT_CONN_KICKED'),
'CLIENT_INFO_SET':Event('CLIENT_INFO_SET'),
'CLIENT_INFO_CHANGE':Event('CLIENT_INFO_CHANGE'),
'CLIENT_INFO_NAME':Event('CLIENT_INFO_NAME'),
'CLIENT_INFO_UPDATE':Event('CLIENT_INFO_UPDATE'),
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
