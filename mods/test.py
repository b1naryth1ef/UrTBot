class ExampleMod():
	enabled = False
	log = {}
	name = "ExampleMod"
	version = 0.1
	author = "B1naryth1ef"

	def __init__(self, api, game):
		self.enabled = True
		self.A = api
		self.G = game

	def cmdHelp(self, obj):
		a = self.A
		a.tell(0, a.cRED+"Sup bitch!")
		# print obj.Sender.split(" ")[1]
		# sendy = int(obj.sender.split(" ")[1])
		# if len(obj.msg.split(" ")) == 1:
		# 	a.tell(sendy, "%sUrTBot Help:" % (a.colorRED))
		# 	cmds = a.getCommands()
		# 	for i in cmds:
		# 		print a.colorBLUE+i+a.colorCYAN+":"+a.colorYELLOW+cmds[i][1]
		# elif len(obj.msg.split(" ")) == 2:
		# 	print obj.sender
		# 	cmds = a.getCommands()
		# 	a.tell(sendy, "%s%s%s: %s%s" % (a.colorBLUE, obj.msg.split(" ")[1], a.colorCYAN, a.colorYELLOW, cmds[obj.msg.split(" ")[1]][1]))
	
	def cmdList(self, obj):
		a = self.A
		a.say("PLAYER LIST:")
		i = a.getPlayer(0)
		msg = a.colorRED+"["+i.name+"]"+a.colorBLUE+i.team
		self.A.say(msg)

	def load(self):
		self.A.rCmd('!help', self.cmdHelp)
		self.A.rCmd('!list', self.cmdList, "List all users (with UID's)")

_MODS_ = {'ExampleMod':ExampleMod}