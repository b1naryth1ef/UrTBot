import threading, thread
from debug import log

def exit():
	log.debug('Exit called')

def fireThread(target, *args, **kwargs):
	#log.debug('Firing thread to %s...' % target)
	t = thread.start_new_thread(target, args, kwargs)
	return t

def get_ident(): return thread.get_ident()