from rcon import RCON
import init, socket, select, time, player, re, thread, const

class GameOutput():
	def __init__(self, usockname=None):
		self.usockname = usockname
		self.usock = None
		self.buf = ''
		self.lines = []

		if self.usockname: self.connect(self.usockname)

	def connect(self, usockname):
		if self.usock: self.usock.close()
		self.usock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		self.usock.connect(usockname)

	def checkAndRead(self):
		newbuf = None
		readrdy = select.select([self.usock], [], [], 0.10)[0]
		if readrdy != []:
			self.buf += self.usock.recv(4096)
			for line in self.buf.splitlines(True):
				if line.endswith("\n"): self.lines.append(line.strip())
				else: newbuf = line
			if newbuf: self.buf = newbuf
			else: self.buf = ''

	def hasLine(self):
		if len(self.lines): return 1
		return 0

	def getLine(self):
		return self.lines.pop(0)

class Bot():
	def __init__(self, prefix="^1[^3Boteh^1]:", ip='localhost:27960', rcon="", debug=False, playerdb=None):
		from config import UrTConfig

		self.prefix = prefix
		self.ip = ip
		self.rcon = rcon
		self.Q = RCON(self.ip, self.rcon)
		self.pdb = playerdb
		self.status = 1 #1 is on, 0 is off
		self.debug = debug #False will hide messages, True will print them and log them to vars
		
		self.maplist = UrTConfig['maps']
		self.currentMap = None
		self.gameData = {}
		self.loadingMap = False

		self.redScore = 0
		self.blueScore = 0

		self.Modules = {} #Plugins
		self.Listeners = {} #Plugins waiting for Triggers
		self.Triggers = {} #Possible Triggers (Events)
		self.Commands = {} #Commands
		self.Aliases = {} #aliases BIATCH

		self.Clients = {} #AKA players
		self.curClients = lambda: [int(i[0]) for i in self.getStatus()]
		
	def roundNew(self): pass
	def roundEnd(self): pass
	def matchNew(self):
		self.loadingMap = False
	def matchEnd(self):
		print 'Match over... RED: %s BLUE: %s' % (self.redScore, self.blueScore)
		self.eventFire('GAME_MATCH_END', {'redscore':self.redScore, 'bluescore':self.blueScore})
		self.loadingMap = True
	
	def getClient(self, uid): return self.Clients[uid]
	def getGameType(self):
		r = self.Q.rcon('g_gametype')
		r = re.findall(const.rconGameType, r)
		self.gameData['g_gametype'] = r[0][0]
		return r[0][0]

	def setScores(self, line):
		#Scores: R:11 B:9
		line = line.split(':')
		self.redScore = int(line[2].strip(' B'))
		self.blueScore = int(line[3])
	
	def updatePlayers(self):
		#0: Eduardodias2012 BLUE k:9 d:11 ping:196 200.181.147.46:44453
		r = self.Q.rcon('players')
		r = r.split('\n')
		self.setScores(r[3])
		for i in r[4:]:
			if i != '':
				i = i.split(' ')
				cid = int(i[0].strip(':'))
				obj = self.Clients[cid]
				obj.team = i[2].lower()
				obj.score[0] = i[3].strip('k:')
				obj.score[1] = i[4].strip('d:')

	def dumpUser(self, uid):
		vz = []
		varz = {}
		r = self.Q.rcon('dumpuser %s' % uid)
		r = r.split('\n')
		for i in r[3:]:
			if i != '':
				vz.append([j for j in i.split(' ') if j != ''])
		for i in vz:
			varz[i[0]] = i[1]
		return varz
		 
	def getStatus(self):
		varz = []
		r = self.Q.rcon('status')
		r = r.split('\n')[4:]
		for i in r:
			if i != '':
				i = i.split(' ')
				i = [o for o in i if o != '']
				varz.append(i)
		return varz

	def getCurrentMap(self):
		r = self.Q.rcon('mapname')
		r = const.rconCurrentMap.search(r)
		self.currentMap = r.group(1)
		self.gameData['mapname'] = r.group(1)
		return r.group(1)

	def eventFire(self, event, data): 
		obj = init.events.EVENTS[event](data)
		for i in self.Listeners.keys():
			if i == event:
				for listener in self.Listeners[i]:
					thread.start_new_thread(listener, (obj, time.time()))
				break
		return obj

	def Startup(self):
		#print 'CALLED STARTUP'
		from config import UrTConfig
		self.Q.rcon("say "+self.prefix+" ^3"+"Starting up...")
		
		# Get the PK3s/maps the server has loaded
		pk3s = self.Q.rcon("sv_pakNames").split('"')[3].split()
		for ignore in UrTConfig['ignoremaps']:
			if ignore in pk3s: pk3s.remove(ignore)
		self.maplist += pk3s
		print self.maplist

		status = self.getStatus()
		if status == []: return

		for i in status:
			print i, i[0]
			uid = int(i[0])
			self.Clients[uid] = player.Player(uid, self.dumpUser(uid), init.A)
			if self.Clients[uid].cl_guid != None:
		 		self.pdb.playerUpdate(self.Clients[uid])

		self.updatePlayers() #Set team/score for players
		self.getGameType() #Set g_gametype in self.gamedata
		self.getCurrentMap() #set mapname in self.gamedata

		self.Q.rcon("say "+self.prefix+" ^3"+"Startup complete.")
		print 'STARTUP DONE'

class API():
	RED = '^1'
	GREEN = '^2'
	YELLOW = '^3'
	BLUE = '^4'
	CYAN = '^5'
	MAGENTA = '^6'
	WHITE = '^7'
	BLACK = '^8'

	def __init__(self, auth=None):
		self.B = init.BOT
		self.Q = init.BOT.Q
	def debug(self, msg, plugin=None): 
		if self.B.debug is True: 
			if plugin is None:
				print '[DEBUG]', msg
				init.botDEBUGS.append((time.time(), msg))
			else:
				print '[DEBUG|%s] %s' % (plugin, msg)
				init.pluginDEBUGS.append((time.time(), plugin, msg))
	def canInt(self, i): return str(i).isdigit()
	def tester(self): self.debug("TESTING! 1! 2! 3!")
	def say(self,msg): self.Q.rcon("say "+self.B.prefix+" ^3"+msg)
	def tell(self,uid,msg): self.Q.rcon("tell %s %s %s " % (uid, self.B.prefix, msg))
	def kick(self, uid): self.Q.rcon('kick %s' % uid)
	def rcon(self,cmd): return self.Q.rcon(cmd)
	def getClients(self): return self.B.Clients
	def getCommands(self): return self.B.Commands
	def whatTeam(self, num): return const.teams[num]
	def exitProc(self): sys.exit()
	def bootProc(self): keepLoop = False #@DEV Need a way of rebooting el boto
	def reboot(self): handlr.initz('reboot')
	def getCmd(self, cmd): return self.B.Commands.get(cmd)
	def getClient(self, iid=0):
		if len(self.B.Clients) != 0: return self.B.Clients.get(int(iid))
		else: return None
	def oldfindClient(self, name):
		x = self.findClients(name)
		if len(x) == 1: return x[0]
		else: return False
	def findClient(self, name, multi=False):
		ret = []
		print 'Finding Client (%s):' % name
		if type(name) is int or name.isdigit():
			for i in self.getClients().values():
				#print int(name), i.uid
				if int(name) == i.uid:
					ret.append(i)
					break
		else:
			for i in self.getClients().values():
				#print name.lower(), i.name.lower()
				if name.lower() in i.name.lower(): 
					ret.append(i)
					break
				if name.lower() == i.name.lower(): 
					ret.append(i)
					break
		if len(ret) == 1: return ret[0]
		elif len(ret) > 1 and multi is True: return ret
		else: return None
	def findClients(self, name):
		if name.isdigit() and len(name) <= 2:
			client = self.getClients().get(int(name))
			#if client != None: return [int(name)] #Should return obj ouis?
			if client != None: return [client]
			return []
		clients = self.getClients()
		return [client for client in clients if name in clients[client].name]
	def nameToCID(self, name, notify=None):
		cid = self.findClients(name)
		if len(cid) == 1:
			return cid[0]
		elif notify:
			if len(cid) == 0:
				self.tell(notify, "No player/clientID matching '%s'." % name)
			else:
				self.tell(notify, "Please be more specific.")
		return None

	def findMap(self, mapname):
		maplist = []
		for name in self.B.maplist:
			if mapname == name or ("ut4_" + mapname) == name: return [name]
			elif mapname in name: maplist.append(name)
		return maplist
	def addListener(self, event, func): 
		if event in self.B.Listeners.keys():
			if self.B.Listeners[event] != None: self.B.Listeners[event].append(func)
			else: self.B.Listeners[event] = [func]
			return True
		else: self.B.Listeners[event] = [func]
	def addListeners(self, events, func):
		for i in events:
			if i in self.B.Listeners.keys():
				if self.B.Listeners[i] != None: self.B.Listeners[i].append(func)
				else: self.B.Listeners[i] = [func]
			else: self.B.Listeners[i] = [func]
	def addCmd(self, cmd, func, desc='None', level=0, alias=[]):
		if cmd in self.B.Commands.keys():
			self.debug("Can't add command %s, another plugin already added it!" % (cmd))
			return False
		self.B.Commands[cmd] = (func,desc,level)
		for i in alias:
			self.B.Aliases[i] = (func,desc,level,cmd)
		return True
	def addCmds(self, cmds):
		for i in cmds:
			if i[0] in self.B.Commands.keys(): self.debug("Can't add command %s, another plugin already added it!" % (i[0]))
			if len(i) == 5:
				for x in i[5]:
					self.B.Aliases[x] = (i[1], i[2], i[3], i[0])
			else: self.B.Commands[i[0]] = (i[1], i[2], i[3])
	def delCmd(self, cmd):
		if cmd in self.B.Commands.keys():
			del self.B.Commands[cmd]
			for i in self.B.Aliases:
				if i[3] == cmd:
					del i
			return True
		return False
	
	def addTrigger(self, trigger):
		if trigger in self.B.Triggers.keys():
			self.debug("Can't add trigger %s, another plugin already added it!" % (trigger))
			return False
		self.B.Triggers[trigger] = []
		return True
	def retrieveTeam(self, team):
		reply = A.rcon("g_" + team + "TeamList").splitlines()[1:][0]
		players = reply.split('\"')[3].split("^")[0]
		ids = []
		for char in players:
			cid = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".find(char)
			if cid != -1: ids.append(cid)
		return ids