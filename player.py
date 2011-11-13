
class Player():
	def __init__(self, uid, data):
		self.uid = int(uid) #@DEV Meh...
		self.data = data
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
		if 'name' in data.keys(): self.name = data['name']
		if 'ip' in data.keys(): self.ip = data['ip']
		
		if 'model' in data.keys(): self.model = data['model']
		if 'sex' in data.keys(): self.sex = data['sex']
		if 'headmodel' in data.keys(): self.headmodel = data['headmodel']
		if 'team_model' in data.keys(): self.team_model = data['team_model']
		if 'team_headmodel' in data.keys(): self.team_headmodel = data['team_headmodel']
		if 'funred' in data.keys(): self.funred = data['funred']
		if 'funblue' in data.keys(): self.funblue = data['funblue']
		if 'racered' in data.keys(): self.raceRed = data['racered']
		if 'raceblue' in data.keys(): self.raceBlue = data['raceblue']
		if 'color1' in data.keys(): self.color1 = data['color1']
		if 'color2' in data.keys(): self.color2 = data['color2']

		if 'cg_predictitems' in data.keys(): self.cg_predictitems = data['cg_predictitems']
		if 'cg_anonymous' in data.keys(): self.cg_anonymous = data['cg_anonymous']
		if 'cl_guid' in data.keys(): self.cl_guid = data['cl_guid']
		if 'cg_rgb' in data.keys(): self.cg_rgb = data['cg_rgb']
		if 'cg_physics' in data.keys(): self.cg_physics = data['cg_physics']
		
		if 'weapmodes' in data.keys(): self.weapmodes = data['weapmodes']
		if 'gear' in data.keys(): self.gear = data['gear']
		if 'teamtask' in data.keys(): self.teamtask = data['teamtask']

		if 'handicap' in data.keys(): self.handicap = data['handicap']
		if 'rate' in data.keys(): self.rate = data['rate']
		if 'snaps' in data.keys(): self.snaps = data['snaps']
		if 'ut_timenudge' in data.keys(): self.ut_timenudge = data['ut_timenudge']

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

