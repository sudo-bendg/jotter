from controllers.projectController import ProjectController
from controllers.taskController import TaskController
import utils

class App:
    def __init__(self):
        self.projectController = ProjectController()
        self.taskController = TaskController()
        self.done = False
        self.detailed = False
        self.currentProject = None

    def appLoop(self):
        while not self.done:
            if self.currentProject:
                self.tasksMenu()
            else:
                self.projectsMenu()

    def displayActionsBar(self, actions):
        actionBar = ""
        for key in actions.keys():
            actionBar += f"{key} - {actions[key]}    "
        actionBar += "\n\n"
        print(actionBar)
    
    def handleAction(self, actions, action):
        command = action[0]
        args = action[2:].split(" ")
        actions[command](args)
    
    def toggleDetailedView(self, args):
        self.detailed = not self.detailed

    def quit(self, args):
        self.done = True

    ## projects actions

    def projectsMenu(self):

        self.displayActionsBar(actions = {
            "c": "create new project",
            "o <projectId>": "open project <projectId>",
            "D <projectId>": "delete project <projectId>",
            "d": "toggle detailed view",
            "Q": "quit"
        })

        if self.detailed:
            projects = self.projectController.getProjects()
            for project in projects:
                print(f"\tID: {project[0]}, Name: {project[1]}\n\t\tDescription: {project[2]}")
        else:
            projects = self.projectController.getProjects()
            for project in projects:
                print(f"\tID: {project[0]}, Name: {project[1]}")
        userAction = utils.validateInput(input(">>"))

        self.handleAction(actions = {
            "c": self.createProject,
            "o": self.openProject,
            "D": self.deleteProject,
            "d": self.toggleDetailedView,
            "Q": self.quit
        }, action = userAction)

    def createProject(self, args):
        name = input("Project name: ")
        description = input("Project description (optional): ")
        if description == "":
            description = None
        self.projectController.addProject(name, description)

    def openProject(self, args):
        projectId = args[0]
        project = self.projectController.getProjectById(projectId)
        self.currentProject = project[0]
            
    def deleteProject(self, args):
        projectId = args[0]
        project = self.projectController.getProjectById(projectId)
        print(f"Delete project: ID: {project[0]}, Name: {project[1]}?")
        
        userAction = utils.validateInput(input(">>"), ['y', 'n'])
        if userAction == 'y':
            self.projectController.deleteProject(projectId)
    
    ## Tasks actions
    def tasksMenu(self):
        
        self.displayActionsBar(actions = {
            "c": "create new task",
            "o <taskId>": "open task <taskId>",
            "D <taskId>": "delete tassk <taskId>",
            "d": "toggle detailed view",
            "C": "close project",
            "Q": "quit"
        })

        if self.detailed:
            tasks = self.taskController.getTasksByProjectId(self.currentProject)
            for task in tasks:
                print(f"\tID: {task[0]}, Name: {task[1]},\n\t\tDone: {task[3] == 1}\n\t\tDescription: {task[2]}")
        else:
            tasks = self.taskController.getTasksByProjectId(self.currentProject)
            for task in tasks:
                print(f"\tID: {task[0]}, Name: {task[1]}, Done: {task[3]}")
        userAction = utils.validateInput(input(">>"))

        self.handleAction(actions = {
            "c": self.createTask,
            "o": self.openTask,
            "D": self.deleteTask,
            "d": self.toggleDetailedView,
            "C": self.closeProject,
            "Q": self.quit
        }, action = userAction)

    def createTask(self, args):
        name = input("Task name: ")
        description = input("Task description (optional): ")
        if description == "":
            description = None
        self.taskController.addTask(name, self.currentProject, description)

    def openTask(self, args):
        taskId = args[0]
        task = self.taskController.getTaskById(taskId)
        print(f"Task ID: {task[0]}, Name: {task[1]}, Description: {task[2]}, Done: {task[3]}")

    def deleteTask(self, args):
        taskId = args[0]
        task = self.taskController.getTaskById(taskId)
        print(f"Delete task: ID: {task[0]}, Name: {task[1]}?")
        
        userAction = utils.validateInput(input(">>"), ['y', 'n'])
        if userAction == 'y':
            self.taskController.deleteTask(taskId)
    
    def closeProject(self, args):
        self.currentProject = None

app = App()
app.appLoop()