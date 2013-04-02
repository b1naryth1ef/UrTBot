

class Q3API():
    def __init__(self, bot):
        self.bot = bot
        self.rcon = bot.rcon

    def r(self, *args, **kwargs):
        return self.rcon.rcon(*args, **kwargs)

    def say(self, msg):
        return self.r("say %s" % '^3'+msg)
