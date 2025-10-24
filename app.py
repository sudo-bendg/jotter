from db.migration import runMigrations
runMigrations()
from controllers.projectController import ProjectController
from controllers.taskController import TaskController
from exceptions import JotterError, ResourceNotFoundError, DatabaseError, InvalidInputError
from ui.projects import Projects
from ui.tasks import Tasks
import utils
import sys

class App(Projects, Tasks):
    def __init__(self):
        Projects.__init__(self)
        Tasks.__init__(self)
        self.projectController = ProjectController()
        self.taskController = TaskController()
        self.done = False
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
        actionBar = "\n"
        for key in actions.keys():
            actionBar += f"\t{key} - {actions[key]}\n"
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
    
    def displayTasks(self):
        super().displayTasks(self.taskController, self.currentProject)

    ## projects actions

    def projectsMenu(self):
        userAction = super().projectsMenu(self.projectController, self.displayActionsBar)
        
        self.handleAction(actions = {
            "c": lambda args: self.createProject(self.projectController),
            "o": lambda args: self.openProject(args, self.projectController),
            "D": lambda args: self.deleteProject(args, self.projectController),
            "d": self.toggleDetailedView,
            "Q": self.quit
        }, action = userAction)
    
    ## Tasks actions
    def tasksMenu(self):
        self.displayTasks()
        userAction = super().tasksMenu(self.displayActionsBar)

        self.handleAction(actions = {
            "c": lambda args: self.createTask(self.taskController, self.currentProject),
            "e": lambda args: self.editTask(args, self.taskController),
            "D": lambda args: self.deleteTask(args, self.taskController),
            "d": self.toggleDetailedView,
            "C": self.closeProject,
            "Q": self.quit
        }, action = userAction)

    def closeProject(self, args):
        self.currentProject = None

print("""
==============================================================
                                                            
    ██                                                    
    ▀▀               ██        ██                         
  ████    ▄████▄   ███████   ███████    ▄████▄    ██▄████ 
    ██   ██▀  ▀██    ██        ██      ██▄▄▄▄██   ██▀     
    ██   ██    ██    ██        ██      ██▀▀▀▀▀▀   ██      
    ██   ▀██▄▄██▀    ██▄▄▄     ██▄▄▄   ▀██▄▄▄▄█   ██      
    ██     ▀▀▀▀       ▀▀▀▀      ▀▀▀▀     ▀▀▀▀▀    ▀▀      
 ████▀                                                    
                                                            
      
      - Benjamin Godfrey
      
==============================================================""")

app = App()
app.appLoop()