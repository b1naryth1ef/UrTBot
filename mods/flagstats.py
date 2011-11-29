import time
from init import A

_name = "Flagstats"

redFlag = None
blueFlag = None

class Timer(object): #@CREDIT B1
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
		return '{number:.{digits}f}'.format(number=x, digits=2)
	def reset(self):
		self.startt = 0
		self.endt = 0
		self.status = 0

def eventListener(obj):
	"""
	The making of this plugin was hell. 
	Fuck the iourt team for the stupid
	decisions in the way flag capping is
	handled. Die in a cold, dark, horrible
	place.
	-B1
	"""
	global A, redFlag, blueFlag
	if redFlag == None: redFlag = Timer()
	if blueFlag == None: blueFlag = Timer()

	elif obj.type == "GAME_FLAGPICKUP":
		print obj.data['flagid'], redFlag.status, blueFlag.status
		if obj.data['flagid'] == 1 and redFlag.status == 0: redFlag.start()
		elif obj.data['flagid'] == 2 and blueFlag.status == 0: blueFlag.start()

	elif obj.type == "GAME_FLAGRETURN":
		if obj.data['flagid'] == 1: redFlag.reset()
		elif obj.data['flagid'] == 2: blueFlag.reset()

	elif obj.type == "GAME_FLAGCAPTURE":
		if obj.data['flagid'] == 2:
			redFlag.stop()
			A.say('%sRed %sFlag captured in %s%s seconds' % (A.RED, A.YELLOW, A.CYAN, redFlag.value()))
			redFlag.reset()
		elif obj.data['flagid'] == 1:
			blueFlag.stop()
			A.say('%sBlue %sFlag captured in %s%s seconds' % (A.BLUE, A.YELLOW, A.CYAN, blueFlag.value()))
			blueFlag.reset()
	elif obj.type == "GAME_FLAGRESET":
		if obj.data['flagid'] == 1: redFlag.reset()
		elif obj.data['flagid'] == 2: blueFlag.reset()

def init(): A.addListeners(['GAME_FLAGPICKUP', 'GAME_FLAGDROP', 'GAME_FLAGRETURN', 'GAME_FLAGCAPTURE', 'GAME_FLAGRESET'], eventListener)