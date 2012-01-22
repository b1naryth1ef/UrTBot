import sys
import time
from config import dbConfig
from buzhug import TS_Base #Thread safety anyone?

#__import__('db.' + dbConfig['database_type'])
#db_plugin = sys.modules['db.' + dbConfig['database_type']]
glob = None
# {'id':'integer primary key autoincrement',
# 			'cgroup':'integer', 'nick':'text', 'guid':'text', 'password':'text',
# 			'ip':'text', 'joincount':'integer', 'firstjoin':'integer',
# 			'lastjoin':'integer'})


class DB():
	def __init__(self, config):
		self.config = config
		self.db = None

	def connect(self):
		path = self.config['database']
		try:
			self.c = TS_Base(path).open()
			print 'BuzHug database found, opening...'
		except IOError as e:
			print 'No BuzHug database found, creating new...'
			self.c = TS_Base(path)
			self.c.create(('cgroup',int), ('nick',str), ('guid',str))
		return self

	def disconnect(self):
		self.c.close()

def init(): pass

def testConnection():
	x = DB({'database':'/tmp/urtbot_test_database.db'}).connect()
	x.disconnect()

if __name__ == '__main__':
	testConnection()