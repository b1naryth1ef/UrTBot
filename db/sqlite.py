from base import DBBase
import sqlite3

class DBPlugin(DBBase):
	def __init__(self):
		print "SQLite DB loaded"
		self.dbconn = None
		self.c = None

	def connect(self, dbinfo):
		self.dbconn = sqlite3.connect(dbinfo['database'])
		self.c = self.dbconn.cursor()

	def disconnect(self):
		# should I close the cursor? does it matter? naw?
		self.dbconn.close()

	def commit(self):
		self.dbconn.commit()

	def rollback(self):
		self.dbconn.rollback()

	def addRow(self, table, values):
		query = '''insert into ''' + table + ''' values ('''
		for i in range(0, len(values)):
			query += '?'
			if (i) != len(values) - 1: query += ','
		query += ')'
		print query, values
		return self.c.execute(query, values).rowcount

	def delRow(self, table, search):
		query = '''delete from ''' + table + ''' where '''
		count = 0
		args = ()
		for key in search.keys():
			args += (search[key],)
			query += key + '=?'
			count += 1
			if count != len(search): query += ' and '
		return self.c.execute(query, args).rowcount

	def getRow(self, table, search):
		query = '''select * from ''' + table + ''' where '''
		count = 0
		args = ()
		for key in search.keys():
			args += (search[key],)
			query += key + '=?'
			count += 1
			if count != len(search): query += ' and '
		print query, args
		rows = self.c.execute(query, args).fetchall()
		return rows

	def getField(self, table, search, field): print ("Not implemented in SQLite yet.. oops!")
	def setField(self, table, search, field, value): print ("Not implemented in SQLite yet.. oops!")

	def addTable(self, table, values):
		query = '''create table ''' + table + ''' ('''
		count = 0
		for key in values.keys():
			query += key  + ' ' + values[key]
			count += 1
			if count != len(values): query += ', '
		query += ")"
		return self.c.execute(query)


	def delTable(self, table):
		return self.c.execute("drop table " + table)

	def getTable(self, table):
		return self.c.execute("select * from " + table).fetchall()

if __name__ == '__main__':
	db = DBPlugin()
	db.connect({'database':'/tmp/fuck'})
	db.addTable('animals', {'gender':'text', 'age':'integer'})
	db.addRow('animals', ('male', 19))
	db.addRow('animals', ('female', 16))
	db.addRow('animals', ('male', 11))
	db.addRow('animals', ('unknown', 99))
	db.commit()
	print db.getTable('animals')
	print db.getRow('animals', {'gender':'male'})
	print "deleting 16 female"
	print db.delRow('animals', {'gender':'female', 'age':12})
	db.commit()
	print db.getTable('animals')
	#db.delTable('animals')
	#print db.getTable('animals')