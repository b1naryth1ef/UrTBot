from bot.main import BOT
from bot.api import listener, Event, command, A, Q3
from bot.config_handler import ConfigFile
from datetime import datetime
from bot.debug import log
import sys, os, time

adEvent = Event('PLUGIN_ADS_SPAM')
default_config = {
	'delay':80,
	'messages':[
	'{admins}',
	'Time: ^1{time}',
	'Checkout UrTBot on github to peak into it\'s open-source goodness!',
	'Want help? Thats what googles for!',
	'Post bugs on github plz/ty!',
	],
	'deleted':[]
}

config = ConfigFile(os.path.join('./', 'bot', 'mods', 'config', 'adsconfig.cfg'), default=default_config)
enabled = False

@command('adlist', 'List all adverts.', level=4)
def cmdList(obj):
	obj.client.tell('Advert List:')
	for n, a in enumerate(config['messages']):
		if type(a) is tuple: a = "%s [%s]" % a
		obj.client.tell('%s: %s' % (n, a))

@command('adadd', 'Add an advert.', '<advert text>', level=4)
def cmdAdd(obj):
	m = obj.msg.split(' ', 1)
	if len(m) == 2:
		config['messages'].append((m[1], obj.sender.uid))
	else:
		obj.usage()

@command('addel', 'Delete an advert.', '<advert #>', level=4)
def cmdDel(obj):
	m = obj.msg.split(' ')
	if len(m) == 2 and m[1].isdigit():
		config['deleted'].append(config['messages'].pop(int(m[1])))
	else:
		obj.usage()

@command('adenable', 'Enable the adverts.', level=4)
def cmdEnable(obj):
	enabled = True
	obj.client.tell('Adverts enabled!')

@command('addisable', 'Disable the adverts.', level=4)
def cmdDisable(obj):
	enabled = False
	obj.client.tell('Adverts disabled!')

def registerLoops():
	x = 0
	while True:
		if len(A.B.Clients) and enabled:
			log.debug('Sending command because %s and len %s' % (enabled, len(A.B.Clients)))
			varz = {
			'admins':'^3, ^1'.join([i.name for i in A.B.Clients.values() if i.client.group == A.config.botConfig['leetlevel']]),
			'time':datetime.now()
			}
			for ad in config['messages']:
				if type(ad) is tuple: ad = ad[0]
				admins = 'Online Admins: '+'^3, ^1'.join(Q3.getAdminList())
				Q3.say(ad.format(time=datetime.now(), admins=admins))
				time.sleep(config['delay'])

def init(B, A): pass

def run():
	global enabled
	enabled = True

def stop():
	config.save()