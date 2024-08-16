#!/usr/bin/env python

__author__ = 'Yuri Carreira Alflen'

import argparse
from task_manager_classes import Tasks

def main():
    """
    Main function to handle command-line arguments and perform the corresponding task operations.
    """
    parser = argparse.ArgumentParser(description="Task Manager")
    parser.add_argument('--add', type=str, help="Task description")
    parser.add_argument('--due', type=str, help="Due date in MM/DD/YYYY format")
    parser.add_argument('--priority', type=int, choices=[1, 2, 3], default=1, help="Priority of task; default value is 1")
    parser.add_argument('--list', action='store_true', help="List all tasks")
    parser.add_argument('--query', type=str, nargs='+', help="Search tasks by term")
    parser.add_argument('--done', type=int, help="Mark task as done by ID")
    parser.add_argument('--delete', type=int, help="Delete task by ID")
    parser.add_argument('--report', action='store_true', help="Generate a report of all tasks")

    args = parser.parse_args()  # Parse command-line arguments

    tasks = Tasks()  # Create the Tasks manager instance

    # Handle different command-line options
    if args.add:
        tasks.add(args.add, args.priority, args.due)
    elif args.list:
        tasks.list_tasks()
    elif args.query:
        tasks.query(args.query)
    elif args.done:
        tasks.mark_done(args.done)
    elif args.delete:
        tasks.delete(args.delete)
    elif args.report:
        tasks.report()
    else:
        parser.print_help()  # Display help if no valid arguments are provided

if __name__ == '__main__':
    main()
