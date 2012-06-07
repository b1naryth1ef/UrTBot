#!/usr/bin/python
from bot.main import Start
from distutils.version import StrictVersion

_version_ = StrictVersion('0.1')

if __name__ == '__main__':
	print 'Booting UrTBot V%s' % _version_
	Start(_version_)
