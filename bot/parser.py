import re
from player import Player

PARSE_SW = {}
PARSE_RE = {}

def sw(typ):
    def deco(func):
        PARSE_SW[typ] = func
        return func
    return deco

def getUserInfo(data):
    return dict(re.findall(r'\\([^\\]+)\\([^\\]+)', data))

@sw("say:")
def parseSay(g, inp):
    _, data = inp.split("say: ")
    cid, msg = data.split(" ", 1)
    if g.players[int(cid)] is None:
        return g.log.warning("Got SAY but we don't have a player @ CID: %s" % int(cid))
    g.api.callHook("PLAYER_SAY", cid=int(cid), player=g.players[int(cid)], msg=msg)

@sw("sayteam:")
def parseSayTeam(g, inp): pass

@sw("saytell:")
def parseSayTell(g, inp): pass

@sw("ClientConnect:")
def parseClientConnect(g, inp):
    cid = int(inp.split(' ')[-1])
    g.players[cid] = None
    g.api.callHook("PLAYER_CONNECT", cid=cid)

@sw("ClientUserinfo:")
def parseClientUserInfo(g, inp):
    a = inp.split(' ')[1:]
    cid = int(a[0])
    data = getUserInfo(a[1])
    if g.players[cid] is None or g.players[cid].name != data['name']:
        g.players[cid] = Player(cid, g, data)
        g.players[cid].init()
        return g.api.callHook("PLAYER_LOADED", cid=cid, player=g.players[cid], data=data)
    g.api.callHook("PLAYER_CUI_CHANGE", cid=cid, player=g.players[cid], data=data)
