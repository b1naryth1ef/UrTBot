#---IMPORTS---#
import subprocess, time, os, sys, imp
from pyquake3 import PyQuake3
#import db

#---Pre Vars---#
home = os.getcwd()
Events = {}
Commands = {}
Q = PyQuake3('localhost:27960', rcon_password='Norp73')
prefix = "^1[^3Boteh^1]"
hj=[]

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
		if 1==1:
			mod = imp.load_source(fname, f)
			for x in getattr(mod,"_funcs"):
				xev = getattr(mod,x+"_events")
				xcmd = getattr(mod,x+"_commands")
				for i in xev:
					if i in Events:
						Events[i].append(xev[i])
					else:
						Events[i] = [xev[i]] 
				for i in xcmd:
					if i in Commands:
						print "Error" #@TODO call error
					else:
						Commands[i] = xcmd[i]
		#except Exception, e:
		#	print >> sys.stderr, "ERROR LOADING %s: %s" % (fname, e)

def parse(inp):
	if inp.startswith("say:"):
		newy = inp.split(':',2)
		nsender = newy[1]
		nmsg = newy[2].rstrip()
		ncmd1 = nmsg.strip(" ")
		ncmd = ncmd1.split(" ")[0]
		print "'"+ncmd+"'"
		print hj
		if ncmd.lower() in Commands:
			print "@CMD TRUE"
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