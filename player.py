class Player():
	def __init__(self, uid, data):
		self.uid = int(uid)
		self.data = data
		self.group = 0
		self.status = None
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
		for i in data.keys: #Strip line endings
			data[i] = data[i].strip()
		self.__dict__.update(data)

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

