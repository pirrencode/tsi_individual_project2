# Todo List Application

This project contains a simple command line todo list application written in Python. It demonstrates inheritance, multi-level inheritance, and interface objects while persisting data to CSV files.

## Usage

Run the application using Python's `-m` option:

```
python3 -m todo list           # List all tasks
python3 -m todo add "Title" --description "text" --due YYYY-MM-DDTHH:MM:SS
python3 -m todo filter --completed
python3 -m todo filter --title-contains text
python3 -m todo done TASK_ID
```

Tasks are stored in `tasks.csv` in the current directory.
