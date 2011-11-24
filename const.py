teams = {
0:'zombie',
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

itemr = {
MOD_WATER: {'id':'1'},
MOD_LAVA: {'id':'3'},
MOD_TELEFRAG : {'id':'5'},
MOD_FALLING: {'id':'6'},
MOD_SUICIDE: {'id':'7'},
MOD_TRIGGER_HURT: {'id':'9'},
MOD_CHANGE_TEAM: {'id':'10'},
UT_MOD_KNIFE: {'id':'12'},
UT_MOD_KNIFE_THROWN: {'id':'13'},
UT_MOD_BERETTA: {'id':'14'},
UT_MOD_DEAGLE: {'id':'15'},
UT_MOD_SPAS: {'id':'16'},
UT_MOD_UMP45: {'id':'17'},
UT_MOD_MP5K: {'id':'18'},
UT_MOD_LR300: {'id':'19'},
UT_MOD_G36: {'id':'20'},
UT_MOD_PSG1: {'id':'21'},
UT_MOD_HK69: {'id':'22'},
UT_MOD_BLED: {'id':'23'},
UT_MOD_KICKED: {'id':'24'},
UT_MOD_HEGRENADE: {'id':'25'},
UT_MOD_FLASH: {'id':None}, #@DEV One of these is 26, the other 27. Dont think we need this
UT_MOD_SMOKE: {'id':None},
UT_MOD_SR8: {'id':'28'},
UT_MOD_AK103: {'id':'30'}
UT_MOD_SPLODED: {'id':'31'},
UT_MOD_SLAPPED: {'id':'32'},
UT_MOD_BOMBED: {'id':'33'},
UT_MOD_NUKED: {'id':'34'},
UT_MOD_NEGEV: {'id':'35'},
UT_MOD_HK69_HIT: {'id':'37'},
UT_MOD_M4: {'id':'38'},
UT_MOD_FLAG: {'id':'39'},
UT_MOD_GOOMBA: {'id':'40'}}

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


class UrTBotError(Exception): pass
class ConfigError(Exception): pass
class UrbanTerrorError(Exception): pass


def getItemID(item): return globals()[item.upper()]['id']
Glob = lambda: globals()

"""
Some content in this file has been found in the B3 source. 
We thank the entire BigBrotherBot team for there contributions 
to the Urban Terror community, and credit much of the data/content 
in this file to them.
"""

        