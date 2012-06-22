import threading, thread
from debug import log

def exit():
	log.debug('Exit called')
	#for thr in threads:
	#	thr._Thread__stop()

def fireThread(target, *args, **kwargs):
	log.debug('Firing thread to %s...' % target)
	t = thread.start_new_thread(target, args, kwargs)
	#t = threading.Thread(target=target, args=args, kwargs=kwargs)
	#t.start()
	return t

def fireTimer(target, delay, *args, **kwargs):
	t = threading.Timer(delay, target, args=args, kwargs=kwargs)
	t.start()
	return t
