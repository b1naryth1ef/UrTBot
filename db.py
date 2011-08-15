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
    def __init__(self, userid, name=None, first_name=None, last_name=None,checkins=None):
        self.id = userid
        self.name = name
        self.first_name = ips
        self.last_name = last_ip
        self.checkins = checkins

