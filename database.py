import sys
import time
from config import dbConfig
from buzhug import TS_Base #Thread safety anyone?

#__import__('db.' + dbConfig['database_type'])
#db_plugin = sys.modules['db.' + dbConfig['database_type']]
glob = None
db = None

def init():
	global db
	db = TS_Base('/tmp/urtbot_beta.db').create(('cgroup',int), ('nick',str), ('guid',str), ('password',str), ('ip',str), ('joincount',int), ('firstjoin',int), ('lastjoin', int), mode="open")

def close():
	global db
	db.close()

def testConnection():
	global db
	init()
	db.insert(nick='Joe')
	print [r for r in db if r.nick == "Joe" ][0]
	close()

if __name__ == '__main__':
	testConnection()