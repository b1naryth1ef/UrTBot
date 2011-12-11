from init import A
import database

""" db example assuming the db is already created (see init()):
	
	import database
	
	db = database.DB()
	db.tableSelect("my_table", "key") # optionally just db.tableSelect("my_table") for key = "id"
	
	myrow = db.rowFind("value") # get the first row with column "key"="value"
	myrow["column"] = "dildo" # set column w/ name "column" to value "dildo"
	myrow["size"] = "xxl"
	(etc etc, myrow is just a dict w/ column names as keys)
	db.rowUpdate(myrow) # update this row in the DB -- might* not be committed yet
	db.rowUpdate(myotherrow) # pretend with me..
	db.rowUpdate(myotherotherrow) # :D
	db.commit()
	
	* there are different modes the db can run in, I think the default one might commit atomically
	  with the row update. Not great for performance but then you don't have to commit().
	  Just commit() to be ready for changing the db mode, ok!? Ok!
	  
	  rowFindAll() returns a list of all rows that match
"""

def parseKill(obj): pass
	#A.B.Clients[obj.atk]
	atk = A.getClient(obj.atk)
	atkClient = db.rowFind(atk.cid) #<<< see player.py for note on what cid should be
	atkClient["kills"] += 1
	db.rowUpdate(atkClient)
	db.commit()

def parseDeath(obj):
	vic = A.getClient[obj.vic]
	vicClient = db.rowFind(vic.cid)
	vicClient["deaths"] += 1
	db.rowUpdate(vicClient)
	db.commit()

def parseSuicide(obj): pass
def parseTeamKill(obj): pass

def eventHandler(obj):
	if obj.type == 'CLIENT_KILL': parseKill(obj)
	elif obj.type == 'CLIENT_SUICIDE': parseSuicide(obj)
	elif obj.type == 'CLIENT_GENERICDEATH': parseDeath(obj)
	elif obj.type == 'CLIENT_WORLDDEATH': parseDeath(obj)
	elif obj.type == 'CLIENT_SUICIDE': parseDeath(obj)
	elif obj.type == 'CLIENT_TEAMKILL': parseTeamKill(obj)

def init():
	global db
	db = database.DB()
	if db.tableExists('stats_main') == False:
		db.tableCreate('stats_main', {'id':'integer', 'kills':'integer', 'deaths':'integer', 'tks':'integer', 'suicides':'integer', 'score':'integer'}) #<<< make int/str map too correct Sqlite shit
	 db.tableSelect('stats_main')
		
	A.addlisteners(['CLIENT_KILL', 'CLIENT_SUICIDE', 'CLIENT_GENERICDEATH', 'CLIENT_WORLDDEATH', 'CLIENT_SUICIDE', 'CLIENT_TEAMKILL'])
	
def die(): pass