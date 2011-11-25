"""
Base DB class
A DB plugin should implement all the methods here even if they are NOPs.
"""

class DBBase:
        def connect(self, dbinfo): print "WTF BAD DB BAD"
        def disconnect(self): print "WTF BAD DB BAD"

        def commit(self): print "WTF BAD DB BAD"
        def rollback(self): print "WTF BAD DB BAD"

        def addRow(self, table, values): print ("WTF BAD DB BAD")
        def delRow(self, table, search): print ("WTF BAD DB BAD")
        def getRow(self, table, search): print ("WTF BAD DB BAD")

        def getField(self, table, search, field): print ("WTF BAD DB BAD")
        def setField(self, table, search, field, value): print ("WTF BAD DB BAD")

        def addTable(self, table, values): print "WTF BAD DB BAD"
        def delTable(self, table): print "WTF BAD DB BAD"
        def getTable(self, table): print "WTF BAD DB BAD"
