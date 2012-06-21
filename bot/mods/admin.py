from bot.config_handler import ConfigFile
from bot.main import BOT
from bot.api import listener, Event, command
from bot.debug import log
import sys, os, time

events = {
    'ban':Event('PLUGIN_ADMIN_BAN'),
    'kick':Event('PLUGIN_ADMIN_KICK')
}

@command('kick')
def testCommand(obj):
    if len(obj['msg'].split(' ')) in [2, 3]: pass
    else:
        client.tell('^1Usage: !kick <cid/name> [reason]')
    #{'msg': '!kick', 'client': <bot.player.Player instance at 0x9f5062c>, 'name': '`SoC-B1nzy'}

def init(B, A): pass
def run(): pass