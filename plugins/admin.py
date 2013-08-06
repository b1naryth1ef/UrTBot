from bot.api import Plugin

p = Plugin("Test Plugin")

@p.hook("PLAYER_SAY")
def playerSay(obj):
    print "%s said %s" % (obj.player.name, obj.msg)

@p.hook("PLAYER_CONNECT")
def playerConnect(obj):
    print "%s connected!" % obj.cid

@p.hook("PLAYER_LOADED")
def playerLoaded(obj):
    print "%s loaded!" % obj.player.name

@p.bind("onLoad")
def onLoad():
    print "Plugin loaded!"

@p.cmd("test")
def commandTest(c, obj):
    obj.reply("This is a test!")
