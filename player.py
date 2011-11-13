
class Player():
	def __init__(self, uid, data):
		self.uid = int(uid) #@DEV Meh...
		self.data = data
		print data
		try:
			self.name = data['name']
			self.ip = data['ip']
			self.team = 0
			
			self.model = data['model']
			self.sex = data['sex']
			self.headmodel = data['headmodel']
			self.team_model = data['team_model']
			self.team_headmodel = data['team_headmodel']
			self.funred = data['funred']
			self.funblue = data['funblue']
			self.raceRed = data['racered']
			self.raceBlue = data['raceblue']
			self.color1 = data['color1']
			self.color2 = data['color2']

			self.cg_predictitems = data['cg_predictitems']
			self.cg_anonymous = data['cg_anonymous']
			self.cg_guid = data['cg_guid']
			self.cg_rgb = data['cg_rgb']
			self.cg_physics = data['cg_physics']
			
			self.weapmodes = data['weapmodes']
			self.gear = data['gear']
			self.teamtask = data['teamtask']

			self.handicap = data['handicap']
			self.rate = data['rate']
			self.snaps = data['snaps']
			self.ut_timenudge = data['ut_timenudge']
			
		except Exception, e:
			print e
		