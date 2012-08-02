from socket import *
import thread, struct
import sys, os, time
from pprint import pprint

COMMANDS = {}
VARS = {
	'g_gametype':['4', '0'],
	'mapname':['ut4_casa', 'nomap'],
}
prefix = "\xFF\xFF\xFF\xFF"

logfile = {}

def getSec(s):
    l = s.split(':')
    return int(l[0]) * 60 + int(l[1])

class FakePlayer():
	def __init__(self): pass

class FakeServer():
	def __init__(self, name, log):
		self.name = name
		self.log = log
		self.players = {}
		self.timedelta = 0

	def run(self):
		self.logparser()
		self.playback()

	def _split(self, line):
		line = line.strip()
		line = line.split(' ', 1)
		return getSec(line[0]), line[1]

	def logparser(self):
		with open(self.log, 'r') as f:
			l = f.readlines()
			l1 = self._split(l[0])
			self.timedelta = l1[0]
			for line in l:
				line = self._split(line)
				if line[0] in logfile.keys():
					logfile[line[0]].append(line[1])
				else:
					logfile[line[0]] = [line[1]]
	
	def playback(self):
		stopat = max(logfile.keys())
		while True:
			if self.timedelta in logfile.keys():
				for i in logfile[self.timedelta]:
					print i
			time.sleep(1)
			self.timedelta += 1
			if self.timedelta > stopat:
				return

def sendVar(sock, src, var): 
	value = VARS[var]
	sock.sendto(prefix+'print\n"%s" is:"%s^7" default:"%s^7"\n' % tuple([var,]+value), src)

def rconThread():
	sock = socket(AF_INET, SOCK_DGRAM)
	sock.bind(('', 27960))

	while True:
		rx, src = sock.recvfrom(4096)

		if len(rx) <= 4 or not rx.startswith('\xFF\xFF\xFF\xFF'):
			continue

		rxparts = rx[4:].split()
		if rxparts[2] in COMMANDS.keys():
			COMMANDS[rxparts[2]](sock, src, rxparts)
		else:
			if rxparts[2] in VARS.keys():
				sendVar(sock, src, rxparts[2])

thread.start_new_thread(rconThread, ())
f = FakeServer('test', 'test.log')
f.run()
