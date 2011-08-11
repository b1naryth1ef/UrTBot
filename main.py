#----------IMPORTS----------#
import subprocess, time, os, sys, imp
from tools import error
import tools
from pyquake3 import PyQuake3

#----------Objects----------#
Q = PyQuake3('localhost:27960', rcon_password='123abc')

#----------Vars----------#
Ev = []
li = {}
id = 0
cmds = {}
home = os.getcwd()
prefix = "^1[^3Boteh^1]"

#----------Command Stuff----------#
def LR(event,exe): #Register listening events
    if not li:
		li[event] = [exe]
	else:
		li[event].append(exe)
		
def L(event,api): #Listener 

	if event in li:
		for i in li[event]:
			i(api)
	else:
		pass

class Cmd(object):
    def __init__(self,name,cmd,exe,active=True):
        self.name = name #Not used yet, DO NOT TRY TO CALL THIS! name = cmd always!
        self.cmd = cmd
        self.exe = exe
        self.active = active
    def exe(self,a)
        #open thread
        self.exe(a)


def CR(cmd,exe): #Register commands
	mycmd = Cmd(cmd,cmd,exe)
	if cmd in cmds:
		error(00,"Command "+cmd+" already registered!")
	else:
		cmds[cmd]=mycmd


#----------Class Definitions----------#


class Api(object):
	def __init__(self,obj=None):
		self.q = Q
		self.a = obj
		self.prefix = prefix
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
	def __init__(self, typex=None, data=None, id=0):
		if typex == "kill":
			self.kill(data)
		elif typex == "death":
			self.death(data)
		elif typex == "kick":
			self.kick(data)
		elif typex == "ban":
			self.ban(data)
		elif typex == "conn":
			self.conn(data)
		elif typex == "msg":
			self.msg(data)
		else:
			error(0,"Event type invalid")

	def kill(self,data):
		self.type = "kill"
		self.atk = data[0] #Attacker
		self.kil = data[1] #Killed person
		self.meth = data[2] #Method

	def death(self,data):
		self.type = "death"
		self.per = data[0] #Person killed
		self.meth = data[1] #Method

	def kick(self,data):
        self.type = "kick"
		self.per = data[0] #Person kicked
		self.adm = data[1] #Admin/kicker
	
	def ban(self,data):
        self.type = "ban"
		self.per = data[0] #Person banned
		self.adm = data[1] #Admin/banner

	def conn(self,data):
        self.type = "conn"
		self.per = data[0] #Person connected
		self.uid = data[1] #Persons ID

	def msg(self, data):
        self.type = "msg"
		self.sender = data[0]
		self.msg = data[1]


#----------Main Function Defs----------#

def _kill(atk,kil,meth):
	obj = Event('kill',(atk,kil,meth))
	A = Api(obj)
	L('kill',A)
	return obj

def _msg(sender,msg):
	obj = Event('msg',(sender,msg))
	A = Api(obj)
	L('msg',A)
	return obj	

def parse(inp):
	if 'say:' in inp:
		new = inp.split(':',2) #Split so that [0:'say',1:'userinfo',2:'msg']
		obj = _msg(new[1],new[2].rstrip())
		if new[2].strip() in cmds:
			A = Api(obj)
			cmds[new[2].strip()].exe(A)
	elif 'ClientConnect:' in inp:
		#We need to check if the client was already connected, and possibly remove the old event?
		newy = inp.split(":")
		new = newy[1].strip()
		print new
		obj = Event('conn',('Blah',new))
		Ev.append(obj)
		print Ev
	elif 'Kill:' in inp:
		newy = inp.split(" ")
		print newy[4]
		print newy[6]
		print newy[8]
		_kill(newy[4],newy[6],newy[8].rstrip())
		
def loop():
	proc = subprocess.Popen('./ioUrbanTerror.app/Contents/MacOS/ioUrbanTerror.ub +set dedicated 2 +exec server.cfg',shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	while True:
		proc_read = proc.stdout.readline()
		if proc_read:
			print proc_read
			parse(proc_read)
	return proc

def exe():
	pass

def load():
	filenames = []
    fail = True
	for fn in os.listdir(os.path.join(home, 'mods')): 
		if fn.endswith('.py') and not fn.startswith('_'): 
			filenames.append(os.path.join(home, 'mods', fn))
	for filename in filenames: 
		fname = os.path.basename(filename)[:-3]
		try:
			mod = imp.load_source(fname, filename)
		except Exception, e: 
			print >> sys.stderr, "ERROR LOADING %s: %s" % (fname, e)
            fail = False
    return fail

Load = load()
if load is True:
    P = loop()
else:
    error(0,"Module failed to load... Cannot start loop!")


#ClientConnect: 0
#ClientUserInfo
#say:
#['Kill:', '0', '1', '19:', 'Adminy', 'killed', 'Adminy_1', 'by', 'UT_MOD_LR300\n']