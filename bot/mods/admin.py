from bot.config_handler import ConfigFile
from bot.main import BOT
from bot.api import listener, Event, command, A, Q3
from bot.debug import log
import bot.database as database
import sys, os, time

events = {
    'ban':Event('PLUGIN_ADMIN_BAN'),
    'kick':Event('PLUGIN_ADMIN_KICK')
}

@command('kick', 'Kick a user.', level=4)
def kickCmd(obj): #@DEV Clean this shit up!
    m = obj.msg.split(' ')
    reason = "No reason given"
    log.debug(':> %s, %s' % (m, len(m)))
    if len(m) in [2, 3]:
        o = Q3.getObj(m[1])
        if not o:
            obj.client.tell('^1Could not find user! Try again, and remember to place an @ in front of numbered names!')
        if len(m) == 3:
            reason = m[2]
        A.Q3.kick(o, reason)
        events['kick'].fire({'client':o})
    else:
        obj.client.tell('Usage: ^1!kick ^3<cid/name/@name> [reason]')

@command('ban', 'Permaban a user.', 5, ['b'])
def banCmd(obj): pass

@command('leet', 'Become even more leet.', 0, ['l33t'])
def leetCmd(obj):
    if not len([i for i in database.User.select().where(group=BOT.config.botConfig['leetlevel'])]):
        obj.client.client.group = BOT.config.botConfig['leetlevel']
        obj.client.client.save()
        obj.client.tell('Enjoy your ^1l33t^3ness!')
        log.info('User %s has gained uber-admin access through the !leet command!' % obj.client.name)
    else:
        obj.client.tell('^1Hahah nope!')
        log.debug('User %s tried gaining access with `!leet` command and was denied.' % obj.client.name)

@command('say', 'Say something.', 3, [BOT.config.botConfig['cmd_prefix']])
def sayCmd(obj):
    m = obj.msg.split(' ', 1)
    BOT.Q3.say(m[1])

@command('tell', 'Tell something.', 3)
def tellCmd(obj):
    m = obj.msg.split(' ', 2)
    o = Q3.getObj(m[1])
    if len(m) == 3:
        if o:
            BOT.Q3.tell(o, m[2])
        else:
            BOT.Q3.tell(obj.client, "Could not find client!")
    else:
        BOT.Q3.tell(obj.client, 'Usage: ^1!tell ^3<cid/name/@name> <message>')
        
def init(B, A):
    if len([i for i in database.User.select().where(group=BOT.config.botConfig['leetlevel'])]):
        A.removeCommand(leetCmd)
def run(): pass