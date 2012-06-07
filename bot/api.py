from debug import log
import sys, os, time

class API():
    def __init__(self):
        self.commands = {}
        self.aliases = {}
        self.events = {}
        self.listeners = {}

    def addCommand(self, cmd, func, desc='', level=0, alias=[]):
        if self.commands.get(cmd):
            return log.warning("Command %s has already been registered!" % cmd)
        self.commands[cmd] = (func,desc,level)
        for i in alias:
            self.aliases[i] = (func,desc,level,cmd)

    def addEvent(self, name):
        if self.events.get(name):
            return log.warning("Event %s has already been registered!" % name)
        self.events[name] = Event(name)

    def addListener(self, name, func):
        if self.events.get(name):
            self.events.get(name).listeners.append(func)
        else:
            log.warning("Event %s has not been registered!")

    def fireEvent(self, name, data):
        log.debug('Firing event %s' % name)
        obj = FiredEvent(name, data)
        for listen in self.events[name].listeners:
            listen(obj)
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

class Event():
    def __init__(self, name):
        self.name = name
        self.listeners = []

class FiredEvent():
    def __init__(self, name, data):
        self.__dict__.update(data)
        self.fired = time.time()


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

for eve in EVENTS:
    A.addEvent(eve)
