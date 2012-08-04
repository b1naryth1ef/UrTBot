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

        self.waitingForBegin = True

        self.hasauth = False
        self.authname = None #@NOTE should always be lowercase
        self.authlevel = 0 #@NOTE integer only
        self.authnotoriety = None
    
        try:
            self.name = None
            self.ip = None
            self.team = SPEC_TEAM
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
            log.debug(e)

    def updateInfo(self, d):
        self.__dict__.update(d)
        
    def getUser(self):
        log.debug('Attempting to get user for %s' % self.__repr__())
        if self.authname and self.hasauth: q = [i for i in database.User.select().where(authname=self.authname)]
        q2 = [i for i in database.User.select().where(guid=self.cl_guid)]
        if self.hasauth and self.authname and len(q): 
            self.user = q[0]
            log.debug('Found user from authinfo! (UID #%s)' % self.user.id)
        elif len(q2) and not self.hasauth: #@DEV dont find users that have auth? 
            self.user = q2[0]
            log.debug('Found user w/o authinfo! (UID #%s)' % self.user.id)
        else: 
            self.user = database.User(
                name=self.name, 
                authname=self.authname,
                authlevel=self.authlevel, 
                joincount=0, 
                firstjoin=datetime.now(),
                level=self.authlevel,
                guid=self.cl_guid,
                ip=self.ip,
                group=0,
                )
            log.debug('Added user with authname "%s"' % self.authname)

        self.user.lastjoin = datetime.now()
        self.user.joincount += 1
        self.user.save()
        self.uid = self.user.id

    def checkTeam(self):
        log.debug('Player Team Verbose: Currently: %s | Players: %s' % (self.team, self.api.Q3.rcon('players')))

    def tell(self, msg):
        self.api.Q3.tell(self, msg)

    def kick(self, msg="Kicked!"):
        self.api.Q3.kick(self, msg)

    def force(self, team):
        self.api.Q3.force(self, team)

    def setData(self, data): #@TODO Fix
        if 'name' in data.keys(): 
            self.name = data['name']
            #self.checkAlias()
        if 'team' in data.keys() and self.team != None and self.team != data['team']: pass
            #self.A.fireEvent('CLIENT_TEAM_SWITCH', {'client':self, 'to':data['team'], 'from':self.team})
            #self.team = data['team']
        self.__dict__.update(data)

    def __repr__(self):
        return "<Player '%s' with IP %s, CID %s, UID %s, GUID %s>" % (self.name, self.ip, self.cid, self.uid, self.cl_guid)
