from bot.config_handler import ConfigFile
from bot.main import BOT
from bot.api import listener, Event, command
import sys, os, time

events = {
    'ban':Event('PLUGIN_ADMIN_BAN'),
    'kick':Event('PLUGIN_ADMIN_KICK')
}

@command('kick')
def testCommand(obj):
    log.debug('ADMIN:KICK>> %s' % obj)

def init(B, A): pass
def run(): pass