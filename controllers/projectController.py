from db.db import DBconnection

class ProjectController:
    def  __init__(self):
        self.connection = DBconnection()

    def getProjectById(self, projectId):
        self.connection.createCursor()
        cursor = self.connection.cursor
        cursor.execute('SELECT * FROM projects WHERE id = ?', (projectId,))
        project = cursor.fetchone()
        cursor.close()
        return project
    
    def getProjects(self):
        self.connection.createCursor()
        cursor = self.connection.cursor
        cursor.execute('SELECT * FROM projects')
        projects = cursor.fetchall()
        cursor.close()
        return projects
    
    def addProject(self, name, description = None):
        self.connection.createCursor()
        cursor = self.connection.cursor
        cursor.execute('INSERT INTO projects (name, description) VALUES (?, ?)', (name, description))
        self.connection.connection.commit()
        cursor.close()