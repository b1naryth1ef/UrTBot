from init import A
import time

_name = "Adverts"

default_messages = [
'Checkout the UrTBot, an open source project, on github!',
'Type ^1!help^3 in chat for more commands!',
'Type ^1!about^3 in chat for more information!',
'W^100^3t! This servers on ^1fire^3!']
default_length = 80

if 1==1:
	from config import adsconfig
	msg = adsconfig.messages
	leng = adsconfig.time_dela #@NOTE This should be a integer
	A.debug('Loaded config correctly...', _name)
# except:
# 	A.debug('Was not able to load config... using default messages', _name)
# 	print "Cannot find 'adsconfig.py' in mods/config/... using default messages." #<<<< This is just for users not using debug
# 	msg = default_messages
# 	leng = default_length

def init(x=0):
	A.debug('ads.init() was called... looping', _name)
	while True:
		time.sleep(leng)
		A.say(msg[x])
		x+=1
		if x > len(msg): x = 0
		

