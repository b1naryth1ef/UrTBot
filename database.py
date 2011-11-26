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
	def __init__(self):
		self.id = 0
		self.group = 0 # cgroup in db
		self.name = '' # nick in db (should be changed?)
		self.cl_guid = '' # guid in db
		self.password = ''
		self.ip = '' # lastip in db (should be changed..)
		self.joincount = 0
		self.firstjoin = 0
		self.lastjoin = 0

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
			count = self.addRow('clients', {'id':None, 'cgroup':client.group, 'nick':client.name, 
			'guid':client.cl_guid, 'password':"", 'lastip':client.ip, 'joincount':1,
			'firstjoin':int(time.time()), 'lastjoin':int(time.time())})
			if count: self.commit()
			return count

	def clientDel(self, client):
		count = self.delRow('clients', {'guid':client.cl_guid})
		if count: self.commit()
		return count

	def clientModify(self, client): pass

	def clientSearch(self, values):
		return self.getRow('clients', values)

	def clientUpdate(self, client):
		cl = self.clientSearch({'guid':client.cl_guid})
		print "got cl, ", cl
		if cl != []:
			# already in db, update fields
			self.setField('clients', {'guid':client.cl_guid}, 'lastip', client.ip)
			self.setField('clients', {'guid':client.cl_guid}, 'lastjoin', int(time.time()))
			count = self.getField('clients', {'guid':client.cl_guid}, 'joincount')
			print "joincount is ", count
			count = count[0][0] + 1
			self.setField('clients', {'guid':client.cl_guid}, 'joincount', count)
			self.commit()
		else:
			self.clientAdd(client)

	def aliasAdd(self): pass
	def aliasDel(self): pass
	def aliasSearch(self): pass
	def aliasSelect(self): pass

	def penaltyAdd(self): pass
	def penaltyDel(self): pass
	def penaltyModify(self): pass
	def penaltySearch(self): pass
	def penaltySelect(self): pass

	def defaultTableSet(self):
		self.addTable('clients', {'id':'integer primary key autoincrement',
		'cgroup':'integer', 'nick':'text', 'guid':'text', 'password':'text',
		'lastip':'text', 'joincount':'integer', 'firstjoin':'integer',
		'lastjoin':'integer'})

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