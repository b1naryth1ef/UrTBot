import threading, thread
from init import config
from debug import log

#0: low
#1: norm
#2: high
#3: insane

SOURCES = { #This table shows what actions should fire threads. You could mess around with it if you understand more...
    'module_init':0,
    'parse_userkicked':0,
    'parse_initgame':2,
    'update_clientinfo':2,
    'parse_action_small':2,
}


THREADS = []

def init():
	config_maxthreads = config.speed['max-threads']
	config_threading = config.speed['threading']

	if config_threading == 3: config_maxthreads = 500 #Yep! Its ridiculous!

def fire(source, func, args, timeout=0):
    f = {}
    global config_threading
    if SOURCES[source] <= config_threading:
        spawnThread(func, source, args, timeout)
    else:
        func(*args)

def clearThreads():
    for x, i in enumerate(THREADS):
        del THREADS[x]

def spawnThread(func, source, args, timeout):
    global THREADS
    log.debug('Tring to spawn thread from source %s' % source)
    if threading.activeCount() <= config_maxthreads:
        var = threading.Thread(name=source, target=func, args=args)
        var.start()
        if timeout > 0: var.join(timeout)
        THREADS.append(var)
    
def garbageCollect(): #Run this when we have an empty server (or during a map change...)
    global THREADS
    alives = 0
    for x, i in enumerate(THREADS):
        if not i.isAlive(): del THREADS[x]
        else: alives += 1
    log.info('Garbage Collected Threads. %s still alive...' % alives)
    if alives > config_maxthreads:
        log.error('Wow... way too many threads for our thread limit! Somethings wrong...')
    