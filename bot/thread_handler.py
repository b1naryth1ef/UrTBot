import threading, thread
from main import log

threads = []
gcthread = None

def exit():
	for thr in threads:
		thr._Thread__stop()

def fireThread(target, *args, **kwargs):
	t = threading.Thread(target=target, args=args, kwargs=kwargs)
	t.start()
	threads.append(t)
	return t

def fireTimer(target, delay, *args, **kwargs):
	t = threading.Timer(delay, target, args=args, kwargs=kwargs)
	t.start()
	threads.append(t)
	return t

def fireGC():
	gcthread = fireTimer(garbageCollect, 500)

def garbageCollect():
	for pos, thr in enumerate(threads):
		if not thr.isAlive():
			del thr
	log.debug('Thread GC ran. Currently %s threads running.' % len(threads))
	return fireGC()