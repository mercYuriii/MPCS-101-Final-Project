#!/usr/bin/env python

__author__ = 'Yuri Carreira Alflen'

import pickle
from datetime import datetime

class Task:
    """Representation of a task
  
  Attributes:
              - created - date
              - completed - date
              - name - string
              - unique id - number
              - priority - int value of 1, 2, or 3; 1 is default
              - due date - date, this is optional"""
    
    #Create counter of how many tasks have been made
    task_counter = 1

    def __init__(self, name, priority=1, due_date=None):
        """Initializes a new Task object."""
        #ID should be current counter
        self.id = Task.task_counter
        #add 1 to counter for next task
        Task.task_counter += 1
        self.name = name
        #tasks have default priority of 1
        self.priority = priority
        self.due_date = due_date
        self.created = datetime.now()
        #tasks are not completed when created
        self.completed = None

    def mark_done(self):
        """Marks the task as completed and records the completion date."""
        self.completed = datetime.now()

    def is_done(self):
        """Returns True if the task is completed, False otherwise."""
        #if it's not None, then it must be completed
        return self.completed is not None

    def __str__(self):
        if self.due_date != None:
            due = self.due_date.strftime("%m/%d/%Y")
        else: 
            due = "-"
        if self.completed != None:
            completed = self.completed_date.strftime("%a %b %d %H:%M:%S %Y") 
        else: 
            completed = "-"
        return f"Task {self.id}: {self.name} (Priority: {self.priority})"

class Tasks:
    """A list of Task objects and methods to manage them."""
    
    def __init__(self):
        """Initializes the Tasks manager."""
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        """Loads tasks from the pickle file."""
        try:
            with open('.todo.pickle', 'rb') as f:
                self.tasks = pickle.load(f)
                Task.task_counter = max(task.id for task in self.tasks) + 1
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        """Saves the current task list to the pickle file."""
        with open('.todo.pickle', 'wb') as f:
            pickle.dump(self.tasks, f)

    def add(self, name, priority=1, due_date=None):
        """Adds a new task to the list."""
        try:
            #check for due date
            if due_date != None:
                due_date_obj = datetime.strptime(due_date, '%m/%d/%Y')
            else: 
                due_date_obj = None

            #create task    
            task = Task(name, priority, due_date_obj)
            self.tasks.append(task)
            self.save_tasks()
            print(f"Created task {task.id}")
        except ValueError:
            print("Invalid date format. Please use MM/DD/YYYY.")

    def list_tasks(self):
        """Lists all tasks that are not yet completed."""
        active_tasks = [task for task in self.tasks if not task.is_done()]
        sorted_tasks = sorted(active_tasks, key=lambda t: (t.due_date or datetime.max, -t.priority, t.created))

        print(f"{'ID':<5} {'Age':<5} {'Due Date':<12} {'Priority':<10} {'Task':<25}")
        print(f"{'--':<5} {'---':<5} {'--------':<12} {'--------':<10} {'----':<25}")

        #loop through tasks
        for task in sorted_tasks:
            # Calculate the age of the task in days
            age = (datetime.now() - task.created).days  
            
            if task.due_date != None:
                due_date = task.due_date.strftime('%m/%d/%Y')
            else:
                due_date = '-'
            
            print(f"{task.id:<5} {age:<5} {due_date:<12} {task.priority:<10} {task.name:<25}")

    def query(self, terms):
        """Searches for tasks that match any of the provided terms."""
        matching_tasks = [task for task in self.tasks if not task.is_done() and any(term.lower() in task.name.lower() for term in terms)]

        # Formatting
        print(f"{'ID':<5} {'Age':<5} {'Due Date':<12} {'Priority':<10} {'Task':<25}")
        print(f"{'--':<5} {'---':<5} {'--------':<12} {'--------':<10} {'----':<25}")

        for task in matching_tasks:
            # Calculate the age of the task in days            
            age = (datetime.now() - task.created).days
            
            if task.due_date != None:
                due_date = task.due_date.strftime('%m/%d/%Y')
            else:
                due_date = '-'

            print(f"{task.id:<5} {age:<5} {due_date:<12} {task.priority:<10} {task.name:<25}")

    def mark_done(self, task_id):
        """Marks a task as completed by its ID."""
        for task in self.tasks:
            if task.id == task_id:
                task.mark_done()
                self.save_tasks()
                print(f"Completed task {task_id}")
                return
        print(f"No task found with ID {task_id}")

    def delete(self, task_id):
        """Deletes a task by its ID."""
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                self.save_tasks()
                print(f"Deleted task {task_id}")
                return
        print(f"No task found with ID {task_id}")

    def report(self):
        """Generates a report listing all tasks, including completed ones."""

        # Header with fixed column widths
        print(f"{'ID':<5} {'Age':<5} {'Due Date':<12} {'Priority':<10} {'Task':<30} {'Created':<25} {'Completed':<25}")
        print(f"{'--':<5} {'---':<5} {'--------':<12} {'--------':<10} {'----':<30} {'-------------------------':<25} {'-------------------------':<25}")

        for task in self.tasks:
             # Calculate the age of the task in days
            age = (datetime.now() - task.created).days

            if task.due_date != None:
                due_date = task.due_date.strftime('%m/%d/%Y')
            else:
                due_date = '-'
            
            created_date = task.created.strftime('%a %b %d %H:%M:%S %Y')
                
            if task.completed != None:
               completed_date = task.completed.strftime('%a %b %d %H:%M:%S %Y')
            else:
                completed_date = '-'

            print(f"{task.id:<5} {age:<5} {due_date:<12} {task.priority:<10} {task.name:<30} {created_date:<25} {completed_date:<25}")
