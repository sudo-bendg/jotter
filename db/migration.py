from db import DBconnection

connection = DBconnection()

def createProjectsTable():
    connection.createCursor()
    cursor = connection.cursor
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
    ''')
    connection.connection.commit()
    cursor.close()

def dropProjectsTable():
    connection.createCursor()
    cursor = connection.cursor
    cursor.execute('DROP TABLE IF EXISTS projects')
    connection.connection.commit()
    cursor.close()

def createTasksTable():
    connection.createCursor()
    cursor = connection.cursor
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            parentProject INTEGER NOT NULL,
            parentTask INTEGER,
            FOREIGN KEY(parentProject) REFERENCES projects(id),
            FOREIGN KEY(parentTask) REFERENCES tasks(id)
        )
    ''')
    connection.connection.commit()
    cursor.close()

def dropTasksTable():
    connection.createCursor()
    cursor = connection.cursor
    cursor.execute('DROP TABLE IF EXISTS tasks')
    connection.connection.commit()
    cursor.close()

dropTableMigrations = [dropProjectsTable, dropTasksTable]
createTableMigrations = [createProjectsTable, createTasksTable]