from peewee import *

dbs = {
    'sqlite': SqliteDatabase,
    'mysql': MySQLDatabase,
}

def load(cfg):
    database = dbs[cfg.database['type']](cfg.database['name'], threadlocals=True, **cfg.database['args'])
