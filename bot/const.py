import re, time

flagtypes = {
'team_CTF_redflag':1,
'team_CTF_blueflag':2,
'RED':1,
'BLUE':2,
}

flagactions = {
0:'drop',
1:'return',
2:'score'    
}

GAMETYPE_FFA = 0
GAMETYPE_TDM = 3
GAMETYPE_TS = 4
GAMETYPE_FTL = 5
GAMETYPE_CAH = 6
GAMETYPE_CTF = 7
GAMETYPE_BM = 8

gametypes = {
0: 'ffa', #free for all
1: None,
2: None,
3: 'tdm', #Team death match
4: 'ts', #Team survivor
5: 'ftl', #Follow the leader
6: 'cah', #Capture and hold
7: 'ctf', #Capture the flag
8: 'bm' #Bomb
}


# Method Of Death (MODs)
MOD_WATER = {'id':'1'}
MOD_SLIME = {'id': '2'}
MOD_LAVA= {'id':'3'}
MOD_CRUSH= {'id':'4'}
MOD_TELEFRAG = {'id':'5'}
MOD_FALLING= {'id':'6'}
MOD_SUICIDE= {'id':'7'} # Dupe with 11
MOD_TARGET_LASER= {'id':'8'}
MOD_TRIGGER_HURT= {'id':'9'}
MOD_CHANGE_TEAM= {'id':'10'}
#MOD_SUICIDE={'id':'11'} # Dupe
UT_MOD_KNIFE= {'id':'12'}
UT_MOD_KNIFE_THROWN= {'id':'13'}
UT_MOD_BERETTA= {'id':'14'}
UT_MOD_DEAGLE= {'id':'15'}
UT_MOD_SPAS= {'id':'16'}
UT_MOD_UMP45= {'id':'17'}
UT_MOD_MP5K= {'id':'18'}
UT_MOD_LR300= {'id':'19'}
UT_MOD_G36= {'id':'20'}
UT_MOD_PSG1= {'id':'21'}
UT_MOD_HK69= {'id':'22'}
UT_MOD_BLED= {'id':'23'}
UT_MOD_KICKED= {'id':'24'}
UT_MOD_HEGRENADE= {'id':'25'}
UT_MOD_FLASHGRENADE= {'id':'26'}
UT_MOD_SMOKEGRENADE= {'id':'27'}
UT_MOD_SR8= {'id':'28'}
UT_MOD_SACRIFICE= {'id':'29'}
UT_MOD_AK103= {'id':'30'}
UT_MOD_SPLODED= {'id':'31'}
UT_MOD_SLAPPED= {'id':'32'}
UT_MOD_BOMBED= {'id':'33'}
UT_MOD_NUKED= {'id':'34'}
UT_MOD_NEGEV= {'id':'35'}
UT_MOD_HK69_HIT= {'id':'37'}
UT_MOD_M4= {'id':'38'}
UT_MOD_FLAG= {'id':'39'}
UT_MOD_GOOMBA= {'id':'40'}


HITS = {
 1: 'UT_MOD_KNIFE',
 2: 'UT_MOD_BERETTA',
 3: 'UT_MOD_DEAGLE',
 4: 'UT_MOD_SPAS',
 5: 'UT_MOD_MP5K',
 6: 'UT_MOD_UMP45',
 8: 'UT_MOD_LR300',
 9: 'UT_MOD_G36',
 10: 'UT_MOD_PSG1',
 14: 'UT_MOD_SR8',
 15: 'UT_MOD_AK103',
 17: 'UT_MOD_NEGEV',
 19: 'UT_MOD_M4',
 21: 'UT_MOD_HEGRENADE'
}

HITZONES = {
0:'head',
1:'helmet',
2:'torso',
3:'kevlar',
4:'arms',
5:'legs',
6:'body',
}

# Hitzones
""" verbatim:
13:57 Hit: 2 1 5 9: chouille hit killgirl in the Legs
Read the hit sequence as follows
Chouille is client 1
KillGirl is client 2
5 is the hit area (here the legs)
9 is the weapon ID
"""

DAMAGES = { 
    'PASSIVE': [0, 0, 0, 0, 0, 0, 0, 0],
    MOD_TELEFRAG['id']: [0, 0, 0, 0, 0, 0, 0, 0],
    UT_MOD_KNIFE['id']: [100, 60, 44, 35, 20, 20, 44, 100],
    UT_MOD_KNIFE_THROWN['id']: [100, 60, 44, 35, 20, 20, 44, 100],
    UT_MOD_BERETTA['id']: [100, 34, 30, 20, 11, 11, 30, 100],
    UT_MOD_DEAGLE['id']: [100, 66, 57, 38, 22, 22, 57, 100],
    UT_MOD_SPAS['id']: [25, 25, 25, 25, 25, 25, 25, 100],
    UT_MOD_UMP45['id']: [100, 51, 44, 29, 17, 17, 44, 100],
    UT_MOD_MP5K['id']: [50, 34, 30, 20, 11, 11, 30, 100],
    UT_MOD_LR300['id']: [100, 51, 44, 29, 17, 17, 44, 100],
    UT_MOD_G36['id']: [100, 51, 44, 29, 17, 17, 44, 100],
    UT_MOD_PSG1['id']: [100, 63, 97, 63, 36, 36, 97, 100],
    UT_MOD_HK69['id']: [50, 50, 50, 50, 50, 50, 50, 100],
    UT_MOD_BLED['id']: [15, 15, 15, 15, 15, 15, 15, 15],
    UT_MOD_KICKED['id']: [20, 20, 20, 20, 20, 20, 20, 100],
    UT_MOD_HEGRENADE['id']: [50, 50, 50, 50, 50, 50, 50, 100],
    UT_MOD_SR8['id']: [100, 100, 100, 100, 50, 50, 100, 100],
    UT_MOD_AK103['id']: [100, 58, 51, 34, 19, 19, 51, 100],
    UT_MOD_NEGEV['id']: [50, 34, 30, 20, 11, 11, 30, 100],
    UT_MOD_HK69_HIT['id']: [20, 20, 20, 20, 20, 20, 20, 100],
    UT_MOD_M4['id']: [100, 51, 44, 29, 17, 17, 44, 100],
    UT_MOD_GOOMBA['id']: [100, 100, 100, 100, 100, 100, 100, 100],
    }

GEARS = {
    
 #Sidearms  
 'F':{'id':UT_MOD_BERETTA['id'], 'name':'Beretta', 'damage':DAMAGES[UT_MOD_BERETTA['id']]}, 
 'G':{'id':UT_MOD_DEAGLE['id'],'name':'Desert Eagle', 'damage':DAMAGES[UT_MOD_DEAGLE['id']]},

    
 #Primary  
 'K':{'id':UT_MOD_HK69['id'], 'name':'HK69', 'damage': DAMAGES[UT_MOD_HK69['id']]},  
 'L':{'id':UT_MOD_LR300['id'], 'name':'LR300', 'damage': DAMAGES[UT_MOD_LR300['id']]},
 'M':{'id':UT_MOD_G36['id'], 'name':'G36', 'damage': DAMAGES[UT_MOD_G36['id']]},
 'N':{'id':UT_MOD_PSG1['id'], 'name':'PSG1','damage': DAMAGES[UT_MOD_PSG1['id']]},
 'Z':{'id':UT_MOD_SR8['id'],'name':'SR8','damage': DAMAGES[UT_MOD_SR8['id']]},
 'a':{'id':UT_MOD_AK103['id'],'name':'AK103','damage': DAMAGES[UT_MOD_AK103['id']]},
 'c':{'id':UT_MOD_NEGEV['id'],'name':'Negav','damage': DAMAGES[UT_MOD_NEGEV['id']]},
 'e':{'id':UT_MOD_M4['id'],'name':'M4','damage': DAMAGES[UT_MOD_M4['id']]},

 #Primary and Secondary   
 'H':{'id':UT_MOD_SPAS['id'],'name':'Spas', 'damage': DAMAGES[UT_MOD_SPAS['id']]},
 'I':{'id':UT_MOD_MP5K['id'],'name':'MP5k', 'damage': DAMAGES[UT_MOD_MP5K['id']]},
 'J':{'id':UT_MOD_UMP45['id'],'name':'UMP45', 'damage': DAMAGES[UT_MOD_UMP45['id']]},

 #Grenades
 'O':{'id':UT_MOD_HEGRENADE['id'], 'name':'HE Grenade', 'damage': DAMAGES[UT_MOD_HEGRENADE['id']]},
 'Q':{'name':'Smoke Grenade'}, #{'id':None,'name':'smoke grenade','damage': DAMAGES['PASSIVE']}, #Smoke nade

    
 #Items
 'R':{'name':'Kevlar Vest'}, #Kevlar vest
 'S':{'name':'Tac Goggles'}, #TAC Goggles
 'T':{'name':'Medkit'}, #Medkit
 'Y':{'name':'Silencer'}, #Silencer
 'V':{'name':'Laser Sight'}, #laser sight
 'W':{'name':'Kevlar Helmet'}, #kevlar helmet
 'X':{'name':'Extra Ammo'}, #extra ammo

 #Etc
 'U':None, #idk 
 'A':None #None :D
}

def timeparse(timestr):
    fin = [[]]
    a = {'h':0, 'm':0, 's':0, 'd':0, 'w':0, 'y':0}
    for i in timestr:
        fin[-1].append(i)
        if not i.isdigit():
            fin.append([])
    fin = [''.join(i) for i in fin]
    for i in fin:
        if i[-1:] in a.keys():
            a[i[-1:]] = int(i[:-1])
    return {'hours':a['h'], 'minutes':a['m'], 'seconds':a['s'], 'days':a['d'], 'weeks':a['w'], 'years':a['y']}

class UrTBotError(Exception): pass
class ConfigError(Exception): pass
class UrbanTerrorError(Exception): pass

def switchTeam(team):
    x = {'blue':RED_TEAM, 'red':BLUE_TEAM}
    if team.shortName in x: return x[team.shortName]
    else: return UNK_TEAM

def getItemID(item): return globals()[item.upper()]['id']
Glob = lambda: globals()

rconGameType = '.*?(\\d+).*?\\d+.*?(\\d+)'
rconCurrentMap = re.compile(r'.*?(?:[a-z][a-z0-9_]*).*?(?:[a-z][a-z0-9_]*).*?(?:[a-z][a-z0-9_]*).*?((?:[a-z][a-z0-9_]*))', re.IGNORECASE|re.DOTALL)
rconStatus = re.compile(r'^(?P<slot>[0-9]+)\s+(?P<score>[0-9-]+)\s+(?P<ping>[0-9]+)\s+(?P<guid>[0-9a-zA-Z]+)\s+(?P<name>.*?)\s+(?P<last>[0-9]+)\s+(?P<ip>[0-9.]+):(?P<port>[0-9-]+)\s+(?P<qport>[0-9]+)\s+(?P<rate>[0-9]+)$', re.I)
rexConnectWith = re.compile(r'.*?(\\d+)')

"""
Some content in this file has been found in the B3 source. 
We thank the entire BigBrotherBot team for there contributions 
to the Urban Terror community, and credit much of the data/content 
in this file to them.

And credit to utstatsbot for sorting most of this out and collecting it together.
http://utstatsbot.googlecode.com/svn-history/r2/trunk/ut.log.format.txt
"""

class Team():
    def __init__(self, nice, code, longn, urt, color="^3"):
        self.color = color
        self.shortName = nice
        self.abbrv = self.shortName[0]
        self.id = code
        self.longName = longn
        self.urt = urt

    def __eq__(self, other):
        if isinstance(other, int):
            if other == self.id: return True
        elif isinstance(other, Team):
            if other.id == self.id: return True
        elif isinstance(other, str):
            if len(other) == 1 and self.abbrv == other: return True
            elif other == self.longName or other == self.shortName: return True
        return False

    def __int__(self):
        return self.id

    def __repr__(self):
        return '%s%s' % (self.color, self.longName)

RED_TEAM = Team('red', 1, 'Red Team', 'red', '^1')
BLUE_TEAM = Team('blue', 2, 'Blue Team', 'blue', '^4')
SPEC_TEAM = Team('spec', 3, 'Spectator', 'spectator', '^7')
UNK_TEAM = Team('unk', -1, 'Unknown', 'none')

teams_text = {
    'spectator':3,
    'blue':2,
    'red':1,
}

teams = {
1:RED_TEAM,
2:BLUE_TEAM,
3:SPEC_TEAM,
-1:UNK_TEAM
}

def findTeam(t):
    if t.isdigit() and int(t) in teams.keys():
        return teams[int(t)]
    else:
        for i in teams.values():
            if t in i.shortName: return i
            elif t in i.longName: return i