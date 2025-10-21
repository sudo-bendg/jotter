from controllers.projectController import ProjectController
from controllers.taskController import TaskController
import utils

class App:
    def __init__(self):
        self.projectController = ProjectController()
        self.taskController = TaskController()

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

    ## projects actions

    def projectsMenu(self, detailed=False):
        self.displayActionsBar(actions = {
            "o <projectId>": "open project <projectId>",
            "e <projectId>": "edit project <projectId>",
            "D <projectId>": "delete project <projectId>",
            "d": "toggle detailed view",
            "Q": "quit"
        })
        if detailed:
            projects = self.projectController.getProjects()
            for project in projects:
                print(f"\tID: {project[0]}, Name: {project[1]}\n\t\tDescription: {project[2]}")
        else:
            projects = self.projectController.getProjects()
            for project in projects:
                print(f"\tID: {project[0]}, Name: {project[1]}")
        userAction = utils.validateInput(input(">>"))
        self.handleAction(actions = {
            "o": self.openProject
        }, action = userAction)

    def openProject(self, args):
        projectId = args[0]
        project = self.projectController.getProjectById(projectId)
        print(project)
            
        ## menu options
        

app = App()
app.projectsMenu(True)