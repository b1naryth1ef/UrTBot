""" rcon.py
Provides a RCON class to communicate with a Q3 server.
Good-ish performance based on automatically retrying the command if a reply
isn't received within a short time. Should be able to spam commands at this
puppy and not worry about any getting dropped or taking forever to send
them out.

$ python rcon.py
elapsed time to send 100 cmds was 52 secs
$ python rcon.py
elapsed time to send 10 cmds was 4 secs
"""

import socket
import time
import thread
import re

split = lambda s, l: [s[i:i+l] for i in range(0, len(s), l)]


class RCON():
    def __init__(self, server='localhost', password='password', port=27960):
        """
        The main RCON class for interacting with servers.
        server (str): The server, default is localhost
        password (str): The rconpassword, default is password
        port (int): The server port, default is 27960
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if ':' in server: self.server, self.port = server.split(":")
        else: self.server, self.port = server, port
        self.port = int(self.port)
        self.password = password
        self.last_cmd = None
        self.retries = 3  # default number of retries
        self.throttle_time = 0.0  # secs to wait between retries
        self.lock = thread.allocate_lock()

        self.socket.connect((self.server, self.port))
        self.socket.settimeout(0.75)

    def send(self, data):
        self.socket.send('\xFF\xFF\xFF\xFF' + str(data))

    def recv(self):
        data = None
        try: data = self.socket.recv(4096)
        except socket.timeout: pass
        return data

    def cmd(self, cmd):
        self.last_cmd = cmd
        retries = self.retries
        data = None

        while retries > 0 and data is None:
            self.send(cmd)
            data = self.recv()
            if data is None:
                time.sleep(self.throttle_time)
            retries -= 1

        return data[4:] if data is not None else data

    def getCvar(self, name):
        """
        Get an rcon cvar, by name
        """
        res = re.findall('print\\n".*?" is:"(.*?)\^7"', self.rcon(name))
        if len(res):
            res = res[0]
            if res.isdigit(): res = int(res)
            return res

    def rcon(self, cmd):
        """
        Send an rcon command, cmd
        """
        self.lock.acquire(1)
        reply = self.cmd('rcon "%s" %s' % (self.password, cmd))
        self.lock.release()
        return reply

if __name__ == '__main__':
    rcon = RCON()
    start = time.time()
    for i in range(0, 10): rcon.rcon("say I am counting... %d" % i)
    print "elapsed time to send %d cmds was %d secs" % (count, (time.time() - start))
