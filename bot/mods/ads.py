from bot.main import BOT
from bot.api import listener, Event, command, A, Q3
from bot.config_handler import ConfigFile
from datetime import datetime
import sys, os, time

adEvent = Event('PLUGIN_ADS_SPAM')
default_config = {
	'delay':80,
	'messages':[
	'Online Admins: ^1{admins}',
	'Time: ^1{time}',
	'Checkout UrTBot on github to peak into it\'s open-source goodness!',
	'Want help? Thats what googles for!',
	'Post bugs on github plz/ty!',
	]
}

config = ConfigFile(os.path.join('./', 'bot', 'mods', 'config', 'adsconfig.cfg'), default=default_config)
enabled = False

@command('adpause', 'Pause the adverts.', level=4)
def cmdPause(obj):
	enabled = False
	obj.client.tell('Adverts have been paused! Resume with adplay!')

@command('adplay', 'Play the adverts.', level=4)
def cmdPlay(obj):
	enabled = True
	obj.client.tell('Adverts have been resumed! Pause with adpause!')

def registerLoops():
	x = 0
	while True:
		if len(A.B.Clients) and enabled:
			varz = {
			'admins':'^3, ^1'.join([i.name for i in A.B.Clients.values() if i.client.group == A.config.botConfig['leetlevel']]),
			'time':datetime.now()
			}
			Q3.say(config['messages'][x].format(**varz))
			x += 1
			if x >= len(config['messages']): x=0
		time.sleep(config['delay'])

def init(B, Abc): pass
	# global A
	# A = B.A

def run():
	global enabled
	enabled = True


