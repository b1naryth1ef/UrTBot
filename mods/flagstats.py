import time
api = None

_name = "Flag Stats"
_author = "B1naryth1ef"
_version = 0.1



class Timer(object):
	def __init__(self):
		self.startt = 0
		self.endt = 0
		self.status = 0
	
	def start(self): 
		if self.status == 0:
			self.startt = time.time()
			self.status = 1
	def stop(self):
		if self.status == 1: 
			self.endt = time.time()
			self.status = 0
	def value(self): 
		x = self.endt-self.startt
		return '{number:.{digits}f}'.format(number=x, digits=4)
	def reset(self):
		self.startt = 0
		self.endt = 0
		self.status = 0


def eventListener(obj):
	global api
	if redFlag == None:
		redFlag = Timer()
	if blueFlag == None:
		blueFlag = Timer()

	if obj == 'init':
		print "Started"

	elif obj.type == "GAME_FLAGPICKUP":
		print "@PICKUP",
		print obj.data['flagid'], redFlag.status, blueFlag.status
		if obj.data['flagid'] == 1 and redFlag.status == 0: 
			print 'Starting'
			redFlag.start()
		elif obj.data['flagid'] == 2 and blueFlag.status == 0: 
			print 'Starting'
			blueFlag.start()

	elif obj.type == "GAME_FLAGRETURN":
		print '@RETURN'
		if obj.data['flagid'] == 1: redFlag.reset()
		elif obj.data['flagid'] == 2: blueFlag.reset()

	elif obj.type == "GAME_FLAGCAPTURE":
		print '@CAPTURE'
		if obj.data['flagid'] == 1:
			redFlag.stop()
			api.say('%sRed %sFlag captured in %s%s' % (api.RED, api.YELLOW, api.CYAN, redFlag.value()))
			redFlag.reset()
		elif obj.data['flagid'] == 2:
			blueFlag.stop()
			api.say('%sBlue %sFlag captured in %s%s' % (api.BLUE, api.YELLOW, api.CYAN, redFlag.value()))
			blueFlag.reset()
	elif obj.type == "GAME_FLAGRESET":
		print '@RESET'
		if obj.data['flagid'] == 1: redFlag.reset()
		elif obj.data['flagid'] == 2: blueFlag.reset()

def init(A):
	global api
	api = A
	print 'Firing'
	eventListener('init')
	api.addListeners(['GAME_FLAGPICKUP', 'GAME_FLAGDROP', 'GAME_FLAGRETURN', 'GAME_FLAGCAPTURE', 'GAME_FLAGRESET'], eventListener)