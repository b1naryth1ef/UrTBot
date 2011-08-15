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

