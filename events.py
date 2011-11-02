import time



class Event(): pass

class EventDeath():
	def __init__(self, data):
		self.id = 0
		self.fireTime = time.time()
		self.initTime = time.time()
		self.data = data

class EventServer(): pass

class EventClient(): pass

class EventOther(): pass


#DEATHS
class DEATH_WATER(EventDeath):
	def __init__(self, data):
		self.id = 1
		self.type = 'suicide'
		self.name = 'MOD_WATER'
		self.fireTime = time.time()
		self.initTime = time.time()
		self.data = data
	
		self.attacker = 'WORLD'
		self.victim = data['victim']
		self.attackerScore = 0
		self.victimScore = -1
		self.isWorld = True

class DEATH_LAVA(EventDeath):
	def __init__(self, data):
		self.id = 3
		self.name = 'MOD_LAVA'
		self.type = 'suicide'
		self.fireTime = time.time()
		self.initTime = time.time()
		self.data = data
	
		self.attacker = 'WORLD'
		self.victim = data['victim']
		self.attackerScore = 0
		self.victimScore = -1
		self.isWorld = True

class DEATH_TELEFRAG(EventDeath): pass
	
class DEATH_FALLING(EventDeath):
	def __init__(self, data):
		self.id = 6
		self.type = 'suicide'
		self.type = 'MOD_FALLING'
		self.fireTime = time.time()
		self.initTime = time.time()
		self.data = data
	
		self.attacker = 'WORLD'
		self.victim = data['victim']
		self.attackerScore = 0
		self.victimScore = -1
		self.isWorld = True 

class DEATH_SUICIDE(EventDeath): #@NOTE Seems like this is non-world
	def __init__(self, data):
		self.id = 7
		self.type = 'suicide'
		self.name = "MOD_SUICIDE"
		self.fireTime = time.time()
		self.initTime = time.time()
		self.data = data
	
		self.attacker = data['attacker']
		self.victim = data['victim']
		self.attackerScore = 0
		self.victimScore = -1
		self.isWorld = False

class DEATH_TRIGGER_HURT(EventDeath):
	def __init__(self, data):
		self.id = 9
		self.type = 'suicide'
		self.name = 'MOD_TRIGGER_HURT'
		self.fireTime = time.time()
		self.initTime = time.time()
		self.data = data
	
		self.attacker = 'WORLD'
		self.victim = data['victim']
		self.attackerScore = 0
		self.victimScore = -1
		self.isWorld = True

class DEATH_CHANGE_TEAM(EventDeath):
	def __init__(self, data):
		self.id = 10
		self.type = 'suicide'
		self.name = "MOD_CHANGE_TEAM"
		self.fireTime = time.time()
		self.initTime = time.time()
		self.data = data
	
		self.attacker = data['attacker']
		self.victim = data['victim']
		self.attackerScore = 0
		self.victimScore = 0
		self.isWorld = False

class WEAPON_KNIFE(EventDeath): pass
class WEAPON_KNIFE_THROWN(EventDeath): pass
class WEAPON_BERETTA(EventDeath): pass
class WEAPON_DEAGLE(EventDeath): pass
class WEAPON_SPAS(EventDeath): pass
class WEAPON_UMP45(EventDeath): pass
class WEAPON_MP5K(EventDeath): pass
class WEAPON_LR300(EventDeath): pass
class WEAPON_G36(EventDeath): pass
class WEAPON_PSG1(EventDeath): pass
class WEAPON_HK69(EventDeath): pass
class WEAPON_BLED(EventDeath): pass
class DEATH_KICKED(EventDeath): pass
class WEAPON_HEGRENADE(EventDeath): pass
class WEAPON_SR8(EventDeath): pass
class WEAPON_AK103(EventDeath): pass
class WEAPON_SPLODED(EventDeath): pass
class WEAPON_SLAPPED(EventDeath): pass
class WEAPON_BOMBED(EventDeath): pass
class WEAPON_NUKED(EventDeath): pass
class WEAPON_NEGEV(EventDeath): pass
class WEAPON_HK69_HIT(EventDeath): pass
class WEAPON_M4(EventDeath): pass
class WEAPON_FLAG(EventDeath): pass
class WEAPON_GOOMBA(EventDeath): pass

evez = {
	'MOD_WATER': DEATH_WATER,
	'MOD_LAVA': DEATH_LAVA,
	'MOD_TELEFRAG': DEATH_TELEFRAG,
	'MOD_FALLING': DEATH_FALLING,
	'MOD_SUICIDE': DEATH_SUICIDE,
	'MOD_TRIGGER_HURT': DEATH_TRIGGER_HURT,
	'MOD_CHANGE_TEAM': DEATH_CHANGE_TEAM
}