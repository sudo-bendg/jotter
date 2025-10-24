import sqlite3
from exceptions import DatabaseError

class DBconnection:
    def __init__(self, db_name='jotter.db'):
        try:
            self.connection = sqlite3.connect(db_name)
            self.cursor = None
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to connect to database: {str(e)}")
    
    def createCursor(self):
        try:
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to create database cursor: {str(e)}")
    
    def closeCursor(self):
        if self.cursor:
            try:
                self.cursor.close()
                self.cursor = None
            except sqlite3.Error as e:
                raise DatabaseError(f"Failed to close cursor: {str(e)}")
    
    def closeConnection(self):
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
            except sqlite3.Error as e:
                raise DatabaseError(f"Failed to close database connection: {str(e)}")