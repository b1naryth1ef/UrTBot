teams = {
1:'red',
2:'blue',
3:'spec'
}

gametypes = {
0: 'ffa',
1: None,
2: None,
3: 'tdm', #Team death match
4: 'ts', #Team survivor
5: 'ftl', #Follow the leader
6: 'cah', #Capture and hold
7: 'ctf', #Capture the flag
8: 'bm' #Bomb
}


# //begin credit B3 project
DEATH_WATER='1'
DEATH_LAVA='3'
DEATH_TELEFRAG='5'
DEATH_FALLING='6'
DEATH_SUICIDE='7'
DEATH_TRIGGER_HURT='9'
DEATH_CHANGE_TEAM='10'
WEAPON_KNIFE='12'
WEAPON_KNIFE_THROWN='13'
WEAPON_BERETTA='14'
WEAPON_DEAGLE='15'
WEAPON_SPAS='16'
WEAPON_UMP45='17'
WEAPON_MP5K='18'
WEAPON_LR300='19'
WEAPON_G36='20'
WEAPON_PSG1='21'
WEAPON_HK69='22'
WEAPON_BLED='23'
DEATH_KICKED='24'
WEAPON_HEGRENADE='25'
WEAPON_FLASH=None #@DEV One of these is 26, the other 27. Time to investigate...
WEAPON_SMOKE=None
WEAPON_SR8='28'
WEAPON_AK103='30'
WEAPON_SPLODED='31'
WEAPON_SLAPPED='32'
WEAPON_BOMBED='33'
WEAPON_NUKED='34'
WEAPON_NEGEV='35'
WEAPON_HK69_HIT='37'
WEAPON_M4='38'
WEAPON_FLAG='39'
WEAPON_GOOMBA='40'

damage = {
	'PASSIVE': [0, 0, 0, 0, 0, 0, 0, 0],
    DEATH_TELEFRAG: [0, 0, 0, 0, 0, 0, 0, 0],
    WEAPON_KNIFE: [100, 60, 44, 35, 20, 20, 44, 100],
    WEAPON_KNIFE_THROWN: [100, 60, 44, 35, 20, 20, 44, 100],
    WEAPON_BERETTA: [100, 34, 30, 20, 11, 11, 30, 100],
    WEAPON_DEAGLE: [100, 66, 57, 38, 22, 22, 57, 100],
    WEAPON_SPAS: [25, 25, 25, 25, 25, 25, 25, 100],
    WEAPON_UMP45: [100, 51, 44, 29, 17, 17, 44, 100],
    WEAPON_MP5K: [50, 34, 30, 20, 11, 11, 30, 100],
    WEAPON_LR300: [100, 51, 44, 29, 17, 17, 44, 100],
    WEAPON_G36: [100, 51, 44, 29, 17, 17, 44, 100],
    WEAPON_PSG1: [100, 63, 97, 63, 36, 36, 97, 100],
    WEAPON_HK69: [50, 50, 50, 50, 50, 50, 50, 100],
    WEAPON_BLED: [15, 15, 15, 15, 15, 15, 15, 15],
    DEATH_KICKED: [20, 20, 20, 20, 20, 20, 20, 100],
    WEAPON_HEGRENADE: [50, 50, 50, 50, 50, 50, 50, 100],
    WEAPON_SR8: [100, 100, 100, 100, 50, 50, 100, 100],
    WEAPON_AK103: [100, 58, 51, 34, 19, 19, 51, 100],
    WEAPON_NEGEV: [50, 34, 30, 20, 11, 11, 30, 100],
    WEAPON_HK69_HIT: [20, 20, 20, 20, 20, 20, 20, 100],
    WEAPON_M4: [100, 51, 44, 29, 17, 17, 44, 100],
    WEAPON_GOOMBA: [100, 100, 100, 100, 100, 100, 100, 100],
     }

#//end credit b3 project

gearInfo = {
	#Sidearms
	'F':{'id':WEAPON_BERETTA, 'name':'beretta', 'damage':damage[WEAPON_BERETTA]},
	'G':{'id':WEAPON_DEAGLE,'name':'desert eagle', 'damage':damage[WEAPON_DEAGLE]},

	#Primary
	'K':{'id':WEAPON_HK69, 'name':'hk69', 'damage': damage[WEAPON_HK69]},
	'L':{'id':WEAPON_LR300, 'name':'lr300', 'damage': damage[WEAPON_LR300]},
	'M':{'id':WEAPON_G36, 'name':'g36', 'damage': damage[WEAPON_G36]},
	'N':{'id':WEAPON_PSG1, 'name':'psg1','damage': damage[WEAPON_PSG1]},
	'Z':{'id':WEAPON_SR8,'name':'sr8','damage': damage[WEAPON_SR8]},
	'a':{'id':WEAPON_AK103,'name':'ak103','damage': damage[WEAPON_AK103]},
	'c':{'id':WEAPON_NEGEV,'name':'negav','damage': damage[WEAPON_NEGEV]},
	'e':{'id':WEAPON_M4,'name':'m4','damage': damage[WEAPON_M4]},

	#Primary and Secondary
	'H':{'id':WEAPON_SPAS,'name':'spas', 'damage': damage[WEAPON_SPAS]},
	'I':{'id':WEAPON_MP5K,'name':'mp5k', 'damage': damage[WEAPON_MP5K]},
	'J':{'id':WEAPON_UMP45,'name':'ump45', 'damage': damage[WEAPON_UMP45]},

	#Grenades
	'O':{'id':WEAPON_HEGRENADE, 'name':'he grenade', 'damage': damage[WEAPON_HEGRENADE]},
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


"""
Much content in this file has been found in the B3 source. 
We thank the entire BigBrotherBot team for there contributions 
to the Urban Terror community, and credit much of the data/content 
in this file to them.

Teams: Give it a team integer and it will return the team name
Gametypes: give it a gametype integer and it will return the gametype name
"""

        