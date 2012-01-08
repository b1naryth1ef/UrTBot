from const import ConfigError

sec_level = None
sec_multi = None

def load():
	from config import securityConfig
	global sec_level
	sec_level = securityConfig['level']
	sec_multi = securityConfig['multi']
	if sec_level > 4: raise ConfigError('Unknown Security Level (%s)' % (sec_level))
	elif sec_level == 4: print "[WARNING] Security Level 4 is EXTREMLY unsecure! It authorizes users by simply there NICKNAME!"
	elif sec_level == 1: print "[WARNING] Security Level 1 is a little over-secure. We do NOT recommend it for production."

def level0(db, guid, ip, nick): 
	#- Method 0: Dynamic
	pass

def level1(db, guid, ip, nick):
	#- Method 1: User must match GUID/IP/NICK to be auto-logged in
	guidList = db.rowFindAll(guid, 'guid')
	ipList = db.rowFindAll(ip, 'ip')
	nickList = db.rowFindAll(nick, 'nick')

	if guidList != None:
		for cl in guidList:
			if cl['ip'] == ip and cl['nick'] == nick: return (cl, cl['cgroup'])
	if ipList != None:
		for cl in ipList:
			if cl['guid'] == guid and cl['nick'] == nick: return (cl, cl['cgroup'])
	if nickList != None:
		for cl in nickList:
			if cl['ip'] == ip and cl['guid'] == guid: return (cl, cl['cgroup'])
	return (None, 0)

def level2(db, guid, ip, nick):
	#- Method 2: User must match GUID/IP, GUID/NICK to be auto-logged in...
	ipList = db.rowFindAll(ip, 'ip')
	nickList = db.rowFindAll(nick, 'nick')

	if ipList != None:
		for cl in ipList:
			if cl['guid'] == guid: return (cl, cl['cgroup'])
	if nicklist != None:
		for cl in nickList:
			if cl['guid'] == guid: return (cl, cl['cgroup'])
	return (None, 0)

def level3(db, guid, ip, nick): 
	#- Method 3: User must match GUID/IP, GUID/NICK or IP/NICK to be auto-logged in
	pass

def level4(db, guid, ip, nick):
	#- Method 4: User must match NICK to be logged in...
	cl = db.rowFind(nick, 'nick')
	if cl != None:
		return (cl, cl['cgroup'])
	return (None, 0)

levelz = {
	0:level0,
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

