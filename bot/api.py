# -*- coding: utf-8 -*-
import os, sys, re

class FiredEvent(object):
    def __init__(self, api, name, data={}):
        self._name = name
        self._data = data
        self._api = api
        self.__dict__.update(data)

        self._cancel = False

    def cancel(self): self._cancel = True

class API(object):
    def __init__(self, bot, log):
        self.bot = bot
        self.log = log
        self.hooks = {}
        self.plugins = {}

    def callHook(self, name, **data):
        self.log.debug("Calling hook '%s' w/ '%s'" % (name, data))
        if name in self.hooks:
            obj = FiredEvent(self, name, data)
            [i(obj) for i in self.hooks[name]]

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

    # Tools
    def load(self, api, mod, log):
        self.log = log
        self.log.info("Loading plugin %s (v%s by %s)" % (self.name, self.version, self.author))
        self.api = api
        self.mod = mod
        for name, func in self.hooks.items():
            self.api.addHook(self, name, func)
        del self.hooks

        self.callFunc("onLoad")

    def unload(self):
        self.log.info("Unloading plugin %s" % self.name)
        self.callFunc("onUnload")
