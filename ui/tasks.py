from exceptions import InvalidInputError, ResourceNotFoundError
import utils

class Tasks:
    def __init__(self):
        self.detailed = False
        
    def organizeTasksHierarchy(self, tasks):
        taskMap = {task[0]: {"task": task, "children": []} for task in tasks}
        
        rootTasks = []
        for task in tasks:
            if task[5] is None:
                rootTasks.append(taskMap[task[0]])
            else:
                if task[5] in taskMap:
                    taskMap[task[5]]["children"].append(taskMap[task[0]])
        
        return rootTasks
    
    def printTaskHierarchy(self, taskNode, level=0, detailed=False):
        task = taskNode["task"]
        indent = "\t" + " " * level
        
        if detailed:
            print(f"{indent}ID: {task[0]}, Name: {task[1]},")
            print(f"{indent} Done: {task[3] == 1}")
            print(f"{indent} Description: {task[2]}")
        else:
            print(f"{indent}ID: {task[0]}, Name: {task[1]}, Done: {task[3] == 1}")
        
        for child in taskNode["children"]:
            self.printTaskHierarchy(child, level + 1, detailed)
    
    def displayTasks(self, taskController, currentProject):
        tasks = taskController.getTasksByProjectId(currentProject)
        taskHierarchy = self.organizeTasksHierarchy(tasks)
        
        for taskNode in taskHierarchy:
            self.printTaskHierarchy(taskNode, 0, self.detailed)
        
        print("\n")

    def tasksMenu(self, displayActionsBar):
        displayActionsBar(actions = {
            "c": "create new task",
            "e <taskId>": "edit task <taskId>",
            "D <taskId>": "delete task <taskId>",
            "d": "toggle detailed view",
            "C": "close project",
            "Q": "quit"
        })

        return utils.validateInput(input(">>"))

    def createTask(self, taskController, currentProject):
        name = input("Task name: ")
        description = input("Task description (optional): ")
        hasParent = utils.validateInput(input("Is this a sub-task? (y/n): "), ['y', 'n'])
        parentTask = None
        if hasParent == 'y':
            while not parentTask:
                parentTaskCandidate = utils.validateInput(input("Enter parent task ID: "))
                try:
                    parentTaskCandidate = int(parentTaskCandidate)
                    parentTaskRecord = taskController.getTaskById(parentTaskCandidate)
                    if parentTaskRecord[4] != currentProject:
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
        taskController.addTask(name, currentProject, description, parentTask)
    
    def editTask(self, args, taskController):
        taskId = args[0]
        task = taskController.getTaskById(taskId)
        print(f"Editing Task ID: {task[0]}, Name: {task[1]}, Description: {task[2]}, Done: {task[3] == 1}, Parent Task ID: {task[5]}")
        
        self.displayActionsBar(actions = {
            "n": "edit name",
            "d": "edit description",
            "D": "toggle done status",
            "p": "set parent task",
            "q": "quit editing"
        })

        userAction = utils.validateInput(input(">>"), ['n', 'd', 'D', 'p', 'q'])

        match userAction:
            case 'n':
                newName = input("New name: ")
                taskController.updateTask(taskId, name = newName)
            case 'd':
                newDescription = input("New description: ")
                taskController.updateTask(taskId, description = newDescription)
            case 'D':
                newDoneStatus = 0 if task[3] == 1 else 1
                taskController.updateTask(taskId, done = newDoneStatus)
            case 'p':
                newParentTask = None
                while newParentTask is None:
                    parentTaskCandidate = utils.validateInput(input("Enter new parent task ID (or leave blank to remove parent): "))
                    if parentTaskCandidate == "":
                        break
                    try:
                        parentTaskCandidate = int(parentTaskCandidate)
                        parentTaskRecord = taskController.getTaskById(parentTaskCandidate)
                        if parentTaskRecord[4] != self.currentProject:
                            print("Parent task does not belong to the current project. Do you want to try again?")
                            retry = utils.validateInput(input(">>"), ['y', 'n'])
                            if retry == 'n':
                                break
                            continue
                        newParentTask = parentTaskCandidate
                    except (ValueError, ResourceNotFoundError):
                        print("Invalid task ID. Do you want to try again?")
                        retry = utils.validateInput(input(">>"), ['y', 'n'])
                        if retry == 'n':
                            break
                taskController.updateTask(taskId, parentTask = newParentTask)
            case 'q':
                return

    def deleteTask(self, args, taskController):
        taskId = args[0]
        task = taskController.getTaskById(taskId)
        print(f"Delete task: ID: {task[0]}, Name: {task[1]}?")
        
        userAction = utils.validateInput(input(">>"), ['y', 'n'])
        if userAction == 'y':
            taskController.deleteTask(taskId)