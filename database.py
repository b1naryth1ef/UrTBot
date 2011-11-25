import sys
from config import dbConfig

__import__('db.' + dbConfig['database_type'])
db_plugin = sys.modules['db.' + dbConfig['database_type']]

class DB(db_plugin.DBPlugin):
	def __init__(self):
		db_plugin.DBPlugin.__init__(self)
		self.connect(dbConfig)

	def clientAdd(self): pass
	def clientDel(self): pass
	def clientModify(self): pass
	def clientSearch(self, field, value): pass

	def clientSelect(self): pass

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
		self.addTable('clients', {'id':'integer', 'cgroup':'integer', 'nick':'text',
		'guid':'text', 'password':'text', 'ip':'text', 'lastip':'text'})

		self.addTable('penalties', {'id':'integer', 'userid':'integer',
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
