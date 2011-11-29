from init import A

def testr(obj):
	A.say('TESTING 1... 2... 3...')
	print "Testing!"

A.addCmd('!t', testr, ':D', 0)

