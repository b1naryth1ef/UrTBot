from database import User, UserData
from datetime import datetime

PLAYER_DEFAULTS = ["name", "ip", "team", "model", "sex", "headmodel", "team_model", "team_headmodel", "funred", "funblue", "racered", "raceblue", "color1", "color2", "cg_predictitems", "cl_anonymous", "cl_guid", "cg_rgb", "cg_physics", "weapmodes", "gear", "tematask", "handicap", "rate", "snaps", "ut_timenudge", "password", "challenge", "teamtask", "protocol", "qport", "authc"]
PLAYER_SHORT_KEY = { #Transalate ClientUserInfoChange to PLAYER_DEFAULTS
    "t": "team",
    "n": "name"
}

class Player(object):
    def __init__(self, cid, bot, data={}):
        self.cid = cid
        self.bot = bot
        self.user = None

        for k in PLAYER_DEFAULTS:
            self.__dict__[k] = None

        self.snap = data

        #Auth
        self.auth_name = None
        self.auth_level = 0
        self.auth_notoriety = None

        #Locked
        self.last_cmd = 0
        self.health = 100

    def rcon(self, q):
        return self.bot.rcon(q.format(self.cid, id=self.cid))

    def init(self):
        self.bot.log.info("Init called for player %s" % self.name)
        q = User.select().where(User.authname == self.auth_name)
        if not q.count():
            self.bot.log.info("Creating new user for player %s" % self.auth_name)
            self.user = User()
            self.user.authname = self.auth_name
        else:
            self.user = q[0]
            self.bot.info("Found user %s in DB with id %s" % (self.auth_name, self.user.id))

        if self.bot.db.track:
            q = UserData.select().where(UserData.ip == self.ip)
            if q.count():
                for g in q:
                    g.count += 1
                    g.save()
            else:
                a = UserData(name=self.name, ip=self.ip, user=self.user).save()


        self.user.last_connect = datetime.now()
        self.user.connections += 1
        self.user.save()

    def changeHook(self, key, value):
        if not self.bot.db.track: return
        if key == 'name':
            q = UserData.select().where(UserData.name == self.name)
            if q.count():
                for g in q:
                    g.count += 1
                    g.save()
            else:
                UserData(name=self.name, ip=self.ip, user=self.user).save()


    def changeSnap(self):
        if self.snap != {}:
            for k, v in self.snap.items():
                if k not in self.__dict__.keys():
                    self.bot.log.warning("Key %s from snap was not in Player object %s" % (k, obj))
                    continue

                if self.__dict__[k] != v:
                    self.bot.log.debug("Player attr %s changed from %s to %s on changeSnap()" % (k, self.__dict__[k], v))
                     g.api.callHook("PLAYER_ATTR_CHANGE", name=k, a=self.__dict__[k], b=v)
                     self.changeHook(k, v)
                    self.__dict__[k] = v
        self.snap = {}

    def handleUserInfo(self, data):
        for k, v in data.items():
            if k in PLAYER_DEFAULTS:
                self.snap[k] = v
            else:
                self.bot.log.warning("Unknown client-var for key %s (%s)" % (k, v))
        self.changeSnap()

    def handleUserInfoChanged(self, data):
        for k, v in data.items():
            if k in PLAYER_SHORT_KEY:
                self.snap[PLAYER_SHORT_KEY[k]] = v
        self.changeSnap()

    def tell(self, msg):
        self.bot.rcon.rcon("tell %s %s" % (self.cid, msg))
