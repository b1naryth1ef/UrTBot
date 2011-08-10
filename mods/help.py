#Help Module
import api

def helpy(A):
	A.say("!Help list:")
	print "At help!"
def killy(A):
	li = A.plist()
	for i in li:
		if A.a.kil in i.name:
			uid = i.uid
	if A.a.atk != A.a.kil:
		A.tell(uid,"YOU DUN GET KILLED BY: "+A.a.atk)
h = api.Mod("HelpMod","0.0.1")
h.cmdreg('!help',helpy)
h.hookreg('kill',killy)