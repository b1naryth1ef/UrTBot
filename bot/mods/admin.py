from bot.config_handler import ConfigFile
from bot.main import BOT
from bot.api import listener, Event, command, A
from bot.debug import log
import sys, os, time

events = {
    'ban':Event('PLUGIN_ADMIN_BAN'),
    'kick':Event('PLUGIN_ADMIN_KICK')
}

@command('kick', 'Kick a user.', level=4)
def kickCmd(obj): #@DEV Clean this shit up!
	m = obj.msg.split(' ')
	cid = None
	reason = "No reason given"
	if len(m) in [2, 3]:
		if m[1].startswith('!') and m[1][1:].isdigit(): cid = int(m[1][1:])
		elif m[1].isdigit(): cid = int(m[1])
		else:
			q = BOT.findByName(m[1], approx=True)
			if q is not None:
				cid = q.cid
		if cid is not None and cid in BOT.Clients.keys():
			o = BOT.Clients[cid]
		else:
			obj.client.tell('^1Could not find user! Try again, and remember to place an exlamation point in front of CID\'s!')
   	 	if len(m) == 2:
   	 		reason = m[2]

   	 	A.Q3.kick(o, reason)
   	 	events['kick'].fire({'client':obj})
    else:
        obj.client.tell('Usage: ^1!kick ^3<cid/name> [reason]')

@command('ban', 'Permaban a user.', level=5, ['b'])
def banCmd(obj): pass

def init(B, A): pass
def run(): pass