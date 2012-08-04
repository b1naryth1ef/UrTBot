from bot.config_handler import ConfigFile
from bot.main import BOT
from bot.api import listener, Event, command, A, Q3
from bot.debug import log
from datetime import datetime
from dateutil.relativedelta import relativedelta #@TODO get rid of this dep
import bot.database as database
import bot.const as const
import sys, os, time

default_config = {
    'block_1337':True
}

events = {
    'ban':Event('PLUGIN_ADMIN_BAN'),
    'tempban':Event('PLUGIN_ADMIN_TEMPBAN'),
    'kick':Event('PLUGIN_ADMIN_KICK')
}

config = ConfigFile(os.path.join(A.configs_path, 'adminconfig.cfg'), default=default_config)
kicks = []

@command('map', 'Load a map!', '<map>', level=4)
def mapCmd(obj):
    m = obj.msg.split(' ', 1)
    if len(m) == 2:
        res = []
        for item in A.B.maplist:
            if m[1] in item: res.append(item)
        if len(res) == 1: Q3.R('map %s' % res[0])
        elif len(res) == 0: obj.client.tell('No map for %s found!' % m[1])
        elif len(res) == 2: obj.client.tell('More than one map for %s found!' % m[1])
    else:
        obj.usage()

@command('setgroup', 'Set a users group!', '<{user}> <group>', level=4)
def setgroupCmd(obj):
    m = obj.msg.split(' ', 2)
    if len(m) == 3:
        o = Q3.getObj(m[1], obj.client.tell)
        if not o: return
        if o == obj.client: return obj.client.tell('You cant set your own group silly!')
        lc = []
        for l, g in enumerate(A.B.config.botConfig['groups']):
            if m[2] in g['name']: lc.append(l)
        if len(lc) == 0: return obj.client.tell('No group %s' % m[2])
        elif len(lc) > 2: return obj.client.tell('More than one group!')
        else: 
            o.user.group = lc[0]
            o.user.save()
            obj.client.tell('User %s successfully put in group %s' % (o.name, lc[0]))
    else: obj.usage()

@command('force', 'Use the force broski!', '<{user}> <team> [lock]', level=4, alias=['f']) #@TODO Should change desc if not a.hasPlugin('fairplay')
def forceCmd(obj):
    m = obj.msg.split(' ', 3)
    if len(m) >= 3:
        o = Q3.getObj(m[1], obj.client.tell)
        if not o: return
        t = const.findTeam(m[2])
        Q3.R('forceteam %s %s' % (o.cid, t.urt))
        if len(m) == 4 and A.hasPlugin('fairplay'):
            o.locked = t
    else: obj.usage()

@command('rcon', 'Run an rcon command.', '<rcon> [data]', level=4)
def rconCmd(obj):
    m = obj.msg.split(' ', 1)
    if len(m) == 2:
        c = Q3.R(m[1])
        if c: 
            c = c.split('\n')
            if len(c) <= 15:
                obj.client.tell('Output:')
                for line in c:
                    obj.client.tell(line)
                time.sleep(.2)
    else: obj.usage()

@command('slap', 'Slap dat ass!', '<{user}> [amount]', level=5, alias=['s'])
@command('nuke', 'Nuke dat hoe!', '<{user}> [amount]', level=5, alias=['n'])
def slapCmd(obj): #!slap 0 10 blah
    m = obj.msg.split(' ', 2)
    if len(m) >= 2:
        o = Q3.getObj(m[1], obj.client.tell)
        if not o: return
        count, stime = 1, 1
        if len(m) == 3:
            if m[2].isdigit(): count = int(m[2])
            elif m[2].startswith(':') and m[2][1:].isdigit(): 
                count = int(m[2][1:])
                stime = .3
        if count > 20: count = 20
        if not isinstance(o, list): o = [o]
        for i in range(0, count):
            A.Q3.R('%s %s' % (obj._obj['name'], o.cid))
            time.sleep(stime)
    else:
        obj.usage()

@command('kick', 'Kick a user.', '<{user}> [reason]', level=4, alias=['k'])
def kickCmd(obj): #!kick joe you are bad
    m = obj.msg.split(' ', 2)
    reason = "No fucks given"
    if len(m) in [2, 3]:
        o = Q3.getObj(m[1], obj.client.tell)
        if not o: return
        if len(m) == 3: reason = m[2]
        database.Penalty(user=o.user, admin=obj.client.user, penalty="kick", reason=reason, creation_date=datetime.now(), expire_date=datetime.now(), active=False).save()
        A.Q3.kick(o, reason)
        events['kick'].fire({'client':o})
    else:
        obj.usage()

@command('ban', 'Ban/Tempban a user. (-1 duration for permaban)', '<{user}> <duration> [reason]', 5, ['b'])
def banCmd(obj):
    m = obj.msg.split(' ', 3)
    reason = "No reason given"
    if len(m) in [3, 4]:
        o = Q3.getObj(m[1], obj.client.tell)
        if not o: return
        if len(m) == 4: reason = m[3]
        if m[2] == "-1": dur = datetime.now()+relativedelta(years=+50)
        else: dur = datetime.now()+relativedelta(**const.timeparse(m[2]))
        database.Penalty(user=o.user, admin=obj.client.user, penalty="ban", reason=reason, creation_date=datetime.now(), expire_date=dur, active=True).save()
        events['ban'].fire({'client':o})
        events['kick'].fire({'client':o})
        A.Q3.kick(o, reason)
    else:
        obj.usage()

@command('unban', 'Unban a user.', '<name/@uid>', 5, ['ub'])
def unbanCmd(obj):
    m = obj.msg.split(' ')
    if len(m) == 2:
        if m[1].startswith('@') and m[1][1:].isdigit(): q = {'id':int(m[1][1:])}
        else: q = {'name':m[1]}
        qu = [i for i in database.User.select().where(**q)]
        if len(qu) == 1:
            b = [i for i in database.Penalty.select().where(user=qu[0], penalty="ban",  active=True)]
            if len(b):
                for i in b:
                    i.active = False
                    i.save()
                obj.client.tell('^1Successfully unbanned ^3%s' % qu[0].name)
            else: obj.client.tell('^1No bans for ^3%s' % qu[0].name)
        elif len(qu) == 0: obj.client.tell('^1More than one user for that query!')
        else: obj.client.tell('^1More than one user for that query (%s users)!' % len(qu))
    else: obj.usage()

@command('leet', 'Become even more leet.', level=0, alias=['l33t'])
def leetCmd(obj):
    if not len([i for i in database.User.select().where(group=BOT.config.botConfig['leetlevel'])]):
        obj.client.user.group = BOT.config.botConfig['leetlevel']
        obj.client.user.save()
        obj.client.tell('Enjoy your ^1l33t^3ness!')
        log.info('User %s has gained uber-admin access through the !leet command!' % obj.client.name)
    else:
        obj.client.tell('^1Hahah nope!')
        log.debug('User %s tried gaining access with `!leet` command and was denied.' % obj.client.name)

@command('say', 'Say something.', '<[@]message>', 3, [BOT.config.botConfig['cmd_prefix']])
def sayCmd(obj):
    m = obj.msg.split(' ', 1)
    if len(m) == 2:
        if m[1].startswith('@'): m = m[1][1:] 
        else: m = "^5%s^1:^3 %s" % (obj.client.name, m[1])
        Q3.say(m)
    else:
        obj.usage()

@command('tell', 'Tell something.', '{user} <[@]message>', 3)
def tellCmd(obj):
    m = obj.msg.split(' ', 2)
    if len(m) == 3:
        o = Q3.getObj(m[1], obj.client.tell)
        if not o: return
        if m[2].startswith('@'): m = m[2][1:] 
        else: m = "^5%s^1:^3 %s" % (obj.client.name, m[2])
        Q3.tell(o, m)
    else:
        obj.usage()
        
@command('info', 'Get info on a user.', '<{user}>', 4)
def infoCmd(obj):
    m = obj.msg.split(' ')
    if len(m) == 2:
        o = Q3.getObj(m[1], obj.client.tell)
        if not o: return
        out = 'Info for ^1%s^3\n---------------------\nUID: ^1%s\n^3CID: ^1%s\n^3IP: ^1%s\n^3GUID: ^1%s' % (o.name, o.uid, o.cid, o.ip, o.cl_guid)
        [obj.client.tell(i) for i in out.split('\n')]
    else:
        obj.usage()

@command('list', "List the online users.", '', 4)
def listCmd(obj):
    obj.client.tell('Online Users: ')
    for i in A.B.Clients.values():
        i = (i.name, i.cid, i.uid, i.ip, datetime.now()-i.user.lastjoin)
        obj.client.tell('^1Name: ^3%s ^1CID: ^3%s ^1UID: ^3%s ^1IP: ^3%s ^1ONLINE-FOR: ^3%s' % i)

@command('stopdemo', 'Stop a demo.', '<{user}>', 3)
@command('startdemo', 'Start a demo.', '<{user}>', 3)
def demoCmd(obj):
    m = obj.msg.split(' ')
    if len(m) == 2:
        act = 'startserverdemo' if obj._obj['name'] == 'startdemo' else 'stopserverdemo'
        if m[1] == '*':o = 'all'
        else: 
            o = Q3.getObj(m[1], obj.client.tell)]
            if not o: return
            o = o.cid
        Q3.rcon("%s %s" % (act, o))
        obj.client.tell('Started server demo for %s!' % o)
    else:
        obj.usage()

@command('admins', 'Find those more sexy than you', '', [0, 1])
def adminsCmd(obj):
    obj.client.tell('Admins: ^1'+'^3, ^1'.join(Q3.getAdminList()))

@command('help', 'Get some help!', '[command]', [0, 1])
def helpCmd(obj):
    m = obj.msg.split(' ')
    if len(m) == 2:
        if m[1].lower() in A.commands.keys(): cmd = A.commands[m[1].lower()]
        elif m[1].lower() in A.aliases.keys(): cmd = A.commands[A.aliases[m[1].lower()]]
        else: obj.client.tell("No such command %s!" % m[1])
        obj.client.tell("%s: %s" % (cmd['name'], cmd['desc']))
    else:
        obj.client.tell('Help Listing: ')
        for cmd in A.commands.values():
            if A.hasAccess(obj.client, cmd): 
                obj.client.tell('%s: %s' % (cmd['name'], cmd['desc']))
                time.sleep(0.5)

@command('alias', 'Find aliases of the user.', '<{user}>', 3)
def cmdAlias(obj):
    m = obj.msg.split(' ')
    if len(m) == 2:
        o = Q3.getObj(m[1], obj.client.tell)
        if not o: return
        q = [i.real for i in database.Alias.select().where(user=o.user)]
        obj.client.tell('Aliases of %s: ^1%s' % (o.name, '^3, ^1'.join(q)))
    else:
        obj.usage()

@command('smite', 'Smite a user!', '<{user}> [msg]', 5, ['kill'])
def cmdSmite(obj):
    m = obj.msg.split(' ', 2)
    if len(m) >= 2:
        o = Q3.getObj(m[1], obj.client.tell)
        if not o: return
        Q3.smite(o)
        if len(m) == 3:
            o.tell(msg[2:])
    else: obj.usage()

def clientInfoSetListener(obj):
    if obj.client.ip.split(':')[-1] == "1337": obj.client.kick()

def onEnable(): pass
def onDisable(): pass
def onBoot():
    if config.block_1337:
        A.addListener('CLIENT_INFO_SET', clientInfoSetListener)
    if len([i for i in database.User.select().where(group=BOT.config.botConfig['leetlevel'])]):
        A.removeCommand(leetCmd)