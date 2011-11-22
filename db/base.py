class User(object):
    """A simple User class"""
    def __init__(self, userid, nick=None, group=None, ips=None, last_ip=None, guid=None, password=None, data=None):
        self.id = userid
        self.nick = nick
        self.group = group
        self.ips = ips
        self.last_ip = last_ip
        self.guid = guid
        self.password = password
        self.data = data
