from controllers.projectController import ProjectController
from controllers.taskController import TaskController
from exceptions import JotterError, ResourceNotFoundError, DatabaseError, InvalidInputError
import utils
import sys

class App:
    def __init__(self):
        self.projectController = ProjectController()
        self.taskController = TaskController()
        self.done = False
        self.detailed = False
        self.currentProject = None

    def appLoop(self):
        while not self.done:
            try:
                if self.currentProject:
                    self.tasksMenu()
                else:
                    self.projectsMenu()
            except ResourceNotFoundError as e:
                print(f"\nError: {str(e)}")
            except DatabaseError as e:
                print(f"\nDatabase Error: {str(e)}")
            except InvalidInputError as e:
                print(f"\nInvalid Input: {str(e)}")
            except Exception as e:
                print(f"\nUnexpected error: {str(e)}")
                sys.exit(1)

    def displayActionsBar(self, actions):
        actionBar = ""
        for key in actions.keys():
            actionBar += f"{key} - {actions[key]}    "
        actionBar += "\n\n"
        print(actionBar)
    
    def handleAction(self, actions, action):
        if not action:
            raise InvalidInputError("No action provided")
        command = action[0]
        if command not in actions:
            raise InvalidInputError(f"Invalid command: {command}")
        args = action[2:].split(" ") if len(action) > 2 else []
        try:
            actions[command](args)
        except IndexError:
            raise InvalidInputError("Missing required arguments for command")
    
    def toggleDetailedView(self, args):
        self.detailed = not self.detailed

    def quit(self, args):
        self.done = True
    
    def displayProjects(self):
        if self.detailed:
            projects = self.projectController.getProjects()
            for project in projects:
                print(f"\tID: {project[0]}, Name: {project[1]}\n\t\tDescription: {project[2]}")
        else:
            projects = self.projectController.getProjects()
            for project in projects:
                print(f"\tID: {project[0]}, Name: {project[1]}")
        print("\n")
    
    def displayTasks(self):
        if self.detailed:
            tasks = self.taskController.getTasksByProjectId(self.currentProject)
            for task in tasks:
                print(f"\tID: {task[0]}, Name: {task[1]},\n\t\tDone: {task[3] == 1}\n\t\tDescription: {task[2]}")
        else:
            tasks = self.taskController.getTasksByProjectId(self.currentProject)
            for task in tasks:
                print(f"\tID: {task[0]}, Name: {task[1]}, Done: {task[3]}")
        print("\n")

    ## projects actions

    def projectsMenu(self):

        self.displayActionsBar(actions = {
            "c": "create new project",
            "o <projectId>": "open project <projectId>",
            "D <projectId>": "delete project <projectId>",
            "d": "toggle detailed view",
            "Q": "quit"
        })

        self.displayProjects()

        userAction = utils.validateInput(input(">>"))
        if not userAction:
            raise InvalidInputError("Invalid input")

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

        self.displayTasks()

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
        hasParent = utils.validateInput(input("Is this a sub-task? (y/n): "), ['y', 'n'])
        parentTask = None
        if hasParent == 'y':
            while not parentTask:
                parentTaskCandidate = utils.validateInput(input("Enter parent task ID: "))
                try:
                    parentTaskCandidate = int(parentTaskCandidate)
                    parentTaskRecord = self.taskController.getTaskById(parentTaskCandidate)
                    if parentTaskRecord[4] != self.currentProject:
                        print("Parent task does not belong to the current project. Do you want to try again?")
                        retry = utils.validateInput(input(">>"), ['y', 'n'])
                        if retry == 'n':
                            break
                        continue
                    parentTask = parentTaskCandidate
                except (ValueError, ResourceNotFoundError):
                    print("Invalid task ID. Do you want to try again?")
                    retry = utils.validateInput(input(">>"), ['y', 'n'])
                    if retry == 'n':
                        break
        

        if description == "":
            description = None
        self.taskController.addTask(name, self.currentProject, description, parentTask)

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