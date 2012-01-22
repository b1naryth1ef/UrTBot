import sys
import time
from config import dbConfig
from buzhug import TS_Base #Thread safety anyone?
from datetime import date

#__import__('db.' + dbConfig['database_type'])
#db_plugin = sys.modules['db.' + dbConfig['database_type']]
glob = None
db = None

class Client():
	def __init__(self, nick, group, guid, password, ip, joincount, firstjoin, lastjoin, db):
		self.nick = nick
		self.group = group
		self.guid = guid
		self.password = password
		self.ip = ip
		self.joincount = joincount
		self.firstjoin = firstjoin
		self.lastjoin = lastjoin

		self.__id__ = None
		self.record = None
		self.db = db

	def clientJoin(self):
		if self.__id__ == None:
			query = [r for r in self.db if r.nick == self.nick and r.guid == self.guid]
			if len(query) > 1:
				return False
			else:
				query[0]
				self.joincount += 1
				db.update(aston, name="Aston Villa")


def init():
	global db
	db = TS_Base('/tmp/urtbot_beta.db').create(('cgroup',int), ('nick',str), ('guid',str), ('password',str), ('ip',str), ('joincount',int), ('firstjoin',date), ('lastjoin', date), mode="open")

def close():
	global db
	db.close()

def testConnection():
	global db
	init()
	#db.insert(nick='Joe', client=cli)
	#JOE = Client('Joe', 5, 'GUID', '', '127.0.0.1', 1, date(2011, 1, 1), date(2011, 1, 1), db)
	#db.insert(nick='Joe', guid='GUID', joincount=0)
	#JOE.clientJoin()
	# f = [r for r in db if r.nick == "Joe" ][0]
	# f.joincount += 1
	#f = [r for r in db if r.nick == "Joe" ][0]
	f = db.select_for_update(['nick', '__id__', 'joincount'], nick='Joe', guid='GUID')
	f[0].joincount += 1
	f[0].update(joincount=f[0].joincount)
	print [r for r in db if r.nick == "Joe" ][0]
	close()

if __name__ == '__main__':
	testConnection()