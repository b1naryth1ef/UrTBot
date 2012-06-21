import socket, select, time, re, thread
import bot, player, const, database, main
from debug import log
from rcon import RCON
from collections import deque
import sys, os, time

class Bot():
    def __init__(self, prefix="^1[^3Boteh^1]:", ip='localhost:27960', rcon="", config=None, database=None, api=None):
        self.prefix = prefix
        self.ip = ip
        self.rcon = rcon
        self.Q = RCON(self.ip, self.rcon)
        self.database = database
        self.api = api

        self.enabled = True
        self.config = config
        self.logback = deque()
        
        self.maplist = self.config.UrTConfig['maps']
        self.currentMap = None
        self.gameData = {}
        self.loadingMap = False
        self.justChangedMap = False

        self.hasPrefix = False
        self.hasDemo = False

        self.redScore = 0
        self.blueScore = 0

        self.Modules = {} #Plugins
        self.Listeners = {} #Plugins waiting for Triggers
        self.Triggers = {} #Possible Triggers (Events)
        self.Commands = {} #Commands
        self.Aliases = {} #aliases BIATCH

        self.Clients = {} #AKA players
        self.curClients = lambda: [int(i[0]) for i in self.getStatus()]
        
    def roundNew(self):
        log.debug('New round starting!')
        self.api.fireEvent('GAME_ROUND_START', {})

    def roundEnd(self):
        log.debug('Round over!')
        self.api.fireEvent('GAME_ROUND_END', {})

    def matchNew(self, data):
        log.debug('New match starting!')
        self.api.fireEvent('GAME_MATCH_START', {'data':data})
        self.loadingMap = False
        self.justChangedMap = True

    def matchEnd(self):
        log.debug('Match over! RED: %s BLUE: %s' % (self.redScore, self.blueScore))
        self.api.fireEvent('GAME_MATCH_END', {'redscore':self.redScore, 'bluescore':self.blueScore})
        self.loadingMap = True
    
    def getClient(self, uid): return self.Clients[uid]

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
    
    def updatePlayers(self): #This may not be acurate at all times
        #0: Eduardodias2012 BLUE k:9 d:11 ping:196 200.181.147.46:44453
        r = self.Q.rcon('players').split('\n')
        self.setScores(r[3])
        for i in [i for i in r[4:] if i != ""]:
            obj = self.findByName(i[1])
            if obj:
                obj.team = i[2].lower()
                obj.score[0] = i[3].strip('k:')
                obj.score[1] = i[4].strip('d:')
            else:
                log.debug('Could not find player for updating players: %s' % i[1])

    def dumpUser(self, uid):
        vz = []
        varz = {}
        r = self.Q.rcon('dumpuser %s' % uid).split('\n')
        for i in r[3:]:
            if i != '':
                vz.append([j for j in i.split(' ') if j != ''])
        for i in vz:
            varz[i[0]] = i[1]
        return varz
         
    def getStatus(self):
        varz = []
        r = self.Q.rcon('status').split('\n')[4:]
        for i in r:
            if i != '':
                i = i.split(' ')
                i = [o for o in i if o != '']
                varz.append(i)
        return varz

    def getCurrentMap(self):
        r = const.rconCurrentMap.search(self.Q.rcon('mapname'))
        self.currentMap = r.group(1)
        self.gameData['mapname'] = r.group(1)
        return self.gameData['mapname']

    def fireEvent(self, event, data): pass

    def Startup(self, API):
        self.A = API
        log.info('SETUP: BOT')

        resp = self.Q.rcon("say ^3"+"Starting up...")
        if "No rconpassword set on the server." in resp:
            log.critical('The server does not have an rcon password check. Please check your server config and try again.')
            sys.exit()
        elif 'Bad rconpassword.' in resp:
            log.critical('The rcon password you provided was incorrect. Please double check it and try again.')
            sys.exit()
        
        self.maplist += [i for i in self.Q.rcon("sv_pakNames").split('"')[3].split() if i not in self.config.UrTConfig['ignoremaps']]
        log.debug('MAPLIST: %s' % self.maplist)

        self.getGameType() #Set g_gametype in self.gamedata
        self.getCurrentMap() #set mapname in self.gamedata

        self.addPlayers()

        if self.config.botConfig['modded']:
            if 'broadcast:' not in self.Q.rcon("sv_sayprefix"):
                self.hasPrefix = True
            if 'broadcast:' not in self.Q.rcon("sv_demonotice"):
                self.hasDemo = True
            self.moddedSetup()

        self.Q.rcon("say ^3Startup complete.")
        log.info('SETUP DONE: BOT')

    def moddedSetup(self):
        if self.hasPrefix:
            self.Q.rcon('sv_sayprefix "%s: "' % self.config.botConfig['prefix'])
            self.Q.rcon('sv_tellprefix "%s [PM]: "' % self.config.botConfig['prefix'])
        if self.hasDemo:
            self.Q.rcon('sv_demonotice ""')

    def addPlayers(self):
        status = self.getStatus()
        if status != []:
            for i in status:
                log.debug('Add User: %s, %s' % (i, i[0]))
                uid = int(i[0])
                self.Clients[uid] = player.Player(uid, self.dumpUser(uid), self.api)
            self.updatePlayers() #Set team/score for players

    def parse(self, line):
        if 0 < len(self.logback) > 5: self.logback.popleft()
        self.logback.append(line)
        main.parse(line)

    def findByName(self, name):
        for client in [i for i in self.Clients.values() if i is not None]:
            log.debug('Name: %s, cname: %s' % (name, client.name))
            if client.name != None and name in client.name:
                return client
        return None