import subprocess, time, os, sys
from tools import error
import tools
from pyquake3 import PyQuake3


Q = PyQuake3('localhost:27960', rcon_password='123abc')
Ev = []
li = {}
id = 0 #Global Event ID

def listenreg(event,exe):
	if not li:
		li[event] = [exe]
	else:
		li[event].append(exe)
		
def L(event,api): #Listener 
	if li[event]:
		for i in li[event]:
			i(api)
	else:
		pass

class Api(object):
	def __init__(self,obj):
		self.q = Q
		self.a = obj

class Event(object):
	def __init__(self, typex=None, data=None, id=0):
		if typex == "kill":
			self.kill(data,id)
		elif typex == "death":
			self.death(data,id)
		elif typex == "kick":
			self.kick(data,id)
		elif typex == "ban":
			self.ban(data,id)
		elif typex == "conn":
			self.conn(data,id)
		elif typex == "msg":
			self.msg(data,id)
		else:
			error(0,"Event type invalid")
	def kill(self,data,id):
		id += 1
		self.id = id
		self.type = "kill"
		self.atk = data[0] #Attacker
		self.kil = data[1] #Killed person
		self.meth = data[2] #Method

	def death(self,data,id):
		id += 1
		self.id = id
		self.type = "death"
		self.per = data[0] #Person killed
		self.meth = data[1] #Method

	def kick(self,data,id):
		id += 1
		self.id = id
		self.per = data[0] #Person kicked
		self.adm = data[1] #Admin/kicker
	
	def ban(self,data,id):
		id += 1
		self.id = id
		self.per = data[0] #Person banned
		self.adm = data[1] #Admin/banner

	def conn(self,data,id):
		id += 1
		self.id = id
		self.per = data[0] #Person connected
		self.uid = data[1] #Persons ID

	def msg(self, data,id):
		id += 1
		self.id = id
		self.sender = data[0]
		self.msg = data[1]

def _kill(atk,kil,meth):
	obj = Event('kill',(atk,kil,meth))
	A = Api(obj)
	L('kill',A)
	return obj

def _msg(sender,msg):
	obj = Event('msg',(sender,msg))
	A = Api(obj)
	L('msg',A)	

#TESTS		
def help():
	print "@help"
def killmsg(api):
	print "Killed!"
listenreg('kill',killmsg)
cmds = {"!help":help}


def parse(inp):
	if 'say:' in inp:\
		new = inp.split(':',2) #Split so that [0:'say',1:'userinfo',2:'msg']
		if new[2].strip() in cmds:
			cmds[new[2].strip()]() #api goes in there

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
		_kill(newy[4],newy[5],newy[7].rstrip())
		
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

P = loop()
#ClientConnect: 0
#ClientUserInfo
#say:
#['Kill:', '0', '1', '19:', 'Adminy', 'killed', 'Adminy_1', 'by', 'UT_MOD_LR300\n']
#4: Killer
#5: Victim
#7: Method