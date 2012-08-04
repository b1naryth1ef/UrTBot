from debug import log
from player import Player
from q3api import Q3API
import database
import sys, os, time
import thread_handler as thread

EVENTS = {}

class API():
    def __init__(self):
        self.plugins = {}
        self.commands = {}
        self.aliases = {}
        self.events = {}
        self.listeners = {'cats':{}, 'eves':{}}
        self.booted = False
        self.listenActions = [] #Buffer
        self.B = None
        self.Q3 = None
        self.config = None

        self.configs_path = os.path.join('./', 'bot', 'mods', 'config')

    def finishBooting(self, bot, config):
        self.booted = True
        self.B = bot
        self.config = config
        for i in self.listenActions:
            self.addListener(*i)

        for i in self.plugins.values():
            log.info('Enabling %s!' % i['name'])
            i['obj'].onEnable()

    def hasPlugin(self, name):
        return name in self.plugins.keys()

    def addPlugin(self, name, obj):
        if name not in self.plugins.keys():
            self.plugins[name] = {'name':name, 'enabled':False, 'obj':obj}
        else:
            log.warning('Module %s already exists!' % name)

    def addCommand(self, cmd, func, desc='', usage='', level=0, alias=[]):
        func._cmd = cmd
        func._alias = alias
        if type(level) is not list: level = [level]
        if self.commands.get(cmd):
            return log.warning("Command %s has already been registered!" % cmd)
        level = self.B.config.botConfig['permissions'].get(cmd, level)
        self.commands[cmd] = {'exec':func, 'desc':desc, 'usage':usage, 'level':level, 'name':cmd}
        for i in alias:
            self.aliases[i] = cmd

    def rmvCommand(self, cmd):
        if hasattr(cmd, '_cmd'): cmd = cmd._cmd
        if hasattr(cmd, '_alias'):
            for i in cmd._alias:
                if i in self.aliases.keys():
                    del self.aliases[i]
        if cmd in self.commands.keys():
            del self.commands[cmd]
        else:
            log.warning('Command %s is not registered so we cant remove it!' % cmd)

    def addEvent(self, name, obj):
        if self.events.get('_'.join(name)): return log.warning("Event %s has already been registered!" % name)
        self.events['_'.join(name)] = obj
        self.listeners['eves']['_'.join(name)] = []
        for n in [name[:i] for i in range(0, len(name)) if name[:i] != []]:
            if not self.listeners['cats'].get('_'.join(n)):
                self.listeners['cats']['_'.join(n)] = []
        log.debug('Event %s has been registered!' % '_'.join(name))

    def addListener(self, name, func=None, cid=None, uid=None, obj=None):
        if isinstance(name, Event):
            name = name.name
        if not self.booted:
            self.listenActions.append((name, func, cid, uid, obj))
            return
        if not obj:
            obj = Listener(func, [name], cid, uid)
        if name in self.listeners['eves']:
            return self.listeners['eves'][name].append(obj)
        if name in self.listeners['cats']:
            return self.listeners['cats'][name].append(obj)
        log.warning("Event %s has not been registered!" % (name))

    def rmvListener(self, obj): #@DEV This could be cleaner
        for eve in obj.events:
            for i in [i for i in self.listeners['eves'][eve]]+[i for i in self.listeners['cats'][eve]]:
                if i == obj:
                    del i

    def fireEvent(self, names, data={}, obj=None):
        def _feve(i):
            if 'client' in data:
                if i.cid and i.cid != data['client'].cid: return
                if i.uid and i.uid != data['client'].uid: return
            thread.fireThread(i, obj)

        if type(names) in (str, int): names = [names]
        elif type(names) != list: names = list(names)
        for name in names:
            log.debug('Firing event %s' % name)
            if not obj: 
                try: obj = self.events[name].getObj(data)
                except:
                    return log.warning('Cannot find event %s!' % name)
            for i in self.listeners['eves'][name]:
                _feve(i)
            if obj._cats:
                for n in [obj._n[:i] for i in range(0, len(obj._n)) if obj._n[:i] != []]: #@FIXME clean this up plz
                    for i in self.listeners['cats']['_'.join(n)]:
                        _feve(i)
                
    def hasAccess(self, client, cmd):
        if not client.user: client.getUser()
        _min = self.config.botConfig['groups'][client.user.group]['minlevel']
        _max =  self.config.botConfig['groups'][client.user.group]['maxlevel']
        _etc = self.config.botConfig['groups'][client.user.group]['levels']
        if len([i for i in cmd['level'] if _min <= i <= _max or i in _etc]):
            return True
        return False

    def fireCommand(self, cmd, data):
        cmd = cmd.lower().replace('#', '')
        client = data['client']
        if not hasattr(client, 'user'): client.getUser()
        if cmd in self.commands.keys(): obj = self.commands.get(cmd)
        elif cmd in self.aliases.keys(): obj = self.commands[self.aliases.get(cmd)]
        else: return Q3.tell(client, '^1No such command ^3%s^1!' % cmd)
        if self.hasAccess(client, obj):
            thread.fireThread(obj['exec'], FiredCommand(cmd, data, obj))
        else:
            Q3.tell(client, '^1You do not have sufficient access to use ^3%s^1!' % cmd)

A = API()

def command(cmd, desc='None', usage="{cmd}", level=0, alias=[]):
    def decorator(target):
        A.addCommand(cmd, target, desc, usage, level, alias)
        return target
    return decorator

def listener(eventz, cid=None, uid=None):
    def decorator(target):
        if not getattr(eventz, '__iter__', False):
            eventz = [eventz]
        l = Listener(target, eventz, cid, uid)
        return target
    return decorator

class Listener():
    def __init__(self, func, events, cid, uid):
        self.events = events
        self.cid = cid
        self.uid = uid
        self.func = func

        for i in events:
            if isinstance(i, Event): i = i.name
            A.addListener(i, obj=self)

    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)

class FiredCommand():
    def __init__(self, cmd, data, obj):
        self._cmd = cmd
        self._obj = obj
        self._usage = obj['usage']
        self.__dict__.update(data)

    def usage(self, obj=None): #cleanup?
        obj = obj or self.client
        s = "Usage: {prefix}{cmd} "+self._usage
        d = {'cmd':self._cmd, 'user':'name/cid/@uid', 'prefix':Q3.B.config.botConfig['cmd_prefix']}
        Q3.tell(obj, s.format(**d))

class FiredEvent():
    def __init__(self, name, data, cats=[]):
        self._name = name
        self._n = name.split('_')
        self._cats = cats
        self.data = data
        self.__dict__.update(data)

class Event():
    def __init__(self, name):
        self.name = name.upper()
        self.n = self.name.split('_')
        self.cats = '_'.join(self.n[:-1])
        A.addEvent(self.n, self)
        #EVENTS[name] = self

    def getObj(self, data={}):
        return FiredEvent(self.name, data, self.cats)

    def fire(self, data={}):
        A.fireEvent(self.name, obj=self.getObj(data))

#CLIENT
Event('CLIENT_HIT_ATK'),
Event('CLIENT_HIT_DEF'),
Event('CLIENT_DIE_TK'),
Event('CLIENT_DIE_WORLD'),
Event('CLIENT_DIE_SUICIDE'),
Event('CLIENT_DIE_GEN'),
Event('CLIENT_KILL_TK'),
Event('CLIENT_KILL_GEN'),
Event('CLIENT_SAY_CMD'),
Event('CLIENT_SAY_GLOBAL'),
Event('CLIENT_SAY_TEAM'),
Event('CLIENT_SAY_TELL'),
Event('CLIENT_TEAM_SWITCH'),
Event('CLIENT_TEAM_JOIN'),
Event('CLIENT_TEAM_LEAVE'),
Event('CLIENT_ITEM_PICKUP'),
Event('CLIENT_CONN_CONNECT'),
Event('CLIENT_CONN_CONNECTED'),
Event('CLIENT_CONN_DC_GEN'),
Event('CLIENT_CONN_DC_CI'),
Event('CLIENT_CONN_DC_KICK'),
Event('CLIENT_INFO_SET'),
Event('CLIENT_INFO_CHANGE'),
Event('CLIENT_GEN_CALLVOTE'),
Event('CLIENT_GEN_VOTE'),
Event('CLIENT_GEN_RADIO'),
#GAME
Event('GAME_MATCH_START'),
Event('GAME_ROUND_START'),
Event('GAME_ROUND_END'),
Event('GAME_MATCH_END'),
Event('GAME_MATCH_TIMELIMIT'),
Event('GAME_GEN_SHUTDOWN'),
Event('GAME_GEN_STARTUP'),
Event('GAME_VOTE_CALL'),
Event('GAME_VOTE_PASS'),
Event('GAME_VOTE_FAIL'),
Event('GAME_VOTE_VETO'),
Event('GAME_FLAG_RETURN'),
Event('GAME_FLAG_CAPTURE'),
Event('GAME_FLAG_PICKUP'),
Event('GAME_FLAG_DROP'),
Event('GAME_FLAG_HOTPOTATO'),

def setup(BOT):
    global Q3, A
    Q3 = Q3API(BOT)
    A.Q3 = Q3
