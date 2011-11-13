botConfig = {
	'prefix': "^1[^2BOT^1]:",
	'rcon': "MyPassword123",
	'rconip': "localhost:27960",
	'servercommand': "~/UrbanTerror/ioUrTded.i386 +set dedicated 2 +exec server.cfg" ,
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

dbConfig = { #Default for MySQL
	'database_type': "mysql",
	'server': 'localhost',
	'user': 'root',
	'password': '',
	'database': 'urtbot',
}