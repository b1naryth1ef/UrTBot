from main import Api
import main
a = Api()


def x(obj):
	a.say("Hiya "+obj.sender+"!")
x_events = {}
x_commands = {"!help":x}


def k(obj):
	a.say("U DUN GET KILLED!")
k_events = {"kill":k}
k_commands = {}

_funcs = ("x","k")