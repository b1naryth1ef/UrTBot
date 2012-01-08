import re, time

teams = {
1:'red',
2:'blue',
3:'spec'
}

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
UT_MOD_FLASHGRENADE= {'id':'26'} #@DEV It is technically possible to die from this, I guarantee it!
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

# Hits (yes these differ from the kill ones, go fig)
"""
1	UT_MOD_KNIFE
2	UT_MOD_BERETTA
3	UT_MOD_DEAGLE
4	UT_MOD_SPAS
5	UT_MOD_MP5K
6	UT_MOD_UMP45
8	UT_MOD_LR300
9	UT_MOD_G36
10	UT_MOD_PSG1
14	UT_MOD_SR8
15	UT_MOD_AK103
17	UT_MOD_NEGEV
19	UT_MOD_M4
21	UT_MOD_HEGRENADE
"""

# Hitzones
""" verbatim:
13:57 Hit: 2 1 5 9: chouille hit killgirl in the Legs
Read the hit sequence as follows
Chouille is client 1
KillGirl is client 2
5 is the hit area (here the legs)
9 is the weapon ID

Hit areas are:
0: Head
1: Helmet
2: Torso
3: Kevlar
4: Arms
5: Legs
6: Body
"""

# Items (pickupable)
# These don't have an integer attached to them, they just 'are'
"""
UT_WEAPON_M4
UT_WEAPON_GRENADE_FRAG
UT_WEAPON_NEGEV
UT_WEAPON_BOMB
UT_WEAPON_AK103
UT_WEAPON_SR8
UT_WEAPON_GRENADE_SMOKE
UT_WEAPON_GRENADE_FLASH
UT_WEAPON_GRENADE_HE
UT_WEAPON_PSG1
UT_WEAPON_G36
UT_WEAPON_LR
UT_WEAPON_HK69
UT_WEAPON_UMP45
UT_WEAPON_MP5K
UT_WEAPON_SPAS12
UT_WEAPON_DEAGLE
UT_WEAPON_BERETTA
UT_WEAPON_KNIFE
UT_WEAPON_BOMB
UT_ITEM_APR
UT_ITEM_EXTRAAMMO
UT_ITEM_HELMET
UT_ITEM_LASER
UT_ITEM_SILENCER
UT_ITEM_MEDKIT
UT_ITEM_NVG
UT_ITEM_VEST
UT_ITEM_BOMB
"""

damage = {
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

gearInfo = {
	#Sidearms
	'F':{'id':UT_MOD_BERETTA['id'], 'name':'beretta', 'damage':damage[UT_MOD_BERETTA['id']]},
	'G':{'id':UT_MOD_DEAGLE['id'],'name':'desert eagle', 'damage':damage[UT_MOD_DEAGLE['id']]},

	#Primary
	'K':{'id':UT_MOD_HK69['id'], 'name':'hk69', 'damage': damage[UT_MOD_HK69['id']]},
	'L':{'id':UT_MOD_LR300['id'], 'name':'lr300', 'damage': damage[UT_MOD_LR300['id']]},
	'M':{'id':UT_MOD_G36['id'], 'name':'g36', 'damage': damage[UT_MOD_G36['id']]},
	'N':{'id':UT_MOD_PSG1['id'], 'name':'psg1','damage': damage[UT_MOD_PSG1['id']]},
	'Z':{'id':UT_MOD_SR8['id'],'name':'sr8','damage': damage[UT_MOD_SR8['id']]},
	'a':{'id':UT_MOD_AK103['id'],'name':'ak103','damage': damage[UT_MOD_AK103['id']]},
	'c':{'id':UT_MOD_NEGEV['id'],'name':'negav','damage': damage[UT_MOD_NEGEV['id']]},
	'e':{'id':UT_MOD_M4['id'],'name':'m4','damage': damage[UT_MOD_M4['id']]},

	#Primary and Secondary
	'H':{'id':UT_MOD_SPAS['id'],'name':'spas', 'damage': damage[UT_MOD_SPAS['id']]},
	'I':{'id':UT_MOD_MP5K['id'],'name':'mp5k', 'damage': damage[UT_MOD_MP5K['id']]},
	'J':{'id':UT_MOD_UMP45['id'],'name':'ump45', 'damage': damage[UT_MOD_UMP45['id']]},

	#Grenades
	'O':{'id':UT_MOD_HEGRENADE['id'], 'name':'he grenade', 'damage': damage[UT_MOD_HEGRENADE['id']]},
	'Q':None, #{'id':None,'name':'smoke grenade','damage': damage['PASSIVE']}, #Smoke nade

	#Items
	'R':None, #Kevlar vest
	'S':None, #TAC Goggles
	'T':None, #Medkit
	'Y':None, #Silencer
	'V':None, #laser sight
	'W':None, #kevlar helmet
	'X':None, #extra ammo

	'A':None #None :D
}

def timeparse(timeStr): #CREDIT TO B3
    if not timeStr:
        return 0
    elif type(timeStr) is int:
        return timeStr

    timeStr = str(timeStr)
    if not timeStr:
        return 0
    elif timeStr[-1:] == 'h':
        return minutes2int(timeStr[:-1]) * 60
    elif timeStr[-1:] == 'm':
        return minutes2int(timeStr[:-1])
    elif timeStr[-1:] == 's':
        return minutes2int(timeStr[:-1]) / 60
    elif timeStr[-1:] == 'd':
        return minutes2int(timeStr[:-1]) * 60 * 24
    elif timeStr[-1:] == 'w':
        return minutes2int(timeStr[:-1]) * 60 * 24 * 7
    else:
        return minutes2int(timeStr)

def minutes2int(mins): #CREDIT TO B3
    if re.match('^[0-9.]+$', mins):
        return round(float(mins), 2)
    else:
        return 0

class UrTBotError(Exception): pass
class ConfigError(Exception): pass
class UrbanTerrorError(Exception): pass

def switchTeam(team):
	x = {'blue':'red', 'red':'blue', None:'spec'}
	return x[team]
def getItemID(item): return globals()[item.upper()]['id']
Glob = lambda: globals()

rconGameType = '.*?(\\d+).*?\\d+.*?(\\d+)'
rconCurrentMap = re.compile(r'.*?(?:[a-z][a-z0-9_]*).*?(?:[a-z][a-z0-9_]*).*?(?:[a-z][a-z0-9_]*).*?((?:[a-z][a-z0-9_]*))', re.IGNORECASE|re.DOTALL)
rconStatus = re.compile(r'^(?P<slot>[0-9]+)\s+(?P<score>[0-9-]+)\s+(?P<ping>[0-9]+)\s+(?P<guid>[0-9a-zA-Z]+)\s+(?P<name>.*?)\s+(?P<last>[0-9]+)\s+(?P<ip>[0-9.]+):(?P<port>[0-9-]+)\s+(?P<qport>[0-9]+)\s+(?P<rate>[0-9]+)$', re.I)

"""
Some content in this file has been found in the B3 source. 
We thank the entire BigBrotherBot team for there contributions 
to the Urban Terror community, and credit much of the data/content 
in this file to them.

And credit to utstatsbot for sorting most of this out and collecting it together.
http://utstatsbot.googlecode.com/svn-history/r2/trunk/ut.log.format.txt
"""
