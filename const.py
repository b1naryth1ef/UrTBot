teams = {
0:'zombie',
1:'red',
2:'blue',
3:'spec'
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


#@TODO These should all be URTNAME = {id:#, event:OUR_NAME}
DEATH_WATER = {id:'1'}
DEATH_LAVA ={id:'3'}
DEATH_TELEFRAG ={id:'5'}
DEATH_FALLING={id:'6'}
DEATH_SUICIDE={id:'7'}
DEATH_TRIGGER_HURT={id:'9'}
DEATH_CHANGE_TEAM={id:'10'}
WEAPON_KNIFE={id:'12'}
WEAPON_KNIFE_THROWN={id:'13'}
WEAPON_BERETTA={id:'14'}
WEAPON_DEAGLE={id:'15'}
WEAPON_SPAS={id:'16'}
WEAPON_UMP45={id:'17'}
WEAPON_MP5K={id:'18'}
WEAPON_LR300={id:'19'}
WEAPON_G36={id:'20'}
WEAPON_PSG1={id:'21'}
WEAPON_HK69={id:'22'}
WEAPON_BLED={id:'23'}
DEATH_KICKED={id:'24'}
WEAPON_HEGRENADE={id:'25'}
WEAPON_FLASH={id:None} #@DEV One of these is 26, the other 27. Time to investigate...
WEAPON_SMOKE={id:None}
WEAPON_SR8={id:'28'}
WEAPON_AK103={id:'30'}
WEAPON_SPLODED={id:'31'}
WEAPON_SLAPPED={id:'32'}
WEAPON_BOMBED={id:'33'}
WEAPON_NUKED={id:'34'}
WEAPON_NEGEV={id:'35'}
WEAPON_HK69_HIT={id:'37'}
WEAPON_M4={id:'38'}
WEAPON_FLAG={id:'39'}
WEAPON_GOOMBA={id:'40'}

damage = {
	'PASSIVE': [0, 0, 0, 0, 0, 0, 0, 0],
    DEATH_TELEFRAG[id]: [0, 0, 0, 0, 0, 0, 0, 0],
    WEAPON_KNIFE[id]: [100, 60, 44, 35, 20, 20, 44, 100],
    WEAPON_KNIFE_THROWN[id]: [100, 60, 44, 35, 20, 20, 44, 100],
    WEAPON_BERETTA[id]: [100, 34, 30, 20, 11, 11, 30, 100],
    WEAPON_DEAGLE[id]: [100, 66, 57, 38, 22, 22, 57, 100],
    WEAPON_SPAS[id]: [25, 25, 25, 25, 25, 25, 25, 100],
    WEAPON_UMP45[id]: [100, 51, 44, 29, 17, 17, 44, 100],
    WEAPON_MP5K[id]: [50, 34, 30, 20, 11, 11, 30, 100],
    WEAPON_LR300[id]: [100, 51, 44, 29, 17, 17, 44, 100],
    WEAPON_G36[id]: [100, 51, 44, 29, 17, 17, 44, 100],
    WEAPON_PSG1[id]: [100, 63, 97, 63, 36, 36, 97, 100],
    WEAPON_HK69[id]: [50, 50, 50, 50, 50, 50, 50, 100],
    WEAPON_BLED[id]: [15, 15, 15, 15, 15, 15, 15, 15],
    DEATH_KICKED[id]: [20, 20, 20, 20, 20, 20, 20, 100],
    WEAPON_HEGRENADE[id]: [50, 50, 50, 50, 50, 50, 50, 100],
    WEAPON_SR8[id]: [100, 100, 100, 100, 50, 50, 100, 100],
    WEAPON_AK103[id]: [100, 58, 51, 34, 19, 19, 51, 100],
    WEAPON_NEGEV[id]: [50, 34, 30, 20, 11, 11, 30, 100],
    WEAPON_HK69_HIT[id]: [20, 20, 20, 20, 20, 20, 20, 100],
    WEAPON_M4[id]: [100, 51, 44, 29, 17, 17, 44, 100],
    WEAPON_GOOMBA[id]: [100, 100, 100, 100, 100, 100, 100, 100],
     }



gearInfo = {
	#Sidearms
	'F':{'id':WEAPON_BERETTA[id], 'name':'beretta', 'damage':damage[WEAPON_BERETTA[id]]},
	'G':{'id':WEAPON_DEAGLE[id],'name':'desert eagle', 'damage':damage[WEAPON_DEAGLE[id]]},

	#Primary
	'K':{'id':WEAPON_HK69[id], 'name':'hk69', 'damage': damage[WEAPON_HK69[id]]},
	'L':{'id':WEAPON_LR300[id], 'name':'lr300', 'damage': damage[WEAPON_LR300[id]]},
	'M':{'id':WEAPON_G36[id], 'name':'g36', 'damage': damage[WEAPON_G36[id]]},
	'N':{'id':WEAPON_PSG1[id], 'name':'psg1','damage': damage[WEAPON_PSG1[id]]},
	'Z':{'id':WEAPON_SR8[id],'name':'sr8','damage': damage[WEAPON_SR8[id]]},
	'a':{'id':WEAPON_AK103[id],'name':'ak103','damage': damage[WEAPON_AK103[id]]},
	'c':{'id':WEAPON_NEGEV[id],'name':'negav','damage': damage[WEAPON_NEGEV[id]]},
	'e':{'id':WEAPON_M4[id],'name':'m4','damage': damage[WEAPON_M4[id]]},

	#Primary and Secondary
	'H':{'id':WEAPON_SPAS[id],'name':'spas', 'damage': damage[WEAPON_SPAS[id]]},
	'I':{'id':WEAPON_MP5K[id],'name':'mp5k', 'damage': damage[WEAPON_MP5K[id]]},
	'J':{'id':WEAPON_UMP45[id],'name':'ump45', 'damage': damage[WEAPON_UMP45[id]]},

	#Grenades
	'O':{'id':WEAPON_HEGRENADE[id], 'name':'he grenade', 'damage': damage[WEAPON_HEGRENADE[id]]},
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
"""

        