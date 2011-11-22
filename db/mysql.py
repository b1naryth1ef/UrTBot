"""
This is the default database plugin for 
UrTBot
"""

import MySQLdb

user = 'root'
passwd = ''
server = 'localhost'
db = 'test'
table = ''

#Initiate curser
db = MySQLdb.connect(user=user, passwd=passwd, host=server, db=db)
c = db.cursor()

class User(object):
    """A simple User class"""
    def __init__(self, userid, name=None, ips=None, last_ip=None,guid=None):
        self.id = userid
        self.name = name
        self.ips=ips
        self.last_ip = last_ip
        self.guid = guid


def clientAdd(): pass
def clientDel(): pass
def clientModify(): pass
def clientSearch(nick=None, guid=None, ip=None): pass
def clientSelect(): pass

def aliasAdd(): pass
def aliasDel(): pass
def aliasSearch(): pass
def aliasSelect(): pass

def penaltyAdd(): pass
def penaltyDel(): pass
def penaltyModify(): pass
def penaltySearch(): pass
def penaltySelect(): pass

def defaultTableSet():
	c.execute(""" 
DROP TABLE IF EXISTS `penalties`;

CREATE TABLE `penalties` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `userid` int(11) DEFAULT NULL,
  `adminid` int(11) DEFAULT NULL,
  `type` varchar(265) DEFAULT '',
  `reason` varchar(265) DEFAULT '',
  `time` int(11) DEFAULT NULL,
  `time_expire` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `group` int(2) DEFAULT NULL,
  `nick` varchar(32) NOT NULL DEFAULT '',
  `guid` varchar(32) NOT NULL DEFAULT '',
  `password` int(6) DEFAULT NULL,
  `data` longtext,
  `ip` varchar(16) DEFAULT '',
  `lastip` varchar(16) DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1; 
""")