import sys
import time
from config import dbConfig

__import__('db.' + dbConfig['database_type'])
db_plugin = sys.modules['db.' + dbConfig['database_type']]

class Client:
	""" container class to make manipulating client db entries simpler
		things that also exist in the running bot's Clients dict should be named
		the same here
	"""
	def __init__(self, info=(0,0,'','','','',0,0,0)):
		self.id = info[0]
		self.group = info[1] # cgroup in db
		self.name = info[2] # nick in db (should be changed?)
		self.cl_guid = info[3] # guid in db
		self.password = info[4]
		self.ip = info[5]
		self.joincount = info[6]
		self.firstjoin = info[7]
		self.lastjoin = info[8]

class DB(db_plugin.DBPlugin):
	def __init__(self):
		db_plugin.DBPlugin.__init__(self)
		self.connect(dbConfig)

	def clientAdd(self, client):
		cl = self.clientSearch({'guid':client.cl_guid})
		if cl != []:
			print "Tried to add player to DB: guid is already used"
			return 0
		else:
			ipOnly = client.ip.split(":")[0]
			count = self.addRow('clients', {'id':None, 'cgroup':client.group, 'nick':client.name, 
			'guid':client.cl_guid, 'password':"", 'ip':ipOnly, 'joincount':1,
			'firstjoin':int(time.time()), 'lastjoin':int(time.time())})
			if count: self.commit()
			return count

	def clientDel(self, client):
		count = self.delRow('clients', {'guid':client.cl_guid})
		if count: self.commit()
		return count

	def clientModify(self, client, fields):
		cl = self.clientSearch({'guid':client.cl_guid})
		if cl == []:
			print "Tried to modify a player that doesn't exist in db!"
			return 0
		for key in fields:
			self.setField('clients', {'guid':client.cl_guid}, key, fields[key])
		self.commit()
		return 1

	def clientSearch(self, values):
		cllist = []
		rows = self.getRow('clients', values)
		for info in rows:
			cllist.append(Client(info))
		return cllist

	def clientUpdate(self, client):
		if client.ip == 'bot': return

		cl = self.clientSearch({'guid':client.cl_guid})
		if cl != []:
			# already in db, update fields
			count = self.getField('clients', {'guid':client.cl_guid}, 'joincount')
			count = count[0][0] + 1
			self.clientModify(client, {'lastjoin':int(time.time()), 'joincount':count})
		else:
			self.clientAdd(client)

	def penaltyAdd(self, client, type, length): pass

	def penaltyDel(self): pass
	def penaltyModify(self): pass
	def penaltySearch(self): pass
	def penaltySelect(self): pass

	def tableCreate(self, table, info):
		self.addTable(table, info)

	def tableExists(self, table):
		return self.checkTable(table);

		
	def defaultTableSet(self):
		if self.tableExists("clients") == True: print "Table 'clients' already exists."
		else:
			self.addTable('clients', {'id':'integer primary key autoincrement',
			'cgroup':'integer', 'nick':'text', 'guid':'text', 'password':'text',
			'ip':'text', 'joincount':'integer', 'firstjoin':'integer',
			'lastjoin':'integer'})

		if self.tableExists("penalties") == True: print "Table 'penalties' already exists."
		else:
			self.addTable('penalties', {'id':'integer primary key', 'userid':'integer',
			'adminid':'integer', 'type':'text', 'time':'integer', 'expiration':'integer'})
		self.commit()

if __name__ == '__main__':
	db = DB()		
	print "Making default tables..."
	try:
		db.defaultTableSet()
	except Exception, e:
		print "Ruh roh! Failed because %s." % e
		sys.exit()

	# ABSOLUTELY ONLY FOR TESTING, use security level 4 (nick only)
	print "Adding dummy uberadmin with name 'uberadmin' for testing..."
	client = Client()
	client.group = 5 # cgroup in db
	client.name = 'uberadmin' # nick in db (should be changed?)
	client.cl_guid = 'THISISNOTAREALGUIDOMGTHISISCOOLZ' # guid in db (should be 32 chars long)
	client.ip = '127.0.0.1'
	try:
		db.clientAdd(client)
	except Exception, e:
		print "Ate shit while adding test user, go fig. (It's neeks fault btw)"
		sys.exit()
	# ==================================================	

	print "All done!"