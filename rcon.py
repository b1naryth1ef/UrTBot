""" rcon.py
Provides the RCON class to communicate with a Q3 server.
Good-ish performance based on automatically retrying the command if a reply
isn't received within a short time. Should be able to spam commands at this puppy
and not worry about any getting dropped or taking forever to send them out.

$ python rcon.py 
elapsed time to send 100 cmds was 52 secs
$ python rcon.py 
elapsed time to send 10 cmds was 4 secs
"""

import socket
import time

class RCON:
	def __init__(self, server='localhost', port=27960, password='password'):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.server = server
		self.port = port
		self.password = password
		self.last_cmd = None
		self.retries = 3 # default number of retries
		self.throttle_time = 0.0 # secs to wait between retries

		self.socket.connect((server, port))
		self.socket.settimeout(0.5)

	def send(self, data):
		self.socket.send('\xFF\xFF\xFF\xFF' + data)

	def recv(self):
		data = None
		try:
			data = self.socket.recv(4096)
		except socket.timeout: pass
		return data

	def rcon(self, cmd):
		self.last_cmd = cmd
		retries = self.retries
		data = None

		while retries > 0 and data == None:
			self.send('rcon "%s" %s' % (self.password, cmd))
			data = self.recv()
			if data == None:
				time.sleep(self.throttle_time)
			retries -= 1

		return data[4:]


if __name__ == '__main__':
	rcon = RCON('localhost', 27960, 'password')
	count = 100
	start = time.time()
	for i in range(0,count): rcon.rcon("say I am counting... %d" % i)
	print "elapsed time to send %d cmds was %d secs" % (count, (time.time() - start))