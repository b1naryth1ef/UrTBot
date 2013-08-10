import const, thread, time, random
from parser import PARSE_SW, PARSE_RE
from api import FiredEvent, API
from database import DatabaseManager

CURRENT_PROTO_VER = 68


class Bot(object):
    """
    A bot is an instance of the bot,
    it should work on ONE server and
    is entirely indepedent of any other
    bots.
    """

    def __init__(self, config, rcon, inter, log):
        self.config = config
        self.rcon = rcon
        self.inter = inter
        self.log = log
        self.db = DatabaseManager(self.config, self.log)
        self.api = API(self, self.log)

        self.players = {}

        #Info
        self.alive = False
        self.cmd_prefix = config.prefix

        #Cvars
        self.g_gametype = None
        self.mapname = None

    def recover(self): pass

    def startup(self):
        self.proto = self.rcon.getCvar("protocol")
        self.version = self.rcon.getCvar("version")
        self.g_gametype = self.rcon.getCvar("g_gametype")
        self.mapname = self.rcon.getCvar("mapname")
        self.inter.connect(self.config.usockname)

        if not isinstance(self.proto, int):
            return self.log.error("Protocol is not an integer: %s" % self.proto)
        elif int(self.proto) != CURRENT_PROTO_VER:
            return self.log.error("Invalid protocol version: %s" % self.proto)

        if not isinstance(self.g_gametype, int):
            return self.log.error('g_gametype is not an integer: %s' % self.g_gametype)
        elif self.g_gametype not in const.GAMETYPES:
            return self.log.error("Invalid g_gametype: %s" % self.g_gametype)

        # Do we need to recover?
        self.recover()

        # Lets logs some shit...
        self.log.info('UrTBot detected server w/ Version: "%s" and Protocol: "%s"' % (self.version, self.proto))
        self.log.info("Server is on map %s playing gametype %s" % (self.mapname, const.GAMETYPES[self.g_gametype].upper()))
        self.api.loadPlugins()

        # Get ready to chat
        self.rcon.rcon(const.C('sv_sayprefix "{C_GREEN}[{C_RED}B0T{C_GREEN}] {C_ORANGE}"'))
        self.rcon.rcon(const.C('sv_tellprefix "{C_GREEN}[{C_RED}B0T{C_GREEN}] {C_CYAN}"'))
        self.rcon.rcon('say UrTBot Version %s started up! "%s" ' % (self.version, random.choice(const.MOTTOS)))

        return True

    def parse(self, line):
        self.log.debug("Parsing line '%s'" % line.strip())
        for SW in PARSE_SW:
            if line.startswith(SW):
                PARSE_SW[SW](self, line)

    def run(self):
        if not self.startup(): return False
        self.alive = True
        thread.start_new_thread(self.mainLoop, ())

        while self.alive:
            time.sleep(5) #We will do stuff here at a later time

    def mainLoop(self):
        while self.alive:
            self.inter.checkAndRead()
            while self.inter.hasLine():
                line = self.inter.getLine()
                if line not in const.IGNORES:
                    self.parse(line)
