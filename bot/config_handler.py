try: from bot.debug import log
except: 
    class LawlLog():
        def _p(self, msg): print msg
        debug = _p
        warning = _p
        info = _p
        error = _p
        critical = _p
    log = LawlLog()
import sys, os, time
import pprint, json


default = {
'botConfig':{
    'prefix': "^1[^2BOT^1]:",
    'cmd_prefix':'!',
    'mode':0,
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
    'connecter':'peewee',
    'type':'sqlite',
    'database':'/tmp/urtbot.db',
},

'developerConfig':{
    'logging':True,
    'logfile':'debug.log',
    'loglevel':'debug',
    'enabled':True,
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
        self.config = self.load()

        self.check()
        self.save()

    def load(self):
        try:
            with open(self.configfile+'.cfg', 'r') as f:
                return json.loads(''.join(f.readlines()))
        except:
           log.warning('Invalid or incorrect config file loaded, creating new!')
           return default

    def save(self):
        s = json.dumps(self.config, sort_keys=True, indent=4)
        with open(self.configfile+'.cfg', 'w') as f:
            f.write(s)

    def check(self):
        for key in default:
            if key not in self.config.keys():
                log.warning('Could not find %s key! Adding to config...')
                self.config[key] = default[key]
            if type(default[key]) is dict:
                for _key in default[key].keys():
                    if _key not in self.config[key].keys():
                        log.warning('Could not find subkey %s of %s. Adding...' % (key, _key))
                        self.config[key][_key] = default[key][_key]
        for key in self.config:
            if key not in default:
                log.warning('Found key %s which is no longer needed! Removing...')
                del self.config[key]
            if type(default[key]) is dict:
                for _key in self.config[key].keys():
                    if _key not in default[key].keys():
                        log.warning('Extra subkey %s of %s. Removing...' % (key, _key))
                        del self.config[key][_key]

    def __getitem__(self, attr):
        return self.config[attr]
   
    def __getattr__(self, attr):
        if attr in self.config.keys():
            return self.config[attr]
        return self.__dict__[attr]

