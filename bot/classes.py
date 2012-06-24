import socket, select, time, re, thread
import bot, player, const, database, main
from debug import log
from rcon import RCON
from collections import deque
import sys, os, time

class Bot():
    def __init__(self, config=None, database=None):
        self.prefix = config.botConfig['prefix']
        self.Q = RCON(config.botConfig['rconip'], config.botConfig['rcon'])
        self.database = database
        self.config = config

        self.enabled = True
        self.logback = deque()
        
        self.maplist = self.config.UrTConfig['maps']
        self.gameData = {}
        self.currentMap = None
        self.loadingMap = False
        self.justChangedMap = False

        self.hasPrefix = False
        self.hasDemo = False
        self.hasKickMsg = False

        self.redScore = 0
        self.blueScore = 0

        self.Clients = {} #AKA players
        self.curClients = lambda: [int(i[0]) for i in self.getStatus()]
        
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
    
    def getClient(self, uid): 
        if uid in self.Clients.keys():
            return self.Clients[uid]

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

    def getPlayers(self): #0: Eduardodias2012 BLUE k:9 d:11 ping:196 200.181.147.46:44453
        r = self.Q.rcon('players').split('\n')
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

        resp = self.Q3.say("^3Starting up...")
        if resp is None:
            log.critical('The server is not reachable. Check the ip/port and try again!')
        elif "No rconpassword set on the server." in resp:
            log.critical('The server does not have an rcon password check. Please check your server config and try again.')
            sys.exit()
        elif 'Bad rconpassword.' in resp:
            log.critical('The rcon password you provided was incorrect. Please double check it and try again.')
            sys.exit()
        
        self.maplist += [i for i in self.Q.rcon("sv_pakNames").split('"')[3].split() if i not in self.config.UrTConfig['ignoremaps']]

        self.getGameType() #Set g_gametype in self.gamedata
        self.getCurrentMap() #set mapname in self.gamedata

        self.addPlayers()

        if self.config.botConfig['modded']:
            if 'broadcast:' not in self.Q.rcon("sv_sayprefix"):
                log.info("Server has say/tell prefix!")
                self.hasPrefix = True

            if 'broadcast:' not in self.Q.rcon("sv_demonotice"):
                log.info("Server has demos!")
                self.hasDemo = True

            if self.Q.rcon('kick').split('\n')[1].split(' ')[-1] == "<reason>":
                log.info('Server has kick reasons!')
                self.hasKickMsg = True

            self.moddedSetup()

        self.Q3.say("^3Startup complete.")
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
            self.getPlayers() #Set team/score for players

    def getClientTeam(self): pass

    def parse(self, line):
        if 0 < len(self.logback) > 5: self.logback.popleft()
        self.logback.append(line)
        main.parse(line)

    def findByName(self, name, approx=False):
        for client in [i for i in self.Clients.values() if i is not None]:
            if client.name == None: return
            if approx and name in client.name: return client
            if client.name == name: return client