from db.db import DBconnection

class TaskController:
    def __init__(self):
        self.db = DBconnection()
        self.db.createCursor()

    def getTaskById(self, taskId):
        cursor = self.db.cursor
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (taskId))
        task = cursor.fetchone()
        cursor.close()
        return task
    
    def getTasks(self):
        cursor = self.db.cursor
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()
        cursor.close()
        return tasks
    
    def getTasksByProject(self, projectId):
        cursor = self.db.cursor
        cursor.execute('SELECT * FROM tasks WHERE parentProject = ?', (projectId))
        tasks = cursor.fetchall()
        cursor.close()
        return tasks
    
    def addTask(self, name, parentProject, description=None, parentTask=None):
        cursor = self.db.cursor
        cursor.execute(
            'INSERT INTO tasks (name, description, parentProject, parentTask) VALUES (?, ?, ?, ?)', 
            (name, description, parentProject, parentTask)
        )
        self.db.connection.commit()
        cursor.close()