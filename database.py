import sys
import time
from config import dbConfig
from buzhug import TS_Base #Thread safety anyone?
from datetime import date

#__import__('db.' + dbConfig['database_type'])
#db_plugin = sys.modules['db.' + dbConfig['database_type']]
glob = None
db = None
az = ['cgroup', 'nick', 'guid', 'password', 'ip', 'joincount', 'firstjoin', 'lastjoin']


class Client():
	def __init__(self, nick, group, guid, password, ip, joincount, firstjoin, lastjoin, db):
		self.nick = nick
		self.cgroup = group
		self.guid = guid
		self.password = password
		self.ip = ip
		self.joincount = joincount
		self.firstjoin = firstjoin
		self.lastjoin = lastjoin

		self.__id__ = None
		self.db = db

	def dict(self): #@NOTE hacky anyone?
		r = {}
		for i in self.__dict__.keys():
			if i in az and i != '__id__':
				r[i] = self.__dict__[i]
		return r

	def clientJoin(self):
		if self.__id__ == None:
			query = [r for r in self.db if r.nick == self.nick and r.guid == self.guid]
			if len(query) > 1:
				return False
			else:
				x = query[0]
				self.joincount += 1
				db.update(aston, nick=self.nick, cgroup=self.group,)

	def find(self):
		if self.__id__ == None:
			q = self.db.select_for_update(az, nick=self.nick, guid=self.guid, ip=self.ip)
			if len(q) == 1:
				return q[0]
			else:
				return None
		else:
			return self.db.select_for_update(az, __id__=self.__id__)[0]

	def pull():
		row = self.find()
		if row != None:
			self.nick = row.nick
			self.cgroup = row.cgroup
			self.ip = row.ip
			self.guid = row.guid
			self.password = row.password
			self.joincount = row.joincount
			self.firstjoin = row.firstjoin
			self.lastjoin = row.firstjoin
			self.__id__ = row.__id__

	def push(self):
		row = self.find()
		if row != None:
			row.update(**self.dict())

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
	JOE = Client('Joe', 5, 'GUID', '', '127.0.0.1', 1, date(2011, 1, 1), date(2011, 1, 1), db)
	db.insert(nick='Joe', guid='GUID', joincount=0, ip='127.0.0.1')
	JOE.push()
	#JOE.clientJoin()
	# f = [r for r in db if r.nick == "Joe" ][0]
	# f.joincount += 1
	#f = [r for r in db if r.nick == "Joe" ][0]
	#f = db.select_for_update(az, __id__=0)
	#f[0].joincount += 1
	#f[0].update(joincount=f[0].joincount)
	print [r for r in db if r.nick == "Joe" ][0]
	close()

if __name__ == '__main__':
	testConnection()