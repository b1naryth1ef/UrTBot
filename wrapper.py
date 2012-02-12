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
	from config_handler import ConfigFile
	global serverexe, serversocket
	botConfig = ConfigFile().botConfig
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

	
if __name__ == '__main__': 
	init()
	
