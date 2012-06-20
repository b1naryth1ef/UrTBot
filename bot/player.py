import sys, os, time
import database, const
from debug import log
from datetime import datetime
from const import RED_TEAM, BLUE_TEAM, SPEC_TEAM

A = None

class Player():
    def __init__(self, cid, data, api):
        global A
        self.uid = -1 #User ID which is gotten from the DATABASE
        self.cid = int(cid) #Client ID which is gotten from the GAME
        self.data = data
        self.status = None
        self.score = [0,0]
        log.debug('Player Init API: %s' % api)
        
        if not A: #@DEV Fix this eventually
            import api
            A = api.A

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

        q1 = [i for i in database.User.select().where(name=self.name, ip=self.ip, guid=self.cl_guid)]
        q2 = [i for i in database.User.select().where(ip=self.ip, guid=self.cl_guid)]
        q3 = [i for i in database.User.select().where(guid=self.cl_guid)]

        if len(q1) or len(q2) or len(q3):
            q = []
            for cli in [i[0] for i in [q1, q2, q3] if len(i)]:
                if cli not in q:
                    q.append(cli)
                if len(q) == 1: self.client = q[0]
                else: log.warning('Found more than one result for %s, %s, %s (%s results)' % (self.name, self.ip, self.cl_guid, len(q)))
        else: self.client = database.User(name=self.name, ip=self.ip, guid=self.cl_guid, group=0, joincount=0, firstjoin=datetime.now())

        self.client.lastjoin = datetime.now()
        self.client.joincount += 1
        self.client.save()

        self.uid = self.client.id
    
    def changeGroup(self, group): pass
    def checkAuth(self): pass

    def setData(self, data):
        log.debug('Data (set): %s' % data)
        data = data['info']
        if 'name' in data.keys(): data['name'] = data['name'].lower()
        if 'team' in data.keys(): data['team'] = const.teams[int(data['team'])]
        for i in data.keys(): #Strip line endings
            data[i] = data[i].strip()
        self.__dict__.update(data)
    
    def updateData(self, data): #@TODO Move this shit out of the class
        log.debug('Data (update): %s' % data)
        #data = data['info']
        if 'name' in data.keys():
            data['name'] = data['name'].lower()
        if 'team' in data.keys():
            if data['team'] != self.team:
                log.debug('Seems the players team has changed! %s >> %s' % (self.team, data['team']))
                A.fireEvent('CLIENT_TEAM_SWITCH', {'client':self, 'to':data['team'], 'from':self.team})
                log.debug('@Updatedata team: %s' % data['team'])
                self.team = const.teams(int(data['team']))
        self.setData(data)
    
    def die(self, meth):
        if meth == 10: log.debug('DIE w/ METH_10: %s' % self.team)
