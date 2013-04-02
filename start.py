from bot.config import ConfigFile
from bot.rcon import RCON
from bot.bot import Bot
from bot.debug import loadLog
from wrapper import GameOutput

import os

default_config = {
    "usockname": "urtbot1",
    "rcon": {
        "host": 'localhost',
        "pass": '',
        "port": 27960
    },
    "devCfg": {
        "loglevel": "info",
        "logfile": "debug.log",
        "uselog": True
    }
}


def load():
    if not os.path.exists("config"): os.mkdir("config")
    config = ConfigFile("config.cfg", path=['config'], default=default_config)
    rcon = RCON(server=config.rcon['host'], password=config.rcon['pass'], port=config.rcon['port'])
    inter = GameOutput()
    log = loadLog(config)
    return config, rcon, inter, log

if __name__ == "__main__":
    config, rcon, inter, log = load()
    bot = Bot(config, rcon, inter, log)
    bot.run()
