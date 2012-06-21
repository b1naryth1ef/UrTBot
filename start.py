#!/usr/bin/python
from bot.main import Start
from distutils.version import StrictVersion
import sys, os, time

_version_ = StrictVersion('0.1')

if __name__ == '__main__':
	print 'Booting UrTBot V%s' % _version_
	config = "config.cfg"
	if len(sys.argv) == 2:
		config = sys.argv[1]

	Start(_version_, config)
