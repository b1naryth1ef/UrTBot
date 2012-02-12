import sys, time
from init import config
from buzhug import TS_Base #Thread safety anyone?
from datetime import date, datetime

glob = None
db = None
pendb = None
az = ['cgroup', 'nick', 'guid', 'password', 'ip', 'joincount', 'firstjoin', 'lastjoin']
botaz = ['nick', 'guid', 'ip']

class Client():
    def __init__(self, nick, guid=None, ip=None, group=0, password='', joincount=0, firstjoin=None, lastjoin=None, db=None):
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
            q = self.db.select_for_update(az, guid=self.guid, ip=self.ip)
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

    def pullField(self, field):
        row = self.find()
        if row != None:
            self.__dict__[field] = row.__dict__[field]

    def pushField(self, field):
        row = self.find()
        if row != None:
            row.update(**self.dict(field))

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
            self.push(True) #Inserting, so assume all our data is correct/sterile
            self.pull()

def init():
    global db, pendb
    db = TS_Base(config.dbConfig['database']+'/client_database.db').create(('cgroup',int), ('nick',str), ('guid',str), ('password',str), ('ip',str), ('joincount',int), ('firstjoin',date), ('lastjoin', date), mode="open")
    #pendb = TS_Base('/tmp/urtbot/penaltiles.db')
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