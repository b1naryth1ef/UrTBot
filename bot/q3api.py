from debug import log

class Q3API():
    def __init__(self, bot):
        self.B = bot
        self.Q = bot.Q
        self.R = bot.Q.rcon

        #@CHECK 4.2
        self.prefix = self.B.prefix
        self.saylength = 69
        self.telllength = 64

    def _rp(self, plyr):
        '''Takes plyr/str/int and returns cid (int)'''
        if isinstance(plyr, Player): return plyr.cid
        elif plyr.isdigit(): return int(plyr)
        else: return plyr

    def _demo(self, act, plyr, allplyr):
        '''Toggle wrapper'''
        if allplyr: plyr = 'all'
        else: plyr = self._rp(plyr)
        log.debug('%s demo on %s' % (act.title(), plyr))
        return self.R('%sserverdemo %s' % (act, plyr))

    def say(self, msg):
        log.debug("Saying: %s" % msg)
        return self.R('say "%s"' % (self.Q.format('^3'+msg, self.saylength)))

    def tell(self, plyr, msg):
        log.debug('Telling %s: %s' % (plyr, msg))
        return self.R('tell %s "%s"' % (self._rp(plyr), self.Q.format('^3'+msg, self.telllength)))

    def force(self, plyr, team):
        log.debug('Forcing %s to %s' % (plyr, team))
        return self.R('forceteam %s %s' % (self._rp(plyr), team.urt))

    def kick(self, plyr, reason):
        log.debug('Kicking %s' % plyr)
        return self.R('kick %s "%s"' % (self._rp(plyr), reason))

    def smite(self, plyr): #@CHECK 4.2
        log.debug('Smiting %s' % plyr)
        return self.R('smite %s' % self._rp(plyr))

    def startDemo(self, plyr, allplyr=False): #@CHECK 4.2
        self._demo('start', plyr, allplyr)

    def stopDemo(self, plyr, allplyr=False): #@CHECK 4.2
        self._demo('stop', plyr, allplyr)

    def getObj(self, txt, reply=None):
        if txt.startswith('@') and txt[1:].isdigit():
            return [i for i in self.B.Clients.values() if i.uid == int(txt[1:])][0]
        elif txt.isdigit() and int(txt) in self.B.Clients.keys(): 
            return self.B.getClient(int(txt))
        else:
            u = [i for i in self.B.Clients.values() if txt.lower() in i.name.lower()]
            if len(u) == 1: return u
            if reply and len(u) > 1:
                reply('^1Found more than one user for your query! Try again with a more specific search term!')
            elif reply:
                reply('^1Could not find user! Try again, and remember to place an @ in front of names containg numbers!')

    def getAdminList(self):
        return [i.name for i in self.B.Clients.values() if i.user.group == self.B.A.config.botConfig['leetlevel']]
