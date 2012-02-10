#!/usr/bin/python
import init
from distutils.version import StrictVersion as V

_version_ = V('0.1')

if __name__ == '__main__':
	print 'Booting UrTBot V%s' % _version_
	init.Start()
