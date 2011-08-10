import subprocess, time, os, sys

def help():
	print "@help"

cmds = {"!help":help}

def parse(inp):
	if 'say:' in inp: #Is it sent by a user?
		new = inp.split(':',2) #Split so that [0:'say',1:'userinfo',2:'msg']
		for i in cmds:
			if i in new[2]:
				cmds[i]()
	

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