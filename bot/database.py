from peewee import *
from datetime import datetime

dbs = {
    'sqlite': SqliteDatabase,
    'mysql': MySQLDatabase,
}

class BaseModel(Model):
    class Meta: pass

class DatabaseManager(object):
    def __init__(self, cfg, log):
        self.log = log
        self.config = cfg
        self.database = dbs[cfg.database['type']](cfg.database['name'], threadlocals=True, **cfg.database['args'])
        self.track = cfg.settings['trackplayers']

        self.models = {}

        self.connect()

        for model in DEFAULT_MODELS:
            self.addModel(model)

    def addModel(self, x):
        x.Meta = self.buildMeta()
        self.models[x.__name__] = x
        x.create_table(True)

    def buildMeta(self):
        class _Meta_:
            database = self.database
        return _Meta_

    def connect(self):
        self.log.info("Connecting to database of type %s" % (self.config.database['type']))
        self.database.connect()
        self.log.info("Connected to database!")

class UserData(BaseModel):
    user = ForeignKeyField("User")

    count = IntegerField(default=1)
    name = CharField()
    ip = CharField()


class User(BaseModel):
    authname = CharField()

    timeplayed = IntegerField(default=0)
    connections = IntegerField(default=0)
    last_connect = DateTimeField(default=datetime.now)
    created = DateTimeField(default=datetime.now)


DEFAULT_MODELS = [User]
