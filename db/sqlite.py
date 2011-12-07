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
		query = '''insert into ''' + table + " ("
		args = ()
		strargs = ''
		count = 0
		for key in values.keys():
			args += (values[key],)
			strargs += '?'
			query += key
			count += 1
			if count != len(values):
				query += ','
				strargs += ','
		query += ") values (" + strargs + ")"
		return self.c.execute(query, args).rowcount

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
		rows = self.c.execute(query, args).fetchall()
		return rows

	def getField(self, table, search, field):
		query = '''select ''' + field + ''' from ''' + table + ''' where '''
		args = ()
		count = 0
		for key in search.keys():
			args += (search[key],)
			query += key + '=?'
			count += 1
			if count != len(search): query += ' and '
		return self.c.execute(query, args).fetchall()

	def setField(self, table, search, field, value):
		query = '''update ''' + table + ''' set ''' + field + '''=? where '''
		args = (value,)
		count = 0
		for key in search.keys():
			args += (search[key],)
			query += key + '=?'
			count += 1
			if count != len(search): query += ' and '
		return self.c.execute(query, args).rowcount

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
	db.addRow('animals', {'gender':'male', 'age':29})
	db.addRow('animals', {'gender':'female', 'age':13})
	db.addRow('animals', {'gender':'male', 'age':99})
	db.addRow('animals', {'gender':'female', 'age':59})
	db.addRow('animals', {'gender':'male', 'age':39})
	db.commit()
	print db.getTable('animals')
	print db.getRow('animals', {'gender':'male'})
	print "deleting 16 female"
	print db.delRow('animals', {'gender':'female', 'age':12})
	db.commit()
	print db.getTable('animals')
	#db.delTable('animals')
	#print db.getTable('animals')
	print db.getField('animals', {'age':'19'}, 'gender')
	print db.setField('animals', {'age':'99'}, 'gender', 'dogsex')
	db.commit()
	print db.getTable('animals')