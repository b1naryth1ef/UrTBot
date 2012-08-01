#!/usr/bin/python

#--HEADER GLOBALS--#
config = None
log = None

#---IMPORTS---#
import sys, time, os, subprocess, imp, re, socket, select, threading
import const, player, debug, database, api
import thread_handler as thread
from datetime import datetime
from bot.classes import Bot
from wrapper import GameOutput
from bot.config_handler import ConfigFile

#--SETTRZ--#
A = None
home = os.getcwd()
keepLoop = True
modules = []

#--GLOB--#
config_plugins = None
config_serversocket = None

#--RENDERING ACTIONS--#
def renderUserInfo(inp):
    varz = {}
    inp2 = inp.split(' ', 2)
    uid = int(inp2[1])
    var = re.findall(r'\\([^\\]+)\\([^\\]+)', inp)
    for i in var:
        varz[i[0]] = i[1]
    if 'name' in varz.keys():
        varz['nick'] = varz['name']
        varz['name'] = varz['name'] #.lower()
    return uid,varz
    
def renderUserInfoChange(inp):
    #r is race, n is name, t is team
    #ClientUserinfoChanged: 0 n\[WoC]*WolfXxXBunny\t\3\r\0\tl\0\f0\\f1\\f2\\a0\0\a1\0\a2\255
    varz, vary = {}, {}
    inp2 = inp.split(' ', 2)
    uid = int(inp2[1])
    var = re.findall(r'([^\\]+)\\([^\\]+)', inp2[2])
    for i in var:
        varz[i[0]] = i[1]
    if 't' in varz.keys(): vary['team'] = const.teams[int(varz['t'])]
    if 'n' in varz.keys(): vary['name'] = varz['n'] #.lower()
    return uid,vary

#--PARSING ACTIONS--#
def parseSay(inp): #say: 0 [WoC]*B1naryth1ef: blah blah
    inp = inp.split(' ', 3)[1:]
    info = {'name':inp[1][:-1], 'client':BOT.getClient(int(inp[0])), 'msg':inp[2]}
    if len(inp) > 2 and info['msg'].startswith(botConfig['cmd_prefix']):
        api.A.fireEvent('CLIENT_SAY_CMD', info)
        api.A.fireCommand(inp[2][1:].rstrip().split(' ')[0], info)
    api.A.fireEvent('CLIENT_SAY_GLOBAL', info)

def parseSayTeam(inp): #sayteam: 0 `SoC-B1nzy: yay?
    inp = inp.split(' ', 3)[1:]
    info = {'name':inp[1][:-1], 'client':BOT.getClient(int(inp[0])), 'msg':inp[2]}
    if len(inp) > 2 and info['msg'].startswith(botConfig['cmd_prefix']) and botConfig['cmd_on_team_say'] is True:
        api.A.fireEvent('CLIENT_SAY_CMD', info)
        api.A.fireCommand(inp[2][1:].rstrip().split(' ')[0], info)
    api.A.fireEvent('CLIENT_SAY_TEAM', info)

#@CHECK 4.2
def parseReconnect(inp): #68.255.111.133:27960:reconnect
    ip = inp.strip(':reconnect')
    for cli in BOT.Clients.values():
        if ip == cli.ip:
            log.debug('Client #%s is reconnecting!' % cli.cid)
            BOT.removeClient(cli.cid)
            api.A.fireEvent('CLIENT_CONN_RECONNECT', {'cid':cli.cid})    
            return
    log.debug('Reconnect has no client with matching ip %s' % ip)

def parseClientConnect(inp): #ClientConnect: 0
    cid = int(re.findall('ClientConnect\: ([0-9]+)', inp)[0])
    api.A.fireEvent('CLIENT_CONN_CONNECT', {"cid":cid})

def parseClientUserInfo(inp):
    cid, varz = renderUserInfo(inp)
    if cid in BOT.Clients.keys():
        api.A.fireEvent('CLIENT_INFO_CHANGE')
        thread.fireThread(BOT.Clients[cid].setData, varz)
    else:
        log.debug('Got join CUI for #%s' % cid)
        BOT.Clients[cid] = player.Player(cid, varz, api)
        BOT.Clients[cid].setData(BOT.dumpUser(cid))
        if BOT.Clients[cid].cl_guid != None:
            log.info('User %s connected with Game ID %s and Database ID %s' % (BOT.Clients[cid].name, BOT.Clients[cid].cid, BOT.Clients[cid].uid))
            pen = [i for i in database.Penalty.select().where(user=BOT.Clients[cid].user, expire_date__gt=datetime.now(), penalty="ban", active=True)]
            if len(pen):
                for p in pen:
                    log.info('Disconnecting user %s because they have an outstanding ban!' % BOT.Clients[cid].name)
                    BOT.Clients[cid].kick(p.reason)
        BOT.Clients[cid].waitingForBegin = True
        f = {'client':BOT.getClient(cid), 'info':varz}
        #api.A.fireEvent('CLIENT_CONN_CONNECTED', f)
        api.A.fireEvent('CLIENT_INFO_SET', f)

def parseClientUserInfoChanged(inp):
    cid, varz = renderUserInfoChange(inp)
    thread.fireThread(BOT.Clients[cid].setData, varz)
    api.A.fireEvent('CLIENT_INFO_CHANGE', {'client': BOT.getClient(cid), 'info':varz})

def parseClientDisconnect(inp): #ClientDisconnect: 0
    cid = int(re.findall('ClientDisconnect\: ([0-9+])', inp)[0])
    log.debug('ClientDisconnect: %s' % cid)
    api.A.fireEvent('CLIENT_CONN_DC_GEN', {'client':BOT.getClient(cid)})
    BOT.removeClient(cid)

def parseKill(inp):
    #Kill: 1 0 15: WolfXxXBunny killed [WoC]*B1naryth1ef by UT_MOD_DEAGLE
    inp = inp.split(" ")[1:]
    attacker = int(inp[0])
    if attacker == 1022: atkobj = None #We're world.
    else: atkobj = BOT.Clients[attacker] #We're a player
    victim = int(inp[1])
    vicobj = BOT.Clients[victim]
    method = int(inp[2][:-1])
    if method in [1, 3, 9, 39]: api.A.fireEvent('CLIENT_DIE_WORLD', {'vic':victim, 'meth':method}) #Water, lava, trigger_hurt or flag (hot patato)
    elif method in [7, 6, 10, 31, 32]: #Various suicides
        if method == 10: vicobj.checkTeam() #Team switch
        api.A.fireEvent('CLIENT_DIE_SUICIDE', {'vic':victim, 'meth':method})
    elif atkobj.team == vicobj.team and atkobj.name != vicobj.name: 
        api.A.fireEvent('CLIENT_KILL_TK', {'atk':attacker, 'vic':victim, 'meth':method})
        api.A.fireEvent('CLIENT_DIE_TK', {'atk':attacker, 'vic':victim, 'meth':method})
    else:
        api.A.fireEvent('CLIENT_KILL_GEN', {'atk':attacker, 'vic':victim, 'meth':method})
        api.A.fireEvent('CLIENT_DIE_GEN', {'vic':victim})

def parseHit(inp):
    #Hit: 1 0 2 21: Skin_antifa(fr) hit Antho888 in the Torso
    inp = inp.split(' ')
    info = {'atk':BOT.getClient(int(inp[1])), 'vic':BOT.getClient(int(inp[2])), 'loc':int(inp[3]), 'meth':int(inp[4][:-1])}
    api.A.fireEvent('CLIENT_HIT_ATK', info)

def parseItem(inp):
    #Item: 1 ut_weapon_ump45
    inp = inp.split(' ')
    item = inp[2].strip()
    client = int(inp[1])
    if item in const.flagtypes.keys(): api.A.fireEvent('GAME_FLAG_PICKUP', {'client':BOT.getClient(client), 'flag':item, 'team':const.flagtypes[item], 'flagid':const.flagtypes[item]})
    else: api.A.fireEvent('CLIENT_ITEM_PICKUP', {'item':item, 'client':BOT.getClient(client)})

def parseFlag(inp):
    #Flag: 0 2: team_CTF_redflag
    inp = inp.strip().replace(':', '').split(' ', 3)
    actionid = int(inp[2])
    data = {'client':BOT.getClient(int(inp[1])), 'actionid':actionid, 'action':const.flagactions[action], 'flag':inp[3], 'flagid':const.flagtypes[flag]}
    api.A.fireEvent(['GAME_FLAG_DROP', 'GAME_FLAG_RETURN', 'GAME_FLAG_CAPTURE'][actionid], {'client':BOT.getClient(int(inp[1])), 'actionid':action, 'action':actionid, 'flag':flag, 'flagid':flagid})

def parseFlagReturn(inp):
    inp = inp.strip().split(' ', 3)
    api.A.fireEvent('GAME_FLAG_RETURN', {'flag':inp[2], 'flagid':const.flagtypes[inp[2]]})

def parseHotPotato(inp): #Hotpotato:
    api.A.fireEvent('GAME_FLAG_HOTPOTATO', {})

def parseCallVote(inp): #Callvote: 1 - "map dressingroom"
    inp = re.findall('Callvote: ([0-9]+) - "([0-9a-zA-Z ]+)"', inp)[0]
    cli = BOT.getClient(int(inp[0]))
    vote = inp[1]
    api.A.fireEvent('GAME_VOTE_CALL', {'client':cli, 'vote':vote})

def parseVote(inp): #Vote: 0 - 2
    inp = inp.split(' ')
    cid, vote = int(inp[1]), int(inp[3])
    api.A.fireEvent('CLIENT_GEN_VOTE', {'client':BOT.getClient(cid), 'vote':vote})

def parseRadio(inp): #Radio: 0 - 7 - 2 - "New Alley" - "I'm going for the flag"
    inp = inp.split('Radio: ')[-1].split(' - ')
    cli = BOT.getClient(int(inp[0]))
    msg = [int(inp[1]), int(inp[2])]
    api.A.fireEvent('CLIENT_GEN_RADIO', {'client': cli, 'msg': msg, 'loc':inp[3], "text":inp[4]})

def parsePlayerBegin(inp): 
    cli = BOT.getClient(int(inp.split(' ')[1]))
    if cli.waitingForBegin:
        api.A.fireEvent('CLIENT_CONN_CONNECTED', {'client:'BOT.getClient(cid)})

def parseShutdownGame(inp): #@FIXME need better rcon msgs before I can do this
    api.A.fireEvent('GAME_SHUTDOWN', {})
    if BOT.logback[0] in ['cyclemap' or 'map']: BOT.matchEnd()
    else: log.debug('Sounds like server is going down...')
    log.debug('SHUTDOWN WITH %s' % BOT.logback[0])

def parseInitGame(inp):
    BOT.matchNew(dict(re.findall(r'\\([^\\]+)\\([^\\]+)', inp)))
    
def parseInitRound(inp):
    BOT.roundNew()

def parseSurvivorWinner(inp):
    if int(BOT.gameData['g_gametype']) in [const.GAMETYPE_TS, const.GAMETYPE_BM, const.GAMETYPE_FTL]: 
        BOT.roundEnd()
    else: log.warning('Wait... Got SurvivorWinner but we\'re not playing TS, BM, or FTL?')

def parseClientKick(inp): #@FIXME Hopefully barb will add some better debug
    def _user_kicked(inp):  
        time.sleep(5)
        cur = BOT.curClients()
        for i in BOT.Clients.keys():
            if i not in cur:
                api.A.fireEvent('CLIENT_CONN_DISCONNECT_KICKED', {'cid':i})
                log.debug('User was indeed kicked!')
    log.debug('Seems like a user was kicked... Threading out parseUserKicked()')
    thread.fireThread(_user_kicked, inp)
    
def parseTimeLimitHit(inp):
    BOT.getPlayers()
    BOT.matchEnd()

#@TODO 4.2
def parseAccountKick(inp): pass
def parseAccountBan(inp): pass
def parseAccountValidated(inp): pass
def parseAccountRejected(inp): pass
#def parseCallVote(inp): pass
#def parseRadio(inp): pass
#def parseHotPotato(inp): pass
#def parseVote(inp): pass

def parse(inp):
    global BOT
    if inp.startswith("say:"): parseSay(inp)
    elif inp.startswith("sayteam:"): parseSayTeam(inp)
    #@TODO 4.2 this should all wait tell we have a working demo
    elif inp.startswith("AccountKick:"): parseAccountKick(inp)
    elif inp.startswith("AccountBan:"): parseAccountBan(inp)
    elif inp.startswith("AccountValidated:"): parseAccountValidated(inp)
    elif inp.startswith("AccountRejected:"): parseAccountRejected(inp)
    elif inp.endswith(':reconnect'): parseReconnect(inp) #@CHECK 4.2
    elif inp.startswith('ClientConnect:'): parseClientConnect(inp)
    elif inp.startswith('ClientUserinfo:'): parseClientUserInfo(inp)
    elif inp.startswith('ClientUserinfoChanged:'): parseClientUserInfoChanged(inp)
    elif inp.startswith('ClientDisconnect:'): parseClientDisconnect(inp)
    elif inp.startswith('Kill:'): parseKill(inp)
    elif inp.startswith('Hit:'): parseHit(inp)
    elif inp.startswith('Item'): parseItem(inp)
    elif inp.startswith('Flag:'): parseFlag(inp)
    elif inp.startswith('Flag Return:'): parseFlagReturn(inp)
    elif inp.startswith('Hotpotato:'): parseHotPotato(inp) #@CHECK 4.2
    elif inp.startswith("Callvote:"): parseCallVote(inp) #@CHECK 4.2
    elif inp.startswith('Vote:'): parseVote(inp) #@CHECK 4.2
    elif inp.startswith("Radio:"): parseRadio(inp) #@CHECK 4.2
    elif inp.startswith('ClientBegin:'): parsePlayerBegin(inp)
    elif inp.startswith('ShutdownGame:'): parseShutdownGame(inp)
    elif inp.startswith('InitGame:'): parseInitGame(inp)
    elif inp.startswith('InitRound:'): parseInitRound(inp)
    elif inp.startswith('SurvivorWinner:'): parseSurvivorWinner(inp)
    elif inp.startswith('clientkick') or inp.startswith('kick'): parseClientKick(inp) #@DEV Hopefully 4.2 provides a fix for this
    elif inp.startswith('Exit: Timelimit hit.'): parseTimeLimitHit(inp)

def loadConfig(cfg):
    """Loads the bot config"""
    global log, config_plugins, config_serversocket, config, botConfig
    try:
        botConfig = config.botConfig
        config_plugins = botConfig['plugins']
        config_serversocket = botConfig['serversocket']
    except Exception, e:
        log.critical('Error loading main config... [%s]' % e)
        sys.exit()

def loadMods():
    global BOT, config
    for name in config_plugins:
        log.info('Loading plugin %s' % name)
        __import__('bot.mods.'+name)
        i = sys.modules['bot.mods.'+name]
        BOT.A.addModule(name, i)
        try: 
            if hasattr(i, 'onBoot'): thread.fireThread(i.onBoot)
            log.info('Loaded plugin %s' % i.__name__)
            modules.append(i)
        except Exception, e:
            log.warning('Error loading plugin %s [%s]' % (i, e))

def loop():
    """Round and round in circles we go!"""
    global proc, keepLoop, BOT
    while True:
        proc.checkAndRead()
        while proc.hasLine():
            line = proc.getLine()
            if line != '^1Error: weapon number out of range':
                print line
            BOT.parse(line)

def Start(_version_, cfgfile):
    global BOT, proc, A, config_debugmode, db, config, log
    config = ConfigFile(cfgfile)
    loadConfig(config)
    log = debug.init(config)
    db = database.setup(config, log)
    BOT = Bot(config=config, database=db)

    api.setup(BOT)
    BOT.Startup(api)
    api.A.B = BOT
    A = api.A
    loadMods()
    api.A.finishBooting(BOT, config)
    proc = GameOutput(config_serversocket)
    
    x = os.uname()
    api.Q3.say('^3UrTBot V%s loaded on %s (%s/%s)' % (_version_, sys.platform, x[2], x[4]))
    if config.developerConfig['enabled']: loop()
    else:
        try: loop()
        except: sys.exit()

if __name__ == "__main__":
    print "Use start.py to start everything or we'll trololololol, and die!"