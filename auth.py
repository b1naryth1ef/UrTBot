from const import ConfigError

sec_level = None
sec_multi = None

def load():
	from config import securityConfig
	global sec_level
	sec_level = securityConfig['level']
	sec_multi = securityConfig['multi']
	if sec_level > 4: raise ConfigError('Unknown Security Level (%s)' % (sec_level))
	elif sec_level == 4: print "[WARNING] Security Level 4 is NOT RECOMMENDED!"


def level1(ip, guid, nick):
	#- Method 1: User must match GUID/IP/NICK to be auto-logged in
	if ip != None and guid != None and nick != None: 
		#Maybe a match, check if they are all the same
		pass
	else:
		return False

def level2():
	#- Method 2: User must match GUID/IP, GUID/NICK to be auto-logged in...
	pass

def level3(): 
	#- Method 3: User must match GUID/IP, GUID/NICK or IP/NICK to be auto-logged in
	pass

def level4():
	#- Method 4: User must match NICK to be logged in...
	pass

levelz = {
	1:level1,
	2:level2,
	3:level3,
	4:level4
}

def checkUserAuth(db, guid, ip, nick):
	xip = db.clientSearch(ip=ip)
	xguid = db.clientSearch(guid=guid)
	xnick = db.clientSearch(nick=nick)

	return levelz[sec_level](xip,xguid,xnick)

