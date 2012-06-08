from bot.main import BOT
from bot.api import listener, Event, command
import sys, os, time

testEvent = Event('PLUGIN_TEST_TESTEVENT')

@listener('PLUGIN_TEST_TESTEVENT')
def testListener(obj): pass

@command('test')
def testCommand(obj):
	print 'BOOYAH!'
	BOT.A.say('^1it works!')

def init(B, A):
	BOT.A.say('Testing...')

def run():
	time.sleep(5)
	testEvent.fire()
