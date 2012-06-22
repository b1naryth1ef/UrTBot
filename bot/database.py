from peewee import *
from datetime import datetime
import sys, os, time

dbs = {
    'sqlite':SqliteDatabase,
}

database = None
config = None
log = None

#name=None, guid=None, ip=None, group=0, password='', joincount=0, firstjoin=None, lastjoin=None
class User(Model):
    name = CharField()
    guid = CharField()
    ip = CharField()
    group = IntegerField()
    password = CharField()
    joincount = IntegerField()
    firstjoin = DateTimeField()
    lastjoin = DateTimeField()

class Ban(Model):
    uid = IntegerField() #Bannie
    by = ForeignKeyField(User) #Banner
    reason = CharField() #Ban reason
    created = DateTimeField() #Ban start
    until = DateTimeField() #Ban end
    active = BooleanField()

def setup(config, log):
    global database
    log.debug('SETUP: DATABASE')
    cfg = config.dbConfig
    database = dbs[cfg['type']](cfg['database'], threadlocals=True)
    database.connect()
    try:
        User.create_table()
        Ban.create_table()
    except: pass
    log.debug('SETUP DONE: DATABASE')
    return database, User