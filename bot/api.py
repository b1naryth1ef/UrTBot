from debug import log
from player import Player
import sys, os, time
import thread_handler as thread

class Q3API():
    def __init__(self, bot):
        self.B = bot
        self.Q = bot.Q
        self.R = bot.Q.rcon

        if not self.B.hasPrefix:
            self.prefix = self.B.prefix
            self.saylength = 69
            self.telllength = 64 
        else:
            self.saylength = 78-len(self.B.prefix)
            self.telllength = 74-len(self.B.prefix) #[PM]
            self.prefix = ""

    def _rendplyr(self, plyr):
        if isinstance(plyr, Player): return plyr.cid
        else: return plyr

    def tell(self, plyr, msg):
        prefix = self.B.prefix if not self.B.hasPrefix else ""
        return self.R('tell %s "%s"' % (self._rendplyr(plyr), self.Q.format(prefix+'^3'+msg, self.telllength))) #@DEV check if R.format() works on tell

    def kick(self, plyr, reason):
        if not self.B.hasKickMsg: reason = ""
        del self.B.Clients[plyr.cid] #@DEV Seems shady...
        return self.R('kick %s "%s"' % (self._rendplyr(plyr), reason))

    def say(self, msg):
        prefix = self.B.prefix if not self.B.hasPrefix else ""
        return self.R('say "%s"' % (self.Q.format(prefix+'^3'+msg, self.saylength)))

    def getObj(self, txt, reply=None):
        u = None
        if txt.startswith('@'): u = self.B.findByName(txt[1:], approx=True)
        elif txt.isdigit() and int(txt) in self.B.Clients.keys(): u = self.B.Clients[int(txt)]
        else: 
            res = []
            for i in self.B.Clients.values():
                if txt.lower() in i.name.lower(): res.append(i)
            if len(res):
                if len(res) == 1: u = res[0]
                elif len(res) > 1:
                    reply.tell('^1Found more than one user for your query! Try again with a more specific search term!')
        if not u and reply:
            reply.tell('^1Could not find user! Try again, and remember to place an @ in front of names containg numbers!')
        return u

class API():
    def __init__(self):
        self.commands = {}
        self.aliases = {}
        self.events = {}
        self.listeners = {'cats':{}, 'eves':{}}
        self.booted = False
        self.listenActions = [] #Buffer
        self.B = None
        self.Q3 = None
        self.config = None

    def finishBooting(self, bot, config):
        self.booted = True
        self.B = bot
        self.config = config
        for i in self.listenActions:
            self.addListener(*i)

    def addCommand(self, cmd, func, desc='', usage='', level=0, alias=[]):
        if self.commands.get(cmd):
            return log.warning("Command %s has already been registered!" % cmd)
        level = self.B.config.botConfig['permissions'].get(cmd, level)
        self.commands[cmd] = {'exec':func, 'desc':desc, 'usage':usage, 'level':level}
        for i in alias:
            self.aliases[i] = cmd

    def removeCommand(self, cmd):
        if hasattr(cmd, '_cmd'): cmd = cmd._cmd
        if hasattr(cmd, '_alias'):
            for i in cmd._alias:
                if i in self.aliases.keys():
                    del self.aliases[i]
        if cmd in self.commands.keys():
            del self.commands[cmd] #@TODO Eventually move to new dict?
        else:
            log.warning('Command %s is not registered so we cant remove it!' % cmd)

    def addEvent(self, name, func):
        if self.events.get('_'.join(name)): return log.warning("Event %s has already been registered!" % name)
        self.events['_'.join(name)] = func
        self.listeners['eves']['_'.join(name)] = []
        for i in name[:-1]:
            if not self.listeners['cats'].get(i):
                self.listeners['cats'][i] = []
        log.debug('Event %s has been registered!' % '_'.join(name))

    def addListener(self, name, func):
        if isinstance(name, Event):
            name = name.name
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
        cmd = cmd.lower()
        user = data['client']
        if not user.client: user.getClient()
        log.debug('Group: %s' % user.client.group)
        _min = self.config.botConfig['groups'][user.client.group]['minlevel']
        _max =  self.config.botConfig['groups'][user.client.group]['maxlevel']
        _etc = self.config.botConfig['groups'][user.client.group]['levels']
        if cmd in self.commands.keys(): obj = self.commands.get(cmd)
        elif cmd in self.aliases.keys(): obj = self.commands[self.aliases.get(cmd)]
        else: return Q3.tell(user, '^1No such command ^3%s^1!' % cmd)
        if _min <= obj['level'] <= _max or obj['level'] in _etc:
            thread.fireThread(obj['exec'], FiredCommand(cmd, data, obj['usage']))
        else:
            log.debug('No access: %s < %s < %s' % (_min, obj['level'], _max))
            Q3.tell(user, '^1You do not have sufficient access to use ^3%s^1!' % cmd)

A = API()

def command(cmd, desc='None', usage="{cmd}", level=0, alias=[]):
    def decorator(target):
        A.addCommand(cmd, target, desc, usage, level, alias)
        target._cmd = cmd
        target._alias = alias
        return target
    return decorator

def listener(event):
    def decorator(target):
        A.addListener(event, target)
        return target
    return decorator

class FiredCommand():
    def __init__(self, cmd, data, usage):
        self._cmd = cmd
        self._usage = usage
        self.__dict__.update(data)

    def usage(self, obj=None): #cleanup?
        obj = obj or self.client
        s = "Usage: {prefix}{cmd} "+self._usage
        d = {'cmd':self._cmd, 'user':'cid/name/@name', 'prefix':Q3.B.config.botConfig['cmd_prefix']}
        Q3.tell(obj, s.format(**d))

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
    global Q3, A
    Q3 = Q3API(BOT)
    A.Q3 = Q3
