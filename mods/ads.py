_name = "Advert Plugin"
_author = "B1naryth1ef"
_version = 0.1

try:
	from config import adsconfig
except:
	print "Cannot find 'adsconfig.py' in mods/config/."
	

def init(API): pass