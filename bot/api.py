# -*- coding: utf-8 -*-
import os, sys, re, time
from q3api import Q3API

class FiredEvent(object):
    def __init__(self, api, name, data={}):
        self._name = name
        self._data = data
        self.api = api
        self.__dict__.update(data)

        self._cancel = False

    def cancel(self): self._cancel = True

    def reply(self, msg):
        if not hasattr(self, "player"):
            return self.api.warning("Someone tried to call .reply() on a FiredEvent w/o player!")
        self.player.tell("[PM] {0}".format(msg))


class Command(object):
    def __init__(self, func, name, binds=[], doc=None, need_args=0):
        self.func = func
        self.binds = binds
        self.binds.append(name)
        self.name = name

        self.need_args = need_args
        self.doc = doc or self.func.__doc__

        self.log = None

    def __repr__(self):
        return "<Command '%s'>" % self.name

    def fire(self, obj):
        self.func(self, obj)

    def add(self, api):
        self.log = api.log
        self.log.debug("Command %s registering command and aliases" % self.name)
        api.addCommand(self)

class API(object):
    def __init__(self, bot, log):
        self.bot = bot
        self.db = bot.db
        self.log = log
        self.hooks = {}
        self.plugins = {}
        self.q3 = Q3API(bot)

        # Commands
        self.commands = []
        self.alias = {}

    def hookChat(self, obj):
        self.log.debug("Calling hookChat w/ %s (%s)" % (obj.msg, obj))
        if obj.msg[0] == self.bot.cmd_prefix:
            # Protect against some insane command spamming
            if time.time()-obj.player.last_cmd < .5:
                return self.log.debug("User %s tried command-spamming!" % (obj.player))

            obj.player.last_cmd = time.time()
            obj.args = obj.msg.split(" ")[1:]

            cmd = obj.msg[1:].split(" ", 1)[0]
            self.log.debug("User %s trying to call command %s" % (obj.player, cmd))
            if cmd in self.alias:
                self.log.info("User %s called command %s" % (obj.player, cmd))
                if self.alias[cmd].need_args and not len(obj.args) == self.alias[cmd].need_args:
                    obj.reply(self.alias[cmd].doc.format(cmd=cmd, prefix=self.bot.cmd_prefix))
                self.alias[cmd].fire(obj)
                return
            self.log.debug("Aliases: %s" % self.alias)
            self.log.info("User %s tried calling command %s, doesn't exist!" % (obj.player, cmd))
            return obj.reply("Command %s doesnt exist! If your stuck, try using !help to get a list of commands." % cmd)

    def callAlias(self, name, obj):
        self.alias[name].fire(obj)

    def addCommand(self, obj):
        if obj in self.commands:
            return self.log.warning("Command @ %s has already been registered!" % obj)
        self.log.debug("Command %s registered!" % obj)
        self.commands.append(obj)

        for ali in obj.binds:
            if ali in self.alias.keys():
                self.log.warning("Alias of %s has already been registered by %s" % (ali, self.alias[ali]))
                continue
            self.log.debug("Adding alias %s to %s" % (ali, obj))
            self.alias[ali] = obj

    def callHook(self, name, **data):
        self.log.debug("Calling hook '%s' w/ '%s'" % (name, data))
        obj = FiredEvent(self, name, data)
        if name in self.hooks:
            [i(obj) for i in self.hooks[name]]
        return obj

    def addHook(self, plugin, hook, func):
        self.log.debug("Adding function '%s' to hook '%s'" % (func, hook))
        if hook in self.hooks: self.hooks[hook].append(func)
        else: self.hooks[hook] = [func]

    def loadPlugins(self):
        self.log.info("Loading Plugins...")
        for i in os.listdir("plugins"):
            if not i[0] in ['.', '_'] and i.endswith('.py'):
                i = i.split('.py')[0]
                if i in self.plugins.keys(): continue
                __import__("plugins.%s" % i)
                mod = sys.modules['plugins.%s' % i]
                for attr in dir(mod):
                    if isinstance(getattr(mod, attr), Plugin):
                        self.loadPlugin(getattr(mod, attr), mod)

    def loadPlugin(self, obj, mod):
        self.plugins[obj.name] = obj
        self.plugins[obj.name].load(self, mod, self.log)

class Plugin():
    def __init__(self, name="NullPlugin", version=0.1, author="Null"):
        self.realname = name.lower().replace(' ', '')
        self.mod = None
        self.plug = None
        self.name = name
        self.version = version
        self.author = author

        self.funcs = {
            "onLoad": [],
            "onUnload": []}
        self.hooks = {}
        self.cmds = []

        self.printfmt = "Plugin {0}: {1}".format(self.name, "{0}")

    def p(self, msg, *args, **kwargs):
        if not self.log: return
        c = self.printfmt.format(msg.format(args, kwargs, self=self))
        self.log.info(c)

    def callFunc(self, name):
        for i in self.funcs[name]: i()

    # Decorators
    def bind(self, name):
        def hook(func):
            self.funcs[name].append(func)
            return func
        return hook

    def hook(self, name):
        def hook(func):
            self.hooks[name] = func
            return func
        return hook

    def cmd(self, name, **kwargs):
        def hook(func):
            c = Command(func, name, **kwargs)
            self.cmds.append(c)
            return c
        return hook

    def db(self, obj):
        self.api.db.addModel(obj)
        return obj

    # Tools
    def load(self, api, mod, log):
        self.log = log
        self.log.info("Loading plugin %s (v%s by %s)" % (self.name, self.version, self.author))
        self.api = api
        self.mod = mod
        [c.add(self.api) for c in self.cmds]
        for name, func in self.hooks.items():
            self.api.addHook(self, name, func)
        del self.hooks

        self.callFunc("onLoad")

    def unload(self):
        self.log.info("Unloading plugin %s" % self.name)
        self.callFunc("onUnload")
