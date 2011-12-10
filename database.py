import sys
import time
from config import dbConfig

__import__('db.' + dbConfig['database_type'])
db_plugin = sys.modules['db.' + dbConfig['database_type']]

class DB(db_plugin.DBPlugin):
	def __init__(self):
		db_plugin.DBPlugin.__init__(self)
		self.connect(dbConfig)
		
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
"""
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
"""
	print "All done!"