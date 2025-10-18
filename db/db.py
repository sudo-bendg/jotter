import sqlite3

class DBconnection:
    def __init__(self, db_name='jotter.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = None
    
    def createCursor(self):
        self.cursor = self.connection.cursor()
    
    def closeCursor(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None
    
    def closeConnection(self):
        if self.connection:
            self.connection.close()
            self.connection = None