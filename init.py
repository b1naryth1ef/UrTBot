#!/usr/bin/python

#--HEADER GLOBALS--#
config = None
log = None

#---IMPORTS---#
import subprocess, time, os, sys, imp, player, string, re, socket
import const, database, select, thread, events, thread_handler, debug
from start import _version_
from events import *
from classes import Bot, API
from wrapper import GameOutput
from thread_handler import fire
from config_handler import ConfigFile


#--SETTRZ--#
A = None
home = os.getcwd()
lastsent = None
keepLoop = True
botDEBUGS = []
pluginDEBUGS = []

#--GLOB--#
config_prefix = None
config_rcon = None
config_rconip = None
config_bootcommand = None
config_groups = None
config_plugins = None
config_serversocket = None

def canInt(i): return str(i).isdigit() #@DEV Just a depricated function... Replace for beta

def command(cmd, desc='None', level=0, alias=[]): #WOOT! DECORATERS ARE THE SHIZ
    def decorator(target):
        if cmd in BOT.Commands.keys(): return None
        BOT.Commands[cmd] = (target,desc,level)
        for i in alias:
            BOT.Aliases[i] = (target,desc,level,cmd)
        return target
    return decorator

def listener(event): #WOOT! DECORATERS ARE THE SHIZ
    def decorator(target):
        if event in BOT.Listeners.keys():
            if BOT.Listeners[event] != None: 
                BOT.Listeners[event].append(target)
                return target
        BOT.Listeners[event] = [target]
        return target
    return decorator

def parseInitGame(inp, varz={}):
    options = re.findall(r'\\([^\\]+)\\([^\\]+)', inp)
    for o in options:
        varz[o[0]] = o[1]
    return varz
      
def parseTimeLimitHit(inp):
    BOT.updatePlayers()
    BOT.matchEnd()

def parseUserInfo(inp, varz={}):
    inp2 = inp.split(' ', 2)
    uid = int(inp2[1])
    var = re.findall(r'\\([^\\]+)\\([^\\]+)', inp)
    for i in var:
        varz[i[0]] = i[1]
    if 'name' in varz.keys():
        varz['nick'] = varz['name']
        varz['name'] = varz['name'].lower()
    return uid,varz
    
def parseUserInfoChange(inp, varz={}, vary={}):
    #r is race, n is name, t is team
    #ClientUserinfoChanged: 0 n\[WoC]*WolfXxXBunny\t\3\r\0\tl\0\f0\\f1\\f2\\a0\0\a1\0\a2\255
    inp2 = inp.split(' ', 2)
    uid = int(inp2[1])
    var = re.findall(r'([^\\]+)\\([^\\]+)', inp2[2])
    for i in var:
        varz[i[0]] = i[1]
    if 't' in varz.keys(): vary['team'] = const.teams[int(varz['t'])]
    if 'n' in varz.keys(): vary['name'] = varz['n'].lower()
    return uid,vary

def parseKill(inp):
    #Kill: 1 0 15: WolfXxXBunny killed [WoC]*B1naryth1ef by UT_MOD_DEAGLE
    inp = inp.split(" ")
    inp.pop(0)
    attacker = int(inp[0])
    if attacker == 1022: atkobj = None #We're world. Setting this None might break shit (but hopefully not)
    else: atkobj = BOT.Clients[attacker] #We're a player
    victim = int(inp[1])
    vicobj = BOT.Clients[victim]
    method = int(inp[2][:-1])
    if method in [1, 3, 9, 39]: BOT.eventFire('CLIENT_WORLDDEATH', {'vic':victim, 'meth':method}) #Water, lava, trigger_hurt or flag (hot patato)
    elif method in [7, 6, 10, 31, 32]: #Various suicides
        BOT.eventFire('CLIENT_SUICIDE', {'vic':victim, 'meth':method})
        vicobj.die(method)
    elif atkobj.team == vicobj.team and atkobj.name != vicobj.name: BOT.eventFire('CLIENT_TEAMKILL', {'atk':attacker, 'vic':victim, 'meth':method})
    else:
        BOT.eventFire('CLIENT_KILL', {'atk':attacker, 'vic':victim, 'meth':method})
        BOT.eventFire('CLIENT_GENERICDEATH', {'vic':victim})

def parseHit(inp):
    #Hit: 1 0 2 21: Skin_antifa(fr) hit Antho888 in the Torso
    inp = inp.split(' ')
    attacker = inp[1]
    victim = inp[2]
    hitloc = inp[3]
    method = inp[4]
    BOT.eventFire('CLIENT_HIT', {'atk':attacker, 'vic':victim, 'loc':hitloc, 'meth':method})

def parseItem(inp):
    #Item: 1 ut_weapon_ump45
    inp = inp.split(' ')
    item = inp[2].strip()
    client = inp[1]
    if item in const.flagtypes.keys(): BOT.eventFire('GAME_FLAGPICKUP', {'client':client, 'flag':item, 'team':const.flagtypes[item], 'flagid':const.flagtypes[item]})
    else: BOT.eventFire('CLIENT_PICKUPITEM', {'item':item, 'client':client})

def parsePlayerBegin(inp):
    #ClientBegin: 0
    inp = inp.split(' ')
    client = int(inp[1])
    BOT.eventFire('CLIENT_BEGIN', {'client':client})

def parseFlag(inp):
    #Flag: 0 2: team_CTF_redflag
    inp = inp.split(' ', 3)
    cid = inp[1]
    action = int(inp[2].strip(':'))
    flag = inp[3].strip()
    flagid = const.flagtypes[flag]
    if action == 0: BOT.eventFire('GAME_FLAGDROP', {'client':cid, 'actionid':action, 'action':const.flagactions[action], 'flag':flag, 'flagid':flagid}) #drop
    elif action == 1: BOT.eventFire('GAME_FLAGRETURN', {'client':cid, 'actionid':action, 'action':const.flagactions[action], 'flag':flag, 'flagid':flagid}) #return
    elif action == 2: BOT.eventFire('GAME_FLAGCAPTURE', {'client':cid, 'actionid':action, 'action':const.flagactions[action], 'flag':flag, 'flagid':flagid}) #score

def parseFlagReturn(inp):
    inp = inp.split(' ', 3)
    flag = inp[2].strip()
    BOT.eventFire('GAME_FLAGRESET', {'flag':flag, 'flagid':const.flagtypes[flag]})

def parseCommand(inp, cmd):
    uid = int(inp[0])
    log.info('User %s sent command %s with level %s' % (BOT.Clients[uid].name, cmd, BOT.Clients[uid].group))
    if BOT.getClient(uid).group >= BOT.Commands[cmd][2]:
        obj = BOT.eventFire('CLIENT_COMMAND', {'sender':inp[0], 'sendersplit':inp[0].split(' '), 'msg':inp[2], 'msgsplit':inp[2].split(' '), 'cmd':cmd})
        thread.start_new_thread(BOT.Commands[cmd][0], (obj, time.time())) 
    else:
        msg = "You lack sufficient access to use %s [%s]" % (cmd, BOT.Clients[uid].group)
        BOT.Q.rcon("tell %s %s %s " % (inp[0], BOT.prefix, msg))

def parseUserKicked(inp):
    time.sleep(5)
    cur = BOT.curClients()
    for i in BOT.Clients.keys():
        print i, cur
        if i not in cur:
            print 'SENDING CLIENT_KICKED'
            BOT.eventFire('CLIENT_KICKED', {'client':i})

def parse(inp):
    global BOT
    if inp.startswith("say:"):
        #say: 0 [WoC]*B1naryth1ef: blah blah
        inp = inp.split(" ", 3)
        inp.pop(0)
        inp[1] = inp[1].strip(':')
        if inp[2].startswith('!'):
            inp[2] = inp[2].lower()
            BOT.eventFire('CLIENT_COMMAND', {'event':'CHAT_MESSAGE', 'name':inp[1].lower(), 'sender':inp[0], 'msg':inp[2]}) #@FIX ffs dont fire chat_message fire command!
            cmd = inp[2].rstrip().split(' ')[0]
            if cmd in BOT.Commands.keys(): parseCommand(inp, cmd)
            if cmd in BOT.Aliases.keys(): parseCommand(BOT.Aliases[inp][3])
        BOT.eventFire('CHAT_MESSAGE', {'event':'CHAT_MESSAGE', 'sender':inp[1], 'gid':inp[0], 'msg':inp[2]})

    elif inp.startswith('ClientConnect:'):
        #ClientConnect: 0
        inp = int(inp.split(" ")[1])
        if inp in BOT.Clients.keys():
            #'til we find ways to work around the missing ClientDisconnect messages... this won't be fatal. 
            #raise const.UrTBotError('Client #%s is already connected... Something is wrong.' % (inp))
            if BOT.loadingMap is False and BOT.justChangedMap is False:
                print const.UrTBotError('Client #%s is already connected... Something is wrong. Flush \'em, danno!' % (inp))
                del BOT.Clients[inp]
            else:
                BOT.justChangedMap = False
        if inp >= 0: BOT.eventFire('CLIENT_CONNECT', {'client':inp})

    elif inp.startswith('ClientUserinfo:'):
        uid, varz = parseUserInfo(inp)
        if uid in BOT.Clients.keys(): fire('update_clientinfo', BOT.Clients[uid].updateData, (varz,))
        else:
            BOT.Clients[uid] = player.Player(uid, varz, A)
            if BOT.Clients[uid].cl_guid != None:
                #BOT.pdb.playerUpdate(BOT.Clients[uid], True) WTF DOES THIS DO?
                #db.tableSelect('penalties', 'userid')
                log.info('User %s connected with Game ID %s and Database ID %s' % (BOT.Clients[uid].name, BOT.Clients[uid].uid, BOT.Clients[uid].cid))
                #en2 = db.rowFindAll(BOT.Clients[uid].cid)
                # if en2 != None:
                #     for en in en2:
                #         if en != None:
                #             if en['type'] == 'ban' and en['status'] == 1:
                #                 print 'Disconnecting user because he/she has been banned'
                #                 return BOT.Q.rcon('kick %s' % uid)
                #             elif en['type'] == 'tempban' and en['status'] == 1:
                #                 #print float(time.time())-float(en['expiration'])
                #                 if float(time.time())-float(en['expiration']) < 0:
                #                     print 'Disconnecting user because he/she has been tempbanned'
                #                     return BOT.Q.rcon('kick %s' % uid)
                #                 else:
                #                     print 'Setting tempban unactive'
                #                     db2 = database.DB()
                #                     db2.tableSelect('penalties')
                #                     enx = db2.rowFind(en['id'])
                #                     enx['status'] = 0
                #                     db2.rowUpdate(enx)
                #                     db2.commit()
            BOT.eventFire('CLIENT_CONNECTED', {'client':uid})

    elif inp.startswith('ClientUserinfoChanged:'): 
        # Different than ClientUserinfo because we don't add clients to the list or DB, just update
        uid, varz = parseUserInfoChange(inp, {}, {})
        if uid in BOT.Clients.keys(): fire('update_clientinfo', BOT.Clients[uid].updateData, (varz,))
    elif inp.startswith('ClientDisconnect:'):
        inp = int(inp.split(" ")[1])
        BOT.eventFire('CLIENT_DISCONNECT', {'client':inp})
        if inp in BOT.Clients.keys(): del BOT.Clients[inp]
    elif inp.startswith('Kill:'): parseKill(inp)
    elif inp.startswith('Hit:'): parseHit(inp)
    elif inp.startswith('Item'): parseItem(inp)
    elif inp.startswith('Flag:'): parseFlag(inp)
    elif inp.startswith('Flag Return:'): parseFlagReturn(inp)
    elif inp.startswith('ClientBegin:'): parsePlayerBegin(inp)
    elif inp.startswith('ShutdownGame:'):
        BOT.eventFire('GAME_SHUTDOWN', {})
        BOT.matchEnd()
        # We clear out our client list on shutdown. Doesn't happen with 'rcon map ..' but does
        # when the mapcycle changes maps? hrmph. investigate.
        # In fact I'm not sure how to detect an 'rcon map' yet! Geeeeeez.
        # rcon from 127.0.0.1:
        # map
        # That should work ye?
        # for key in BOT.Clients.keys():
        #     BOT.eventFire('CLIENT_DISCONNECT', {'client':key})
        #     del BOT.Clients[key]
        # ^^^ Dont run that because then a map change is treated as new clients connecting. Not sure how to fix that stuffz
    elif inp.startswith('InitGame:'): 
        fire('parse_initgame', BOT.gameData.update, (parseInitGame(inp),))
        BOT.matchNew()
    elif inp.startswith('InitRound:'): BOT.roundNew()
    elif inp.startswith('SurvivorWinner:'): 
        BOT.roundEnd()
        if int(BOT.gameData['g_gametype']) in [4, 8]: BOT.eventFire('GAME_ROUND_END', {}) #<<< Will this work?
        else: log.warning('Wait... Got SurvivorWinner but we\'re not playing Team Surivivor or bomb?')
    elif inp.startswith('InitRound:'): pass
    elif inp.startswith('clientkick') or inp.startswith('kick'): #@DEV This needs to be fixed in beta
        log.debug('Seems like a user was kicked... Threading out parseUserKicked()')
        fire('parse_userkicked', parseUserKicked, (inp,)) #Threaded because we have to delay sending out CLIENT_KICKED events slightly
    elif inp.startswith('Exit: Timelimit hit.'): parseTimeLimitHit(inp)

def loadConfig(cfg):
    """Loads the bot config"""
    global log, config_prefix, config_rcon, config_rconip, config_bootcommand, config_plugins, config_groups, config_serversocket, config_debugmode, config
    try:
        botConfig = config.botConfig
        config_prefix = botConfig['prefix']
        config_rcon = botConfig['rcon']
        config_rconip = botConfig['rconip']
        config_bootcommand = botConfig['servercommand']
        config_plugins = botConfig['plugins']
        config_groups = botConfig['groups']
        config_serversocket = botConfig['serversocket']
        config_debugmode = botConfig['debug_mode']
    except Exception, e:
        log.critical('Error loading main config... [%s]' % e)
        sys.exit()

def loadMods():
    global BOT, A
    for i in config_plugins:
        log.info('Loading plugin %s...' % i)
        __import__('mods.'+i)
        i = sys.modules['mods.'+i]
        try: 
            fire('module_init', i.init, ())
            log.info('Loaded mod %s' % i)
        except Exception, e:
            A.warning('Error loading mod %s [%s]' % (i, e))

def loop():
    """Round and round in circles we go!"""
    global proc, keepLoop
    while True:
        proc.checkAndRead()
        while proc.hasLine():
            line = proc.getLine()
            if line != '^1Error: weapon number out of range':
                print line
            parse(line)

def Start():
    global BOT, proc, A, config_debugmode, db, config, log
    config = ConfigFile()
    thread_handler.init(config)
    loadConfig(config)
    log = debug.init(config)
    BOT = Bot(config_prefix, config_rconip, config_rcon, config_debugmode, config=config)
    A = API() #@TODO Fix this bullshit
    BOT.Startup()
    loadMods()
    proc = GameOutput(config_serversocket)
    
    db = database.init(config)

    x = os.uname()
    A.say('UrTBot V%s loaded on %s (%s/%s)' % (_version_, sys.platform, x[2], x[4]))

    loop()

def Exit(): sys.exit()

if __name__ == "__main__":
    print "Use start.py to start everything or we'll trololololol, and die!"
