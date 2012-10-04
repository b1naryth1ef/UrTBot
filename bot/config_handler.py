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


defaultcfg = {
'botConfig':{
    'prefix': "^1[^2BOT^1]: ",
    'cmd_prefix':'!',
    'cmd_on_team_say':True,
    'rcon': "MyPassword123",
    'rconip': "localhost:27960",
    'servercommand': "~/UrbanTerror/ioUrTded.i386 +set dedicated 2 +exec server.cfg" ,
    'serversocket': "/tmp/quake3_27961",
    'plugins':[],
    'leetlevel':5,
    'groups':[
        {'name':'guest', 'minlevel':0, 'maxlevel':1, 'levels':[]},
        {'name':'user', 'minlevel':1, 'maxlevel':2, 'levels':[]},
        {'name':'member', 'minlevel':1, 'maxlevel':3, 'levels':[]},
        {'name':'mod', 'minlevel':1, 'maxlevel':4, 'levels':[]},
        {'name':'admin', 'minlevel':1, 'maxlevel':5, 'levels':[]},
        {'name':'uberadmin', 'minlevel':1, 'maxlevel':6, 'levels':[]}
    ],
    'permissions':{
    },
},

'dbConfig':{
    'connecter':'peewee',
    'type':'sqlite',
    'name':'urtbot.db',
    'args':{},
},

'developerConfig':{
    'enabled':False,
    'logging':True,
    'logfile':'debug.log',
    'loglevel':'debug',   
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
                        'pak0^7', 'common-spog', 'zUrT42_0001',
                        'zUrT42_0002', 'zUrT42_0003', 'zUrT42_0004',
                        'zUrT42_0005', 'zUrT42_0006', 'zUrT42_0007',
                        'zUrT42_0008', 'zUrT42_0009']
}}

class ConfigFile():
    def __init__(self, configfile='config', default=None):
        self.configfile = configfile.replace('.cfg', '')
        self.default = default or defaultcfg
        self.config = self.load(self.default)

        self.check()
        self.save()

    def load(self, default):
        try:
            with open(self.configfile+'.cfg', 'r') as f:
                return json.loads(''.join(f.readlines()))
        except IOError:
            log.info('Creating config file!')
            return default
        except:
            raise Exception('Invalid config file! Please check your JSON formatting!')

    def save(self):
        s = json.dumps(self.config, sort_keys=True, indent=4)
        with open(self.configfile+'.cfg', 'w') as f:
            f.write(s)

    def check(self):
        def checkDict(a, b, rmv=False):
            mark = []
            for key in a:
                if key not in b:
                    if rmv: 
                        log.info('Removing key %s' % key)
                        mark.append(key)
                    else: 
                        log.info('Adding key %s' % key)
                        b[key] = a[key]
                if key in b and isinstance(b[key], dict):
                    return checkDict(a[key], b[key], rmv)
            for i in mark:
                del a[i]

        checkDict(self.default, self.config)
        checkDict(self.config, self.default, rmv=True)

    def __getitem__(self, attr):
        return self.config[attr]
   
    def __getattr__(self, attr):
        if attr in self.config.keys():
            return self.config[attr]
        return self.__dict__[attr]

