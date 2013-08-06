
PLAYER_DEFAULTS = ["name", "ip", "team", "model", "sex", "headmodel", "team_model", "team_headmodel", "funred", "funblue", "racered", "raceblue", "color1", "color2", "cg_predictitems", "cl_anonymous", "cl_guid", "cg_rgb", "cg_physics", "weapmodes", "gear", "tematask", "handicap", "rate", "snaps", "ut_timenudge", "password", "challenge", "teamtask", "protocol", "qport", "authc"]
PLAYER_SHORT_KEY = { #Transalate ClientUserInfoChange to PLAYER_DEFAULTS
    "t": "team",
    "n": "name"
}

class Player(object):
    def __init__(self, cid, bot, data={}):
        self.cid = cid
        self.bot = bot

        for k in PLAYER_DEFAULTS:
            self.__dict__[k] = None

        self.snap = data

        #Locked
        self.last_cmd = 0

    def init(self): pass

    def changeSnap(self):
        if self.snap != {}:
            for k, v in self.snap.items():
                if k not in self.__dict__.keys():
                    self.bot.log.warning("Key %s from snap was not in Player object %s" % (k, obj))
                    continue

                if self.__dict__[k] != v:
                    self.bot.log.debug("Player attr %s changed from %s to %s on changeSnap()" % (k, self.__dict__[k], v))
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
