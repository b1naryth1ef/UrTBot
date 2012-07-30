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
    global User, Penalty, Alias, database
    log.debug('SETUP: DATABASE')
    cfg = config.dbConfig
    database = dbs[cfg['type']](cfg['name'], threadlocals=True, **cfg['args'])
    database.connect()

    class BaseModel(Model):
        class Meta():
            database = database

    class User(BaseModel):
        name = CharField()
        joincount = IntegerField()
        firstjoin = DateTimeField()
        lastjoin = DateTimeField()

    class Penalty(BaseModel):
        user = ForeignKeyField(User)
        admin = ForeignKeyField(User)
        penalty = CharField()
        reason = CharField()
        creation_date = DateTimeField()
        expire_date = DateTimeField()
        active = BooleanField()

    class Alias(BaseModel):
        user = ForeignKeyField(User)
        real = CharField()
        alias = CharField()

    try:
        User.create_table()
        Penalty.create_table()
        Alias.create_table()
    except: pass
    log.debug('SETUP DONE: DATABASE')
    return database, User