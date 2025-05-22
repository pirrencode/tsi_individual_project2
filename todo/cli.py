import argparse
from datetime import datetime

from .manager import TodoManager
from .storage import CSVTaskStorage


def parse_args():
    parser = argparse.ArgumentParser(description="Simple Todo Application")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title")
    add_parser.add_argument("--description", default="")
    add_parser.add_argument("--due")

    list_parser = subparsers.add_parser("list", help="List tasks")

    filter_parser = subparsers.add_parser("filter", help="Filter tasks")
    filter_parser.add_argument("--completed", action="store_true")
    filter_parser.add_argument("--title-contains")

    done_parser = subparsers.add_parser("done", help="Mark task complete")
    done_parser.add_argument("task_id", type=int)

    return parser.parse_args()


def main():
    args = parse_args()
    storage = CSVTaskStorage("tasks.csv")
    manager = TodoManager(storage)
    manager.load()

    if args.command == "add":
        due = datetime.fromisoformat(args.due) if args.due else None
        manager.add_task(args.title, description=args.description, due_date=due)
        manager.save()
        print("Task added")
    elif args.command == "list":
        for task in manager.list_tasks():
            print(task)
    elif args.command == "filter":
        predicate = lambda t: True
        if args.completed:
            predicate = lambda t: t.completed
        if args.title_contains:
            text = args.title_contains
            predicate = lambda t, p=predicate: p(t) and text in t.title
        for task in manager.filter_tasks(predicate):
            print(task)
    elif args.command == "done":
        manager.mark_complete(args.task_id)
        manager.save()
        print("Task marked complete")
    else:
        print("No command specified")

if __name__ == "__main__":
    main()
