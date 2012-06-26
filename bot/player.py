import sys, os, time
import database, const
from debug import log
from datetime import datetime
from const import RED_TEAM, BLUE_TEAM, SPEC_TEAM

class Player():
    def __init__(self, cid, data, api):
        self.uid = -1 #User ID which is gotten from the DATABASE
        self.cid = int(cid) #Client ID which is gotten from the GAME
        self.data = data
        self.status = None
        self.score = [0,0]
        self.api = api
        self.A = self.api.A
        self.joined = datetime.now()
    
        try:
            self.name = None
            self.ip = None
            self.team = None
            self.model = None
            self.sex = None
            self.headmodel = None
            self.team_model = None
            self.team_headmodel = None
            self.funred = None
            self.funblue = None
            self.raceRed = None
            self.raceBlue = None
            self.color1 = None
            self.color2 = None
            self.cg_predictitems = None
            self.cg_anonymous = None
            self.cl_guid = None
            self.cg_rgb = None
            self.cg_physics = None
            self.weapmodes = None
            self.gear = None
            self.teamtask = None
            self.handicap = None
            self.rate = None
            self.snaps = None
            self.ut_timenudge = None
            self.setData(self.data)
        except Exception, e:
            print e

        self.getClient()
        
    def getClient(self):
        q1 = [i for i in database.User.select().where(name=self.name.lower(), ip=self.ip, guid=self.cl_guid)]
        q2 = [i for i in database.User.select().where(ip=self.ip, guid=self.cl_guid)]
        q3 = [i for i in database.User.select().where(ip=self.ip, name=self.name.lower())]
        q4 = [i for i in database.User.select().where(guid=self.cl_guid)]

        if len(q1) or len(q2) or len(q3) or len(q4):
            q = []
            for cli in [i[0] for i in [q1, q2, q3, q4] if len(i)]:
                if cli not in q: q.append(cli)
                if len(q) == 1: self.client = q[0]
                else: log.warning('Found more than one result for %s, %s, %s (%s results)' % (self.name, self.ip, self.cl_guid, len(q)))
        else: self.client = database.User(name=self.name.lower(), ip=self.ip, guid=self.cl_guid, group=0, joincount=0, firstjoin=datetime.now())

        self.client.lastjoin = datetime.now()
        self.client.joincount += 1
        self.client.save()
        self.uid = self.client.id

    def checkTeam(self): pass #@TODO

    def tell(self, msg):
        self.api.Q3.tell(self, msg)

    def kick(self, msg="Kicked!"):
        self.api.Q3.kick(self, msg)

    def changeGroup(self, group): pass
    def checkAuth(self): pass

    def setData(self, data):
        if 'name' in data.keys(): self.name = data['name']
        if 'team' in data.keys() and self.team != None and self.team != data['team']:
            self.A.fireEvent('CLIENT_TEAM_SWITCH', {'client':self, 'to':data['team'], 'from':self.team})
            self.team = data['team']
        self.__dict__.update(data)

    def __repr__(self):
        return "<Player '%s' with IP %s, CID %s, UID %s, GUID %s>" % (self.name, self.ip, self.cid, self.uid, self.cl_guid)
