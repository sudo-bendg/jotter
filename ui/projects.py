from exceptions import InvalidInputError
import utils

class Projects:
    def __init__(self):
        self.detailed = False
        
    def displayProjects(self, projectController):
        if self.detailed:
            projects = projectController.getProjects()
            for project in projects:
                print(f"\tID: {project[0]}, Name: {project[1]}\n\t\tDescription: {project[2]}")
        else:
            projects = projectController.getProjects()
            for project in projects:
                print(f"\tID: {project[0]}, Name: {project[1]}")
        print("\n")

    def projectsMenu(self, projectController, displayActionsBar):
        displayActionsBar(actions = {
            "c": "create new project",
            "o <projectId>": "open project <projectId>",
            "D <projectId>": "delete project <projectId>",
            "d": "toggle detailed view",
            "Q": "quit"
        })

        self.displayProjects(projectController)

        userAction = utils.validateInput(input(">>"))
        if not userAction:
            raise InvalidInputError("Invalid input")

        return userAction

    def createProject(self, projectController):
        name = input("Project name: ")
        description = input("Project description (optional): ")
        if description == "":
            description = None
        projectController.addProject(name, description)

    def openProject(self, args, projectController):
        projectId = args[0]
        project = projectController.getProjectById(projectId)
        return project[0]
            
    def deleteProject(self, args, projectController):
        projectId = args[0]
        project = projectController.getProjectById(projectId)
        print(f"Delete project: ID: {project[0]}, Name: {project[1]}?")
        
        userAction = utils.validateInput(input(">>"), ['y', 'n'])
        if userAction == 'y':
            projectController.deleteProject(projectId)