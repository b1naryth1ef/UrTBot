import sys
import time
from config import dbConfig

__import__('db.' + dbConfig['database_type'])
db_plugin = sys.modules['db.' + dbConfig['database_type']]

class DB(db_plugin.DBPlugin):
	def __init__(self):
		db_plugin.DBPlugin.__init__(self)
		self.connect(dbConfig)
		self.table = None
		self.tablekey = None
		self.cols = {}
		self.colsOrder = []

	def tableCreate(self, table, values):
		return self.addTable(table, values)
	def tableDelete(self, table):
		return self.delTable(table)
	def tableExists(self, table):
		return self.checkTable(table)

	def tableSelect(self, table, key="id"):
		self.table = table
		self.tablekey = key
		self.colsOrder = []

		cols = self.getColumns(table)
		value = None
		for field in cols:
			if field[1] == 'id': pass # leave as none for autoid
			elif field[2] == 'text': value = ""
			elif field[2] == 'integer': value = 0
			else: print "[WARNING] sqlite column of neither integer nor text. Not yet supported!"
			self.cols[field[1]] = value
			self.colsOrder.append(field[1])

	def rowToDict(self, row):
		""" Helper function for the class """
		rowDict = self.cols.copy()
		i = 0
		for column in self.colsOrder:
			rowDict[column] = row[i]
			i += 1 # Not very pythonish :D Alternatives?!
		return rowDict

	def rowCreate(self, row):
		return self.addRow(self.table, row)

	def rowFind(self, search, key=None):
		if key == None: key = self.tablekey
		result = self.getRow(self.table, {key:search})
		if len(result) == 0: return None
		return self.rowToDict(result[0])

	def rowFindAll(self, search=None, key=None):
		if key == None: key = self.tablekey
		if search == None: result = self.getTable(self.table)
		else: result = self.getRow(self.table, {key:search})
		if len(result) == 0: return None
		rows = []
		for row in result:
			rows.append(self.rowToDict(row))
		return rows

	def rowUpdate(self, row):
		# This could be improved by a dbplugin method to update multiple fields at once... doh :D
		for field in row:
			if field == self.tablekey: continue
			self.setField(self.table, {self.tablekey:row[self.tablekey]}, field, row[field])
		if self.tablekey in row:
			# Not sure why we'd do this, but hey... 
			self.setField(self.table, {self.tablekey:row[self.tablekey]}, self.tablekey, row[self.tablekey])

	def rowBlank(self):
		return self.cols.copy()

	def defaultTableSet(self):
		if self.tableExists("penalties") == True: print "Table 'penalties' already exists."
		else:
			print 'Adding penalties'
			self.tableCreate('penalties', {'id':'integer primary key', 'userid':'integer',
			'adminid':'integer', 'type':'text', 'reason':'text', 'time':'text', 'expiration':'text', 'status':'integer'})
		self.commit()

if __name__ == '__main__':
	db = DB()		
	print "Making default tables..."
	try:
		db.defaultTableSet()
	except Exception, e:
		print "Ruh roh! Failed because %s." % e
		sys.exit()
	print "All done!"

	print "Now for some tests..."
	db.tableSelect("clients", "guid")
	result = db.rowFind("THISISNOTAREALGUIDOMGTHISISCOOLZ")
	print result
	result["cgroup"] = 4
	db.rowUpdate(result)
	# If this were real, we'd db.commit() after doing a rowUpdate()
	result = db.rowFind("THISISNOTAREALGUIDOMGTHISISCOOLZ")
	print result

	print "#######################################"
	print "#######################################"
	result = db.rowFindAll()
	print result