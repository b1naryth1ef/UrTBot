import database
import auth
import time 

class Player():
	def __init__(self, uid, data, api):
		self.uid = int(uid)
		self.cid = None #<<< get from the db
		self.data = data
		self.group = 0
		self.status = None
		self.api = api
		try:
			self.name = None
			self.ip = None
			self.team = None
			self.model = None
			self.sex = None
			self.headmodel = None
			self.team_model = None
			self.team_headmodel = None
			self.funred = None
			self.funblue = None
			self.raceRed = None
			self.raceBlue = None
			self.color1 = None
			self.color2 = None
			self.cg_predictitems = None
			self.cg_anonymous = None
			self.cl_guid = None
			self.cg_rgb = None
			self.cg_physics = None
			self.weapmodes = None
			self.gear = None
			self.teamtask = None
			self.handicap = None
			self.rate = None
			self.snaps = None
			self.ut_timenudge = None
			self.setData(self.data)
		except Exception, e:
			print e

	def setData(self, data):
		for i in data.keys(): #Strip line endings
			data[i] = data[i].strip()
		self.__dict__.update(data)
	
	def updateData(self, data):
		if 'team' in data.keys():
			if data['team'] != self.team:
				print 'Fired change team from updateData'
				self.api.B.eventFire('CLIENT_SWITCHTEAM', {'client':self.uid, 'toteam':data['team'], 'fromteam':self.team})
		self.setData(data)

class PlayerDatabase():
	def __init__(self):
		self.db = database.DB()
		if not self.db.tableExists("clients"): #PYTHON BABEH! NO HAS == FOR TRUE/FALSE!
			self.db.tableCreate('clients', {'id':'integer primary key autoincrement',
			'cgroup':'integer', 'nick':'text', 'guid':'text', 'password':'text',
			'ip':'text', 'joincount':'integer', 'firstjoin':'integer',
			'lastjoin':'integer'})
			self.db.commit()
		self.db.tableSelect("clients", "guid")

	def playerCreate(self, player):
		newplayer = self.db.rowBlank()
		newplayer["id"] = None
		newplayer["cgroup"] = 0
		newplayer["nick"] = player.name
		newplayer["guid"] = player.cl_guid
		newplayer["password"] = ""
		newplayer["ip"] = player.ip
		newplayer["joincount"] = 1
		newplayer["firstjoin"] = int(time.time())
		newplayer["lastjoin"] = newplayer["firstjoin"]
		try:
			newplayer["ip"] = player.ip.split(":")[0]
		except: print "[WARNING] Mal-formed IP address... that's all. :D"
		self.db.rowCreate(newplayer)
		return self.db.commit()

	def playerUpdate(self, player, join=False):
		# Ignore bots (what works best for this?)
		if player.cl_guid == None or player.cl_guid == "": return
		# If the player is in the db already, set player data from db
		entry = self.db.rowFind(player.cl_guid)
		if entry != None:
			player.group = auth.checkUserAuth(self.db, player.cl_guid, player.ip, player.name)
			if join != False:
				entry["joincount"] += 1
				self.db.rowUpdate(entry)
				self.db.commit()
		else:
			self.playerCreate(player)
			player.group = 0

	def playerJoin(self, player):
		entry = self.db.findRow(player.cl_guid)
# {'racered': '1', 'protocol': '68', 'ip': '127.0.0.1', 
# 'sex': 'male', 'rate': '25000', 'cg_predictitems': '0', 
# 'headmodel': 'sarge', 'team_model': 'james', 
# 'cl_anonymous': '0', 'funred': 'phat, goggles', 
# 'weapmodes': '00000111220000020002\n', 
# 'cl_guid': '5748E6243644AFFEF9B6B2F2A2F3A6D1', 'snaps': '20', 
# 'cg_rgb': '0 255 0', 'gear': 'FKAOXSA', 'handicap': '100', 
# 'color1': '4', 'qport': '42659', 'color2': '5', 'cg_physics': '1', 
# 'teamtask': '0', 'name': '[WoC]*B1naryTh1ef', 'challenge': '-585209824',
#  'team_headmodel': '*james', 'ut_timenudge': '30', 'raceblue': '1', 'model': 'sarge'}

