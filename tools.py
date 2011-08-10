def error(code,err):
	if code == "0":
		print "CRITICAL: "+err
	elif code == "1":
		print "ERROR: "+err
