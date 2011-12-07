#!/usr/bin/python
# wrap iourtded so stdout is available on a unix socket
from socket import *
import subprocess
import select
import os, sys
import signal

serverexe = None
serversocket = None
proc = None

def sigHandler(signum, frame):
	os.kill(proc.pid, signal.SIGINT)
	proc.wait()
	sys.exit()

def loadConfig():
	from config import botConfig
	global serverexe, serversocket
	serverexe = botConfig['servercommand']
	serversocket = botConfig['serversocket']

def launch():
	global proc, procfile
	clients = []

	proc = subprocess.Popen(serverexe, 
								shell=True,
								stdin=subprocess.PIPE,
								stdout=subprocess.PIPE,
								stderr=subprocess.STDOUT)
	procfile = os.fdopen(proc.stdout.fileno())
	server = socket(AF_UNIX, SOCK_STREAM)
	try: os.unlink(serversocket)
	except: pass
	server.bind(serversocket)
	server.listen(10)

	while True:
		rfd, wfd, xfd = select.select([proc.stdout, server], [], [], 1)
		if proc.stdout in rfd: # we potentially block here if we don't have a whole line :|
			data = procfile.readline()
			print data.rstrip()
			for client in clients:
				try:
					client.send(data)
				except:
					client.close()
					clients.remove(client)
		if server in rfd: # accept a new connection
			client, _ = server.accept()
			clients.append(client)

def init():
	signal.signal(signal.SIGINT, sigHandler)
	loadConfig()
	launch()

if __name__ == '__main__': 
	init()
	
