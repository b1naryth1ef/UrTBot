from pyquake3 import PyQuake3

Q = PyQuake3('localhost:27960', rcon_password='123abc')
Q.rcon_update()
for i in Q.players:
	print i.name, i.uid