#---IMPORTS---#
import subprocess, time, os, sys, imp
from pyquake3 import PyQuake3

#---Pre Vars---#
home = os.getcwd()
Events = {}
Commands = {}
Q = PyQuake3('localhost:27960', rcon_password='Norp73')
prefix = "^1[^3Boteh^1]"

#---System Wide Handlers---#
def error(t,msg):
	if t == 001:
		print "CRITICAL ERROR: "+msg
		sys.exit()
	elif t == 002:
		print "ERROR: "+msg
	elif t == 011:
		print "MOD CRITICAL ERROR: "+msg
		sys.exit()
	elif t == 012:
		print "MOD ERROR: "+msg

#---MODULE FUNCS---#
def RegE(eve,exe):
	"""Registers a modules usage of an event"""
	if eve not in Events:
		Events[eve] = [exe]
		print "Adding event"
		print Events
	else:
		Events[eve].append(exe)

def RegC(cmd,exe):
	print "@reg2"
	if cmd not in Commands:
		print "Adding command"
		Commands[cmd] = exe
		print Commands
	else:
		error(002,"Command already registered... Ignoring new Register Request.")

def Listen(event,obj):
	if event in Events:
		for i in Events[event]:
			i(obj)
	else:
		pass

#---CLASSES---#
class Api(object):
	
	def __init__(self):
		self.N = "API"
		self.q = Q
	def register(self,tp,data):
		print "@reg"
		if tp.lower() == "event":
			RegE(data[0],data[1])
		elif tp.lower() == "command":
			RegC(data[0],data[1])
		else:
			error(002,"Unknown register call:"+tp)
	def ping(self):
		"""API Method: Simple system to test modules"""
		print "Pong!"
	def say(self,msg):
		Q.rcon("say "+prefix+" ^2"+msg)
	def tell(self,uid,msg):
		Q.rcon("tell "+uid+" "+msg)
	def rcon(self,cmd):
		return Q.rcon(cmd)
	def plist(self):
		Q.update()
		return Q.players
		

class Event(object):
	def kill(self,data):
		self.attacker = data[0]
		self.victim = data[1]
		self.method = data[2]
	def msg(self,data):
		self.sender = data[0]
		self.msg = data[1]
		self.iscmd = data[2] #Bool, should be true if ! is in front
	def conn(self,data):
		print data
		self.uid = data[0]
		self.name = data[1]
		self.ip = data[2]
	i = {'kill':kill,'msg':msg,'conn':conn}
	def __init__(self,typex,data):
		if typex in self.i:
			self.i[typex](self,data)

#---EVENTS---#
def _kill(atk,vic,meth):
	obj = Event('kill',(atk,vic,meth))
	Listen('kill',obj)
	return obj

def _msg(sen,msg,iscmd=False):
	obj = Event('msg',(sen,msg,iscmd))
	Listen('msg',obj)
	return obj

def _conn(uid):
	Q.rcon_update()
	for i in Q.players:
		if i.uid == uid:
			name = i.name
			ip = i.ip
	obj = Event('conn',(uid,name,ip))
	Listen('conn',obj)
	return obj

#---MODULE SETUP---#
def load():
	fn = []
	county = 0
	for i in os.listdir(os.path.join(home, 'mods')):
		if i.endswith('.py') and not i.startswith("_"):
			if not i.startswith("api"):
				fn.append(os.path.join(home, 'mods', i))
	for f in fn:
		fname = os.path.basename(f)[:-3]
		try:
			mod = imp.load_source(fname, f)
		except Exception, e:
			print >> sys.stderr, "ERROR LOADING %s: %s" % (fname, e)

def parse(inp):
	if inp.startswith("say:"):
		print Commands
		newy = inp.split(':',2)
		nsender = newy[1]
		nmsg = newy[2].rstrip()
		ncmd = nmsg.split(" ")[0]
		print ncmd
		print nmsg
		if ncmd.lower() in Commands:
			obj = _msg(nsender,nmsg,True)
			Commands[ncmd](obj)
	elif inp.startswith('ClientConnect:'):
		new = inp.split(":")[1].strip()
		_conn(new)
	elif inp.startswith('Kill:'):
		newy = inp.split(" ")
		_kill(newy[4],newy[6],newy[8].rstrip())
		
def loop():
	proc = subprocess.Popen('./ioUrbanTerror.app/Contents/MacOS/ioUrbanTerror.ub +set dedicated 2 +exec server.cfg',shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	while True:
		proc_read = proc.stdout.readline()
		if proc_read:
			print proc_read.rstrip()
			parse(proc_read)
	return proc


if __name__ == "__main__":
	load()
	loop()