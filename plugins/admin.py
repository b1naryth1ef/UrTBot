from bot.api import Plugin
from bot.database import BaseModel, User, UserInfo
from peewee import *

p = Plugin("Test Plugin")

@p.db
class Greeting(BaseModel):
    user = ForeignKeyField(User)
    msg = CharField()

    def getGreeting(self, player):
        q = Greeting.select().where(Greeting.user == player.user)
        if q.count():
            return q[0].msg

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

@p.cmd("find", need_args=2)
def commandTest(c, obj):
    """{prefix}{cmd} <field> <value>"""
    format = None

    if obj.args[0] == "ip":
        q = (UserInfo.ip ** obj.args[1])
        format = "Match: User {entry.user.authname} | {entry.ip} == %s" % obj.args[1]
    elif obj.args[0] == "name":
        q = (UserInfo.name ** obj.args[1])
        format = "Match: User {entry.user.authname} | {entry.name} == %s" % obj.args[1]
    else:
        return obj.reply("No such field %s" % obj.args[0])

    q = UserInfo.select().where(q)
    if not q.count():
        return obj.reply("No results!")

    if q.count() > 25:
        return obj.reply("Over 25 results; not displaying.")

    # Print the results
    obj.api.q3.long("tell %s [{num}] {msg}" % obj.player.cid, [format.format(entry=i) for i in q])
