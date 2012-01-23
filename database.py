import sys
import time
from config import dbConfig
from buzhug import TS_Base #Thread safety anyone?
from datetime import date, datetime

#__import__('db.' + dbConfig['database_type'])
#db_plugin = sys.modules['db.' + dbConfig['database_type']]
glob = None
db = None
az = ['cgroup', 'nick', 'guid', 'password', 'ip', 'joincount', 'firstjoin', 'lastjoin']
botaz = ['nick', 'guid', 'ip']

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

#Idk, but I might have done this in a stupid way. This is kinda just a demo of how it should work
#I feel like if we actually just used this, we would get conflicts with push/pull.
#Probablly use this IDEA and implement it into the player, but only push NICK/GUID/IP, because
#we know those are constant, and the Player class should have them correct because it gets them
#straight from the game
class Client():
	def __init__(self, nick, guid=None, ip=None, group=0, password='', joincount=0, firstjoin=None, lastjoin=None, db=db):
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

		self.insert()

	def dict(self, f): #@NOTE hacky anyone?
		r = {}
		for i in self.__dict__.keys():
			if i in f and i != '__id__':
				r[i] = self.__dict__[i]
		return r

	def clientJoin(self):
		row = self.find()
		if row != None:
			if self.firstjoin == None:
				self.firstjoin = datetime.now()
			self.lastjoin = datetime.now()
			self.joincount += 1
			self.push()

	def find(self):
		if self.__id__ == None:
			q1 = self.db.select_for_update(az, guid=self.guid, ip=self.ip)
			if len(q) == 1: return q[0]
			else: return None
		else:
			return self.db.select_for_update(az, __id__=self.__id__)[0]

	def pull(self):
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

	def push(self, pushall=False):
		row = self.find()
		if row != None:
			if pushall is True:
				row.update(**self.dict(az))
			elif pushall is False:
				row.update(**self.dict(botaz))

	def insert(self):
		if self.find() == None:
			db.insert(**self.dict(az))
			self.push(True) #We're inserting, so assume all our data is correct/sterile
			self.pull()

def init():
	global db
	db = TS_Base('/tmp/urtbot_beta.db').create(('cgroup',int), ('nick',str), ('guid',str), ('password',str), ('ip',str), ('joincount',int), ('firstjoin',date), ('lastjoin', date), mode="open")
	return db

def close():
	global db
	db.close()

def testConnection():
	print 'Testing connection...'
	global db
	init()
	#db.insert(nick='Joe', client=cli)
	JOE = Client('Joe', 'GUID', '127.0.0.1', 5, '', 1, db=db)
	JIM = Client('Jim', 'GUID2', '127.0.0.2', 3, '', 4, db=db)
	JIM.clientJoin()
	print [r for r in db]
	close()

if __name__ == '__main__':
	testConnection()