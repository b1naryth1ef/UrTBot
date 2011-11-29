from init import A
import time

_name = "Advert Plugin"
_author = "B1naryth1ef"
_version = 0.1

default_messages = [
'Checkout the UrTBot, an open source project, on github!',
'Type ^1!help^3 in chat for more commands!',
'Type ^1!about^3 in chat for more information!',
'W^100^3t! This servers on ^1fire^3!']
default_length = 120

try:
	from config import adsconfig
	msg = adsconfig['messages']
	leng = adsconfig['time_delay'] #@NOTE This should be a integer
	A.debug('Loaded config correctly...', _name)
except:
	A.debug('Was not able to load config... using default messages', _name)
	print "Cannot find 'adsconfig.py' in mods/config/... using default messages." #<<<< This is just for users not using debug
	msg = default_messages
	leng = default_length

def init():
	x = 0
	while A.B.status == 1:
		if len(msg) > x: x = 0
		else:
			time.sleep(leng)
			A.say(msg[x])
			x+=1


