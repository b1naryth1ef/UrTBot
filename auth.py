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


def level1(db, guid, ip, nick):
	#- Method 1: User must match GUID/IP/NICK to be auto-logged in
	cl = db.clientSearch({'guid':guid,'lastip':ip,'nick':nick})
	if cl != []:
		print cl[0][2] # group, clientSearch will return something nicer someday..
		return cl[0][2]
	return 0

def level2(db, guid, ip, nick):
	#- Method 2: User must match GUID/IP, GUID/NICK to be auto-logged in...
	pass

def level3(db, guid, ip, nick): 
	#- Method 3: User must match GUID/IP, GUID/NICK or IP/NICK to be auto-logged in
	pass

def level4(db, guid, ip, nick):
	#- Method 4: User must match NICK to be logged in...
	cl = db.clientSearch({'nick':nick})
	if cl != []:
		print cl[0][2] # group, clientSearch will return something nicer someday..
		return cl[0][2]
	return 0


levelz = {
	1:level1,
	2:level2,
	3:level3,
	4:level4
}

def checkUserAuth(db, guid, ip, nick):
	return levelz[sec_level](db,guid,ip,nick)

