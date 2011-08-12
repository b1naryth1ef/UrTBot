from main import Api
a = Api()


def x(obj):
	a.say("Hiya "+obj.sender+"!")

def k(obj):
	a.say("U DUN GET KILLED!")
a.register("command",("!test",x))
a.register("event",("kill",k))