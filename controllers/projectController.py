from db.db import DBconnection
from exceptions import ResourceNotFoundError, DatabaseError

class ProjectController:
    def  __init__(self):
        self.connection = DBconnection()
        self.numberOfProjects = self.getNumberOfProjects()

    def getNumberOfProjects(self):
        self.connection.createCursor()
        cursor = self.connection.cursor
        cursor.execute('SELECT COUNT(*) FROM projects')
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    def getProjectById(self, projectId):
        try:
            self.connection.createCursor()
            cursor = self.connection.cursor
            cursor.execute('SELECT * FROM projects WHERE id = ?', (projectId,))
            project = cursor.fetchone()
            if not project:
                raise ResourceNotFoundError(f"Project with ID {projectId} not found")
            return project
        finally:
            self.connection.closeCursor()
    
    def getProjects(self):
        self.connection.createCursor()
        cursor = self.connection.cursor
        cursor.execute('SELECT * FROM projects')
        projects = cursor.fetchall()
        cursor.close()
        return projects
    
    def getProjectsConcise(self):
        self.connection.createCursor()
        cursor = self.connection.cursor
        cursor.execute('SELECT id, name FROM projects')
        projects = [[row[0], row[1]] for row in cursor.fetchall()]
        cursor.close()
        return projects
    
    def addProject(self, name, description = None):
        self.connection.createCursor()
        cursor = self.connection.cursor
        cursor.execute('INSERT INTO projects (name, description) VALUES (?, ?)', (name, description))
        self.connection.connection.commit()
        self.numberOfProjects += 1
        cursor.close()
    
    def deleteProject(self, projectId):
        self.connection.createCursor()
        cursor = self.connection.cursor
        cursor.execute('DELETE FROM projects WHERE id = ?', (projectId,))
        self.connection.connection.commit()
        self.numberOfProjects -= 1
        cursor.close()