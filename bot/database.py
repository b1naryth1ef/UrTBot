from peewee import *
from datetime import datetime
import sys, os, time

dbs = {
    'sqlite':SqliteDatabase,
    'mysql':MySQLDatabase,
}

database = None
config = None
log = None

def setup(config, log):
    global User, Ban, database
    log.debug('SETUP: DATABASE')
    cfg = config.dbConfig
    database = dbs[cfg['type']](cfg['name'], threadlocals=True, **cfg['args'])
    database.connect()

    class BaseModel(Model):
        class Meta():
            database = database

    class User(BaseModel):
        name = CharField()
        guid = CharField()
        ip = CharField()
        group = IntegerField()
        password = CharField()
        joincount = IntegerField()
        firstjoin = DateTimeField()
        lastjoin = DateTimeField()

    class Ban(BaseModel):
        uid = IntegerField() #Bannie
        by = ForeignKeyField(User) #Banner
        reason = CharField() #Ban reason
        created = DateTimeField() #Ban start
        until = DateTimeField() #Ban end
        active = BooleanField()

    try:
        User.create_table()
        Ban.create_table()
    except: pass
    log.debug('SETUP DONE: DATABASE')
    return database, User