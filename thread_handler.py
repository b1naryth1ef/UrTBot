import threading, thread
from init import config
from debug import log

THREADS = []

config_maxthreads = config.speed['max-threads']
config_threading = config.speed['threading']

def clearThreads():
	for x,i in enumerate(THREADS):
		del THREADS[x]

def spawnThread(func, source, args):
	global THREADS
	log.debug('Tring to spawn thread from source %s' % source)
	if threading.activeCount() <= config_maxthreads and config_threading != 3:
		var = threading.Thread(name=source, target=func, args=args)
		var.start()
		THREADS.append(var)
	
def garbageCollect(): #Run this when we have an empty server (or during a map change...)
	global THREADS
	alives = 0
	for x,i in enumerate(THREADS):
		if not i.isAlive():
			del THREADS[x]
		else:
			alives += 1
	log.info('Garbage Collected Threads. %s still alive...' % alives)
	if alives > config_maxthreads and config_threading != 3:
		log.error('Wow... way too many threads for our thread limit! Somethings wrong...')
	
		