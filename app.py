from controllers.projectController import ProjectController
from controllers.taskController import TaskController
import utils

class App:
    def __init__(self):
        self.projectController = ProjectController()
        self.taskController = TaskController()
        self.done = False
        self.detailed = False

    def displayActionsBar(self, actions):
        actionBar = ""
        for key in actions.keys():
            actionBar += f"{key} - {actions[key]}\t"
        actionBar += "\n\n"
        print(actionBar)
    
    def handleAction(self, actions, action):
        command = action[0]
        args = action[2:].split(" ")
        actions[command](args)
    
    def toggleDetailedView(self, args):
        self.detailed = not self.detailed

    ## projects actions

    def projectsMenu(self):

        self.displayActionsBar(actions = {
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
            "o": self.openProject,
            "D": self.deleteProject,
            "d": self.toggleDetailedView
        }, action = userAction)

    def openProject(self, args):
        projectId = args[0]
        project = self.projectController.getProjectById(projectId)
        print(project)
            
    def deleteProject(self, args):
        projectId = args[0]
        project = self.projectController.getProjectById(projectId)
        print(f"Delete project: ID: {project[0]}, Name: {project[1]}?")
        
        userAction = utils.validateInput(input(">>"), ['y', 'n'])
        if userAction == 'y':
            self.projectController.deleteProject(projectId)

app = App()
while not app.done:
    app.projectsMenu()