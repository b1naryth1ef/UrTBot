import subprocess, time, os, sys
proc = subprocess.Popen('./ioUrbanTerror.app/Contents/MacOS/ioUrbanTerror.ub +set dedicated 2 +exec server.cfg',shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
while True:
    proc.stdin.write('status\n')
    proc_read = proc.stdout.readline()
    if proc_read:
        print proc_read


import time
time.sleep(15)
from pyquake3 import PyQuake3
q = PyQuake3('localhost:27960', rcon_password='Norp73')
q.update()
print 'The name of %s is %s, running map %s with %s player(s).' % (q.get_address(), q.vars['sv_hostname'], q.vars['mapname'], len(q.players))
for player in q.players:
    print '%s with %s frags and a %sms ping' % (player.name, player.frags, player.ping)
q.rcon_update()
for player in q.players:
    print '%s has an address of %s' % (player.name, player.address)
print q.rcon("status")