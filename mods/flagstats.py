
api = None

def eventListener(obj):
	print "[][][][][][][][]"
	if obj == 'init':
		pass #setup stuff
	elif obj.type == "GAME_FLAGPICKUP":
		print obj.data['item'], obj.data['team']
	elif obj.type == "GAME_FLAGDROP":
		print obj.data['flag'], obj.data['flagid']
	elif obj.type == "GAME_FLAGRETURN":
		print obj.data['flag'], obj.data['flagid']
	elif obj.type == "GAME_FLAGCAPTURE":
		print obj.data['flag'], obj.data['flagid']

def init(A):
	global api
	api = A
	api.addListeners(['GAME_FLAGPICKUP', 'GAME_FLAGDROP', 'GAME_FLAGRETURN', 'GAME_FLAGCAPTURE'], eventListener)