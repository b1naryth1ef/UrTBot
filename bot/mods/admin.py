from bot.config_handler import ConfigFile
from bot.main import BOT
from bot.api import listener, Event, command, A, Q3
from bot.debug import log
from datetime import datetime
from dateutil.relativedelta import relativedelta
import bot.database as database
import sys, os, time

events = {
    'ban':Event('PLUGIN_ADMIN_BAN'),
    'kick':Event('PLUGIN_ADMIN_KICK')
}

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
        events['kick'].fire({'client':0})
    else:
        obj.usage()

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
        
def init(blah, blaski):
    if len([i for i in database.User.select().where(group=BOT.config.botConfig['leetlevel'])]):
        A.removeCommand(leetCmd)
def run(): pass