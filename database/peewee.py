import sys, os, time
from peewee import *
from datetime import datetime

dbs = {
	'sqlite':SqliteDatabase,
}

database = None
config = None
log = None

#name=None, guid=None, ip=None, group=0, password='', joincount=0, firstjoin=None, lastjoin=None
class User():
	name = CharField()
	guid = CharField()
	ip = CharField()
	group = IntegerField()
	password = CharField()
	joincount = IntegerField()
	firstjoin = DateField()
	lastjoin = DateField()

def init(config, log):
	global database, config, log
	cfg = config.dbConfig
	database = dbs[cfg['connecter']](cfg['database'], threadlocals=True)
	database.connect()
	try:
		User.create_table()
	except: pass
	return database, User