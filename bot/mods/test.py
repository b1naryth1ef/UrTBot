from bot.main import BOT
from bot.api import listener, Event, command
import sys, os, time

testEvent = Event('PLUGIN_TEST_TESTEVENT')

@listener('PLUGIN_TEST_TESTEVENT')
def testListener(obj): pass

@command('test')
def testCommand(obj):
	BOT.Q3.say('^1Testing command works!')

def init(B, A): pass
def run(): pass
