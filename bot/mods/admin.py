from bot.config_handler import ConfigFile
from bot.main import BOT
from bot.api import listener, Event, command, A, Q3
from bot.debug import log
from datetime import datetime
from dateutil.relativedelta import relativedelta
import bot.database as database
import bot.const as const
import sys, os, time

events = {
    'ban':Event('PLUGIN_ADMIN_BAN'),
    'tempban':Event('PLUGIN_ADMIN_TEMPBAN'),
    'kick':Event('PLUGIN_ADMIN_KICK')
}

@command('rcon', 'Run an rcon command', '<rcon> [data]', level=4)
def rconCmd(obj):
    m = obj.msg.split(' ', 1)
    if len(m) == 2:
        c = Q3.R(m[1])
        if c: obj.client.tell('Output: %s' % c)
    else: obj.usage()

@command('kick', 'Kick a user.', '<{user}> [reason]', level=4, alias=['k'])
def kickCmd(obj): #!kick joe you are bad
    m = obj.msg.split(' ', 2)
    reason = "No reason given"
    if len(m) in [2, 3]:
        o = Q3.getObj(m[1], obj.client)
        if not o: return
        if len(m) == 3:
            reason = m[2]
        A.Q3.kick(o, reason)
        events['kick'].fire({'client':o})
    else:
        obj.usage()

@command('ban', 'Permaban a user.', '<{user}> [reason]', 5, ['b'])
def banCmd(obj): #!ban joe tsk tsk tsk
    m = obj.msg.split(' ')
    reason = "No reason given"
    if len(m) in [2, 3]:
        o = Q3.getObj(m[1], obj.client)
        if not o: return
        if len(m) == 3: reason = m[2]
        b = database.Ban(uid=o.client.id, by=obj.client.client, reason=reason, created=datetime.now(), until=datetime.now()+relativedelta(years=+10), active=True)
        b.save()
        A.Q3.kick(o, reason)
        events['ban'].fire({'client':o})
        events['kick'].fire({'client':o})
    else:
        obj.usage()

@command('tempban', 'Tempban a user.', '<{user}> <duration> [reason]', 5, ['tb'])
def tempbanCmd(obj):
    reason = "No reason given"
    m = obj.msg.split(' ', 3)
    if len(m) in [3, 4]:
        o = Q3.getObj(m[1], obj.client)
        if not o: return
        if len(m) == 4: reason = m[3]
        dur = const.timeparse(m[2])
        b = database.Ban(uid=o.client.id, by=obj.client.client, reason=reason, created=datetime.now(), until=datetime.now()+relativedelta(**dur), active=True)
        b.save()
        A.Q3.kick(o, reason)
        events['tempban'].fire({'client':o})
        events['kick'].fire({'client':o})
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
            b = [i for i in database.Ban.select().where(uid=qu[0].id, active=True)]
            if len(b):
                for i in b:
                    i.active = False
                    i.save()
                obj.client.tell('Successfully unbanned %s' % qu[0].name)
            else: obj.client.tell('^1No bans for %s' % qu[0].name)
        else: obj.client.tell('^1More than one user for that query!')
    else: obj.usage()

@command('leet', 'Become even more leet.', level=0, alias=['l33t'])
def leetCmd(obj):
    if not len([i for i in database.User.select().where(group=BOT.config.botConfig['leetlevel'])]):
        obj.client.client.group = BOT.config.botConfig['leetlevel']
        obj.client.client.save()
        obj.client.tell('Enjoy your ^1l33t^3ness!')
        log.info('User %s has gained uber-admin access through the !leet command!' % obj.client.name)
    else:
        obj.client.tell('^1Hahah nope!')
        log.debug('User %s tried gaining access with `!leet` command and was denied.' % obj.client.name)

@command('say', 'Say something.', '<[@]message>', 3, [BOT.config.botConfig['cmd_prefix']])
def sayCmd(obj):
    m = obj.msg.split(' ', 1)
    if len(m) == 2:
        if m[1].startswith('@'): m = "^5%s^1:^3 %s" % (obj.client.name, m[1][1:])
        else: m = m[1]
        Q3.say(m)
    else:
        obj.usage()

@command('tell', 'Tell something.', '{user} <[@]message>', 3)
def tellCmd(obj):
    m = obj.msg.split(' ', 2)
    if len(m) == 3:
        o = Q3.getObj(m[1], obj.client)
        if not o: return
        if m[2].startswith('@'): m = "^5%s^1:^3 %s" % (obj.client.name, m[2][1:])
        else: m = m[2]
        Q3.tell(o, m)
    else:
        obj.usage()
        
@command('info', 'Get info on a user.', '{user}', 3)
def infoCmd(obj):
    m = obj.msg.split(' ')
    if len(m) == 2:
        o = Q3.getObj(m[1], obj.client)
        if not o: return
        out = 'Info for ^1%s^3\n---------------------\nUID: ^1%s\n^3CID: ^1%s\n^3IP: ^1%s\n^3GUID: ^1%s' % (o.name, o.uid, o.cid, o.ip, o.cl_guid)
        [obj.client.tell(i) for i in out.split('\n')]
    else:
        obj.usage()
def init(blah, blaski):
    if len([i for i in database.User.select().where(group=BOT.config.botConfig['leetlevel'])]):
        A.removeCommand(leetCmd)
def run(): pass