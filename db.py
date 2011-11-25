from config import dbConfig
db_plugin = from db __import__(dbConfig['database_type'])

class DB(db_plugin.DBPlugin):
	def __init__(self):
		db_plugin.DBPlugin.__init__(self)

	def clientAdd(): pass
	def clientDel(): pass
	def clientModify(): pass
	def clientSearch(field, value): pass

	def clientSelect(): pass

	def aliasAdd(): pass
	def aliasDel(): pass
	def aliasSearch(): pass
	def aliasSelect(): pass

	def penaltyAdd(): pass
	def penaltyDel(): pass
	def penaltyModify(): pass
	def penaltySearch(): pass
	def penaltySelect(): pass

	def defaultTableSet(): pass