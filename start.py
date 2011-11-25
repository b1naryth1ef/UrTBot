from multiprocessing import Process, Queue
import init

pr = 0

def func(inp):
	global pr
	if inp == 'reboot':
		print '@reboot'
		pr.terminate()
		main()

def main():
	global pr
	pr = Process(target=init.Start, args=(func, None))

main()