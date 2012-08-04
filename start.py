#!/usr/bin/python
from bot.main import Start
import sys, os, time

_version_ = "0.4dev"
_author_ = "B1naryth1ef"

if __name__ == '__main__':
	print 'Booting UrTBot V%s' % _version_
	if len(sys.argv) == 2: config = sys.argv[1]
	else: config = "config.cfg"
	Start(_version_, config)
