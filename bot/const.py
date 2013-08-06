

MOTTOS = [
    "Locked and Loaded!",
    "Because B3 is shit...",
    "Built off the tears of unicorns",
    "Because YoLo/"
]

GAMETYPES = {
    0: "ffa",
    1: "ftl",
    3: "tdm",
    4: "ts",
    5: "ftl",
    6: "cah",
    7: "ctf",
    8: "bomb",
    9: "jump",
    10: "gungame"
}

IGNORES = ['^1Error: weapon number out of range']

COLORS = {
   "BLACK": 0,
   "RED": 1,
   "GREEN": 2,
   "YELLOW": 3,
   "BLUE": 4,
   "CYAN": 5,
   "MAGENTA": 6,
   "WHITE": 7,
   "ORANGE": 8,
   "OLIVE": 9
}

COLOR_FORMAT = dict([("C_%s" % k.upper(), "^%s" % v) for k, v in COLORS.items()])

def C(msg, **kwargs):
    kwargs.update(COLOR_FORMAT)
    return msg.format(msg, **kwargs)
