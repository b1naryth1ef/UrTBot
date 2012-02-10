#from debug import log
import sys, os

checkKeys = ['botConfig', 'dbConfig', 'developerConfig', 'speed', 'UrTConfig']

header = 'config = '
footer = ''
default = {
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

'speed':{
	'threading':0, #0: Normal, 1: Low (Less threads), 2: High (More threads), 3: Insane (Thread all the things!)
	'max-threads':20, #Probablly just leave this. If your on threading mode 3, this will be ignored!
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

class ConfigFile():
	def __init__(self, configfile='config'):
		self.configfile = configfile
		self.config = self.open()
		self.fi = None

		self.check()
		self.loadVars()

	def loadVars(self):
		for key in self.config:
			self.__dict__[key] = self.config[key]

	def writeDict(self, dicty):
		self.fi = open(self.configfile+'.py', 'w')
		self.fi.write(header)
		self.fi.write(dicty.__str__())
		self.fi.write(footer)
		self.fi.close()

	def check(self):
		for key in default:
			if key not in self.config.keys():
				print '%s not in!' % key
				self.config[key] = default[key]
		for key in self.config:
			if key not in default:
				print '%s in!' % key
				del self.config[key]
		self.writeDict(self.config)

	def open(self):
		try: 
			return getattr(__import__(self.configfile), 'config')
		except ImportError, e:
			self.createDefaultConfig()
			return self.open()		

	def createDefaultConfig(self): self.writeDict(default)

