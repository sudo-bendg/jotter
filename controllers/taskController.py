from db.db import DBconnection
from exceptions import ResourceNotFoundError, DatabaseError

class TaskController:
    def __init__(self):
        self.db = DBconnection()
        self.numberOfTasks = self.getNumberOfTasks()

    def getNumberOfTasks(self):
        self.db.createCursor()
        cursor = self.db.cursor
        cursor.execute('SELECT COUNT(*) FROM tasks')
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    def getTaskById(self, taskId):
        try:
            self.db.createCursor()
            cursor = self.db.cursor
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (taskId,))
            task = cursor.fetchone()
            if not task:
                raise ResourceNotFoundError(f"Task with ID {taskId} not found")
            return task
        finally:
            self.db.closeCursor()
    
    def getTasks(self):
        self.db.createCursor()
        cursor = self.db.cursor
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()
        cursor.close()
        return tasks
    
    def getTasksByProjectId(self, projectId):
        self.db.createCursor()
        cursor = self.db.cursor
        cursor.execute('SELECT * FROM tasks WHERE parentProject = ?', (projectId,))
        tasks = cursor.fetchall()
        cursor.close()
        return tasks
    
    def getTasksByParentTaskId(self, parentTaskId):
        self.db.createCursor()
        cursor = self.db.cursor
        cursor.execute('SELECT * FROM tasks WHERE parentTask = ?', (parentTaskId,))
        tasks = cursor.fetchall()
        cursor.close()
        return tasks
    
    def addTask(self, name, parentProject, description=None, parentTask=None):
        self.db.createCursor()
        cursor = self.db.cursor
        cursor.execute(
            'INSERT INTO tasks (name, description, parentProject, parentTask) VALUES (?, ?, ?, ?)', 
            (name, description, parentProject, parentTask)
        )
        self.db.connection.commit()
        self.numberOfTasks += 1
        cursor.close()
    
    def deleteTask(self, taskId):
        self.db.createCursor()
        cursor = self.db.cursor
        childTasks = self.getTasksByParentTaskId(taskId)
        for child in childTasks:
            self.deleteTask(child[0])
        cursor.execute('DELETE FROM tasks WHERE id = ?', (taskId,))
        self.db.connection.commit()
        self.numberOfTasks -= 1
        cursor.close()
    
    def deleteTasksByProjectId(self, projectId):
        self.db.createCursor()
        cursor = self.db.cursor
        cursor.execute('SELECT COUNT(*) FROM tasks WHERE parentProject = ?', (projectId,))
        deleted_count = cursor.fetchone()[0]
        cursor.execute('DELETE FROM tasks WHERE parentProject = ?', (projectId,))
        self.db.connection.commit()
        self.numberOfTasks -= deleted_count
        cursor.close()
    
    def updateTask(self, taskId, name=None, description=None, done=None, parentTask=None):
        self.db.createCursor()
        cursor = self.db.cursor
        updates = []
        params = []
        if name is not None:
            updates.append('name = ?')
            params.append(name)
        if description is not None:
            updates.append('description = ?')
            params.append(description)
        if done is not None:
            updates.append('done = ?')
            params.append(done)
        if parentTask is not None:
            updates.append('parentTask = ?')
            params.append(parentTask)
        params.append(taskId)
        update_clause = ', '.join(updates)
        cursor.execute(f'UPDATE tasks SET {update_clause} WHERE id = ?', params)
        self.db.connection.commit()
        cursor.close()