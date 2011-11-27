botConfig = {
	'prefix': "^1[^2BOT^1]:",
	'rcon': "MyPassword123",
	'rconip': "localhost:27960",
	'servercommand': "~/UrbanTerror/ioUrTded.i386 +set dedicated 2 +exec server.cfg" ,
	'serversocket': "/tmp/quake3_27961",
	'plugins':[],
	'groups':{
		'unsub':0,
		'user':1,
		'member':2,
		'mod':3,
		'admin':4,
		'uberadmin':5
	}	
}

##################################
### Database config
###		Pick one, delete the rest
###		'python database.py' will create 
###		the database and setup the tables. Doit.	
##################################

#dbConfig = { #Default for MySQL [NOT IMPLEMENTED]
#	'database_type': "mysql",
#	'server': 'localhost',
#	'user': 'root',
#	'password': '',
#	'database': 'urtbot',
#	'prefix': '',
#}

dbConfig = { #Default for SQLite
	'database_type': "sqlite",
	'server': '',
	'user': '',
	'password': '',
	'database': '/tmp/urtbot.db',
	'prefix': '',
}

#Security Levels:
#- Method 1: User must match GUID/IP/NICK to be auto-logged in
#- Method 2: User must match GUID/IP, GUID/NICK to be auto-logged in...
#- Method 3: User must match GUID/IP, GUID/NICK or IP/NICK to be auto-logged in
#- Method 4: User must match NICK to be logged in...

securityConfig = {
	'level': 2,
	'multi': False,
}

# Urban Terror config --
# YOU MOST LIKELY DO NOT NEED TO TOUCH THIS!
UrTConfig = {
    # Maps that don't have their own PK3
    'maps' : [ 'ut4_abbey','ut4_abbeyctf','ut4_algiers','ut4_ambush',
    'ut4_austria','ut4_casa','ut4_company','ut4_crossing','ut4_docks',
    'ut4_dressingroom','ut4_eagle','ut4_elgin','ut4_firingrange',
    'ut4_harbortown','ut4_herring','ut4_horror','ut4_kingdom','ut4_mandolin',
    'ut4_maya','ut4_oildepot','ut4_prague','ut4_ramelle','ut4_ricochet',
    'ut4_riyadh','ut4_sanc','ut4_snoppis','ut4_suburbs','ut4_subway',
    'ut4_swim','ut4_thingley','ut4_tombs','ut4_toxic','ut4_tunis',
    'ut4_turnpike','ut4_uptown' ],
    # PK3s that aren't actually maps
    'ignoremaps' : [ 'zpak000', 'zpak000_assets', 'zpak001_assets',
                        'pak0^7', 'common-spog']
}

