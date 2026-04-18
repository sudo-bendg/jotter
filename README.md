# Jotter

Jotter is a terminal-based task manager. It lets you organise work into projects, each of which holds a list of tasks. Tasks can be nested under one another, so you can break larger pieces of work down into sub-tasks.

All data is stored locally in a SQLite database at `~/.jotter.db`. No account or internet connection is required.

## Requirements

- Python 3.10 or later (the code uses `match` statements)

No third-party packages are needed. Jotter uses only the Python standard library.

## Installation

Clone the repository and run the app directly with Python:

```bash
git clone https://github.com/benjamingodfrey/jotter.git
cd jotter
python app.py
```

## How it works

When you start Jotter you are shown your list of projects. From there you can:

| Command | Action |
|---|---|
| `c` | Create a new project |
| `o <id>` | Open a project by its ID |
| `D <id>` | Delete a project |
| `d` | Toggle detailed view (shows descriptions) |
| `Q` | Quit |

Opening a project takes you into its task list. From there you can:

| Command | Action |
|---|---|
| `c` | Create a new task |
| `e <id>` | Edit a task |
| `D <id>` | Delete a task |
| `d` | Toggle detailed view |
| `C` | Close the project and go back |
| `Q` | Quit |

When creating a task, you will be asked whether it is a sub-task. If it is, you can assign it a parent task from within the same project. Tasks are displayed in a tree structure, with sub-tasks indented beneath their parent.

When editing a task, you can change its name, description, done status, or parent task.

## Data

The database is created automatically on first run at `~/.jotter.db`. Deleting this file will remove all your data.

## Compatibility

Jotter has been designed to work on Linux machines primarily. For users of Mac or Windows who face difficulty on setup, support can be found [here](https://ubuntu.com/tutorials/install-ubuntu-desktop).