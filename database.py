import sys
import time
from config import dbConfig

__import__('db.' + dbConfig['database_type'])
db_plugin = sys.modules['db.' + dbConfig['database_type']]

class DB(db_plugin.DBPlugin):
	def __init__(self):
		db_plugin.DBPlugin.__init__(self)
		self.connect(dbConfig)

	def clientAdd(self, client):
		cl = self.clientSearch('guid', client.cl_guid)
		if cl != []:
			print "Tried to add player to DB: guid is already used"
			return 0
		else:
			count = self.addRow('clients', {'id':None, 'cgroup':0, 'nick':client.name, 
			'guid':client.cl_guid, 'password':"", 'lastip':client.ip, 'joincount':1,
			'firstjoin':int(time.time()), 'lastjoin':int(time.time())})
			print "in clientadd", count
			if count: self.commit()
			return count

	def clientDel(self, client):
		count = self.delRow('clients', {'guid':client.cl_guid})
		if count: self.commit()
		return count

	def clientModify(self, client): pass
	def clientSearch(self, field, value):
		return self.getRow('clients', {field:value})

	def clientUpdate(self, client):
		cl = self.clientSearch('guid', client.cl_guid)
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
		self.addTable('clients', {'id':'integer primary key',
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
	print "All done!"