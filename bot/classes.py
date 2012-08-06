import socket, select, time, re, thread
import bot, player, const, database, main
import sys, os, time
import thread_handler as thread
from collections import deque
from rcon import RCON
from debug import log
from datetime import datetime

class Bot():
    def __init__(self, config=None, database=None):
        self.prefix = config.botConfig['prefix']
        self.Q = RCON(config.botConfig['rconip'], config.botConfig['rcon'])
        self.database = database
        self.config = config

        self.boottime = datetime.now() #@NOTE this could be more acurate but screw it

        self.enabled = True
        self.logback = deque()
        
        self.maplist = self.config.UrTConfig['maps']
        self.gameData = {}
        self.serverData = {}
        self.currentMap = None
        self.loadingMap = False
        self.justChangedMap = False
        self.authEnabled = False

        self.demos = {}

        self.redScore = 0
        self.blueScore = 0

        self.Clients = {} #AKA players
        self.ClientBacklog = deque()
        self.curClients = lambda: [int(i[0]) for i in self.getStatus()]

    def getGroup(gid):
        return self.config.botConfig['groups'].get(gid)

    def removeClient(self, cid):
        log.debug('Attempting to remove client #%s' % cid)
        if int(cid) in self.Clients.keys():
            if len(self.ClientBacklog) > 10:
                self.ClientBacklog.popleft()
            self.ClientBacklog.append(self.Clients[cid])
            del self.Clients[cid]
            log.debug('Removed client w/ CID #%s' % cid)
        else:
            log.debug('Client w/ CID #%s could not be removed, the cid is invalid')

    def roundNew(self):
        log.debug('New round starting!')
        self.A.fireEvent('GAME_ROUND_START', {})

    def roundEnd(self):
        log.debug('Round over!')
        self.A.fireEvent('GAME_ROUND_END', {})

    def matchNew(self, data):
        log.debug('New match starting!')
        self.A.fireEvent('GAME_MATCH_START', {'data':data})
        self.loadingMap = False
        self.justChangedMap = True

    def matchEnd(self):
        log.debug('Match over! RED: %s BLUE: %s' % (self.redScore, self.blueScore))
        self.A.fireEvent('GAME_MATCH_END', {'redscore':self.redScore, 'bluescore':self.blueScore})
        self.loadingMap = True
    
    def getClient(self, cid):
        log.debug('Attempting to get client #%s' % cid)
        if cid in self.Clients.keys():
            log.debug('Found client #%s' % cid)
            return self.Clients[cid]
        log.debug('Could not find client #%s' % cid)

    def getGameType(self):
        r = self.Q.rcon('g_gametype')
        r = re.findall(const.rconGameType, r)
        self.gameData['g_gametype'] = int(r[0][0])
        return self.gameData['g_gametype']

    def setScores(self, line):
        #Scores: R:11 B:9
        line = re.findall('.*?(\\d+)', line)
        self.redScore = int(line[0])
        self.blueScore = int(line[1])

    def getPlayerTeam(self, cid):
        i = self.Q.rcon('players').split('\n')[4:]
        out = []
        for l in i:
            l = re.findall('([0-9]+): (.*?) (.*?) k:([0-9]+) d:([0-9]+) ping:([0-9]+) (.*?)', l)
            if len(l):
                l = l[0]
                if int(l[0]) == cid:
                    return const.findTeam(l[2])

    def getPlayers(self): #0: Eduardodias2012 BLUE k:9 d:11 ping:196 200.181.147.46:44453
        r = self.Q.rcon('players').split('\n') #@DEV THIS IS BROKEN. FIX FOR 4.2!!!
        self.setScores(r[3])
        for player in self.Clients.values():
            player.setData(self.dumpUser(player.cid))
        for i in [i.split(' ') for i in r[4:] if i != ""]:
            obj = self.findByName(i[1])
            if obj:
                obj.team = const.teams[const.teams_text[i[2].lower()]]
                obj.score[0] = i[3].strip('k:')
                obj.score[1] = i[4].strip('d:')
        
    def dumpUser(self, uid):
        data = self.Q.rcon('dumpuser %s' % uid)
        if data.startswith('print'):
            data = data.split('\n')
            li = [[y for y in x.split(' ') if y != ''] for x in data[3:]]
            return dict([(x[0], ' '.join(x[1:])) for x in li if x and x[0] != 'team'])
            
    def getStatus(self):
        varz = []
        r = self.Q.rcon('status').split('\n')
        self.currentMap = r[1][5:]
        for i in r[4:]:
            if i != '':
                varz.append([o for o in i.split(' ') if o != ''])
        return varz

    def getCurrentMap(self):
        r = const.rconCurrentMap.search(self.Q.rcon('mapname'))
        self.currentMap = r.group(1)
        self.gameData['mapname'] = r.group(1)
        return self.gameData['mapname']

    def Startup(self, API):
        self.api = API
        self.A = self.api.A
        self.Q3 = self.A.Q3
        log.info('SETUP: BOT')

        resp = self.Q3.R("say \"^3UrTBot is starting up...\"")
        if resp is None:
            log.critical('The server is not reachable. Check the ip/port and try again!')
            sys.exit()
        elif "No rconpassword set on the server." in resp:
            log.critical('The server does not have an rcon password. Please check your server config and try again.')
            sys.exit()
        elif 'Bad rconpassword.' in resp:
            log.critical('The rcon password you provided was incorrect. Please double check it and try again.')
            sys.exit()
        
        self.maplist += [i for i in self.Q.rcon("sv_pakNames").split('"')[3].split() if i not in self.config.UrTConfig['ignoremaps']]

        self.serverData['hasauth'] = self.Q.getCvar('auth_enable')
        if type(self.serverData['hasauth']) is int: bool(self.serverData['hasauth'])
        else: log.error('Error getting hasauth: %s' % self.serverData['hasauth'])

        if self.serverData['hasauth'] and self.config.botConfig['use_auth']:
            self.authEnabled = True
            log.info('Auth is enabled!')
        else:
            self.authEnabled = False
            log.info('Auth is disabled!')

        self.Q.rcon('sv_sayprefix "%s: "' % self.config.botConfig['prefix'])
        self.Q.rcon('sv_tellprefix "%s [PM]: "' % self.config.botConfig['prefix'])
        self.Q.rcon('sv_demonotice ""')

        self.getGameType() #Set g_gametype in self.gamedata
        self.getCurrentMap() #set mapname in self.gamedata

        self.addPlayers()
            
        #self.Q3.setLengths()
        self.Q3.say("^3Startup complete.")
        log.info('SETUP DONE: BOT')

    def addPlayers(self):
        status = self.getStatus()
        if status != []:
            for i in status:
                log.debug('Add User: %s, %s' % (i, i[0]))
                uid = int(i[0])
                self.Clients[uid] = player.Player(uid, self.dumpUser(uid), self.api)
                self.Clients[uid].getUser()
                self.Clients[uid].waitingForBegin = False
            self.getPlayers() #Set team/score for players

    def refreshPlayers(self): pass

    def getClientTeam(self): pass

    def parse(self, line):
        if 0 < len(self.logback) > 5: self.logback.popleft()
        self.logback.append(line)
        main.parse(line)

    def findByName(self, name, approx=False):
        for client in [i for i in self.Clients.values() if i is not None]:
            if client.name == None: return
            if approx and name in client.name.lower(): return client