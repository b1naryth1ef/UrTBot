def error(code,err):
	if code == "0":
		print "CRITICAL: "+err
	elif code == "1":
		print "ERROR: "+err
	elif code == "00":
		print "MOD CRITICAL: "+err
	elif code == "01":
		print "MOD ERROR: "+err