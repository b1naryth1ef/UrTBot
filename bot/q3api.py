import thread

class Q3API():
    def __init__(self, bot):
        self.bot = bot
        self.rcon = bot.rcon
        self.delay = .5

    def r(self, *args, **kwargs):
        return self.rcon.rcon(*args, **kwargs)

    def say(self, msg):
        return self.r("say %s" % '^3'+msg)

    def long(self, cmd, msgs):
        def q():
            for num, i in enumerate(msgs):
                self.r(cmd.format(msg=i, num=num))
                time.sleep(self.delay)
        return thread.start_new_thread(q, ())
