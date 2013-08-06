import re
from player import Player

PARSE_SW = {}
PARSE_RE = {}


GENERIC_LINE_A = re.compile(r'^(?P<action>[a-z]+):\s*(?P<data>(?P<cid>[0-9]+)\s(?P<text>.*))$', re.IGNORECASE)

def sw(typ):
    def deco(func):
        PARSE_SW[typ] = func
        return func
    return deco

def getUserInfo(data):
    return dict(re.findall(r'\\([^\\]+)\\([^\\]+)', data))

@sw("say:")
def parseSay(g, inp):
    m = GENERIC_LINE_A.match(inp)
    if not m: g.log.warning("Failed to match say!")
    cid = int(m.group("cid"))
    if g.players[cid] is None: return g.log.warning("Failed to find player in say w/ cid %s" % cid)
    obj = g.api.callHook("PLAYER_SAY_GLOBAL", cid=cid, player=g.players[cid], msg=m.group("text").split(":", 1)[-1].strip())
    g.api.hookChat(obj)

@sw("sayteam:")
def parseSayTeam(g, inp):
    m = GENERIC_LINE_A.match(inp)
    if not m: g.log.warning("Failed to match sayteam!")
    cid = int(m.group("cid"))
    if g.players[cid] is None: return g.log.warning("Failed to find player in sayteam w/ cid %s" % cid)
    obj = g.api.callHook("PLAYER_SAY_TEAM", cid=cid, player=g.players[cid], msg=m.group("text").split(":", 1)[-1].strip())
    g.api.hookChat(obj)

@sw("saytell:")
def parseSayTell(g, inp):
    m = GENERIC_LINE_A.match(inp)
    if not m: g.log.warning("Failed to match saytell!")
    cid = int(m.group("cid"))
    cidb = int(m.group("text").split(" ")[0])
    if g.players[cid] is None or g.players[cidb] is None:
        return g.log.warning("Failed to find player in saytell (cids %s and %s)" % (cid, cidb))
    obj = g.api.callHook("PLAYER_SAY_TELL", cid=cid, cidto=cidb, player=g.players[cid], playerto=g.players[cidb], msg=m.group("text").split(":", 1)[-1].strip())
    g.api.hookChat(obj)

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
    g.players[cid].handleUserInfo(data)
    g.api.callHook("PLAYER_CUI", cid=cid, player=g.players[cid], data=data)

@sw("ClientUserinfoChanged:")
def parseClientUserInfoChanged(g, inp):
    _, cid, data = inp.split(" ", 2)
    cid = int(cid)
    data = getUserInfo(data)
    if g.players[cid] is None:
        return g.log.warning("Failed to find player in CUI changed: %s" % cid)
    g.players[cid].handleUserInfoChanged(data)
    g.api.callHook("PLAYER_CUI_CHANGE", cid=cid, player=g.players[cid], data=data)


