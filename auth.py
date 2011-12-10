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
	clist = db.rowFindAll(guid)
	for cl in clist:
		if cl['ip'] == ip and cl['nick'] == nick: return cl['cgroup']
	return 0

def level2(db, guid, ip, nick):
	#- Method 2: User must match GUID/IP, GUID/NICK to be auto-logged in...
	clist = db.rowFindAll(guid)
	for cl in clist:
		if cl['ip'] == ip or cl['nick'] == nick: return cl['cgroup']
	return 0

def level3(db, guid, ip, nick): 
	#- Method 3: User must match GUID/IP, GUID/NICK or IP/NICK to be auto-logged in
	pass

def level4(db, guid, ip, nick):
	#- Method 4: User must match NICK to be logged in...
	cl = db.rowFind(nick, 'nick')
	if cl != None:
		return cl['cgroup']
	return 0


levelz = {
	1:level1,
	2:level2,
	3:level3,
	4:level4
}

def checkUserAuth(db, guid, ip, nick):
	if ip == "bot": return 0 # skip 'em
	ipOnly = ip
	try:
		ipOnly = ip.split(":")[0]
	except: print "[WARNING] Bad IP passed to auth"

	return levelz[sec_level](db,guid,ipOnly,nick)

