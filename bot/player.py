
PLAYER_DEFAULTS = ["name", "ip", "team", "model", "sex", "headmodel", "team_model", "team_headmodel", "funred", "funblue", "racered", "raceblue", "color1", "color2", "cg_predictitems", "cl_anonymous", "cl_guid", "cg_rgb", "cg_physics", "weapmodes", "gear", "tematask", "handicap", "rate", "snaps", "ut_timenudge", "password", "challenge", "teamtask", "protocol", "qport"]

class Player(object):
    def __init__(self, cid, game, data={}):
        self.cid = cid
        self.game = game

        for k in PLAYER_DEFAULTS:
            self.__dict__[k] = None

        self.update(data)

    def update(self, data):
        for k, v in data.items():
            if k not in PLAYER_DEFAULTS:
                self.game.log.info("Unknown client-var for update: %s (%s)" % (k, v))
            else:
                self.__dict__[k] = v

    def init(self): pass
