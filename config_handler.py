#from debug import log
import sys, os

default = """
config = {
'botConfig':{
	'prefix': "^1[^2BOT^1]:",
	'rcon': "MyPassword123",
	'rconip': "localhost:27960",
	'servercommand': "~/UrbanTerror/ioUrTded.i386 +set dedicated 2 +exec server.cfg" ,
	'serversocket': "/tmp/quake3_27961",
	'plugins':[],
	'groups':{
		'unsub':0,
		'user':1,
		'member':2,
		'mod':3,
		'admin':4,
		'uberadmin':5
	},
	'debug_mode':True
},

'dbConfig':{
	'database':'/tmp/urtbot_beta.db',
},

'developerConfig':{
	'logging':True,
	'logfile':'debug.log',
	'loglevel':'debug'
},

'UrTConfig':{
    # Maps that don't have their own PK3
    'maps' : [ 'ut4_abbey','ut4_abbeyctf','ut4_algiers','ut4_ambush',
    'ut4_austria','ut4_casa','ut4_company','ut4_crossing','ut4_docks',
    'ut4_dressingroom','ut4_eagle','ut4_elgin','ut4_firingrange',
    'ut4_harbortown','ut4_herring','ut4_horror','ut4_kingdom','ut4_mandolin',
    'ut4_maya','ut4_oildepot','ut4_prague','ut4_ramelle','ut4_ricochet',
    'ut4_riyadh','ut4_sanc','ut4_snoppis','ut4_suburbs','ut4_subway',
    'ut4_swim','ut4_thingley','ut4_tombs','ut4_toxic','ut4_tunis',
    'ut4_turnpike','ut4_uptown' ],
    # PK3s that aren't actually maps
    'ignoremaps' : [ 'zpak000', 'zpak000_assets', 'zpak001_assets',
                        'pak0^7', 'common-spog']
}}
"""

class ConfigFile():
	def __init__(self, configfile='config'):
		self.configfile = configfile
		self.f = self.open()
		self.config = self.loadVars()

	def loadVars(self): return self.f.config

	def open(self):
		try: 
			__import__('config')
			return sys.modules['config']
		except ImportError, e:
			self.createDefaultConfig()
			return self.open()
		

	def createDefaultConfig(self):
		self.f = open(self.configfile+'.py', 'w')
		self.f.write(default)
		self.f.close()
