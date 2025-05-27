#!/usr/bin/env python3
import sys
import json
import os
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
from tkinter import simpledialog

# Default font for UI elements
DEFAULT_FONT = ("Helvetica", 12)

TODO_FILE = 'todo.json'

def load_tasks():
    """Load tasks from the JSON file (or return empty list)."""
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, 'r') as f:
        return json.load(f)

def save_tasks(tasks):
    """Save the list of tasks back to the JSON file."""
    with open(TODO_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def list_tasks(tasks):
    """Print all tasks with their status and ID."""
    if not tasks:
        print("No tasks yet. Use `add` to create one.")
        return
    for i, task in enumerate(tasks, 1):
        status = "✓" if task["done"] else " "
        print(f"{i}. [{status}] {task['desc']}")

def add_task(tasks, desc):
    """Add a new task with description `desc`."""
    tasks.append({"desc": desc, "done": False})
    save_tasks(tasks)
    print(f"Added: {desc!r}")

def complete_task(tasks, idx):
    """Mark task at 1-based index `idx` as done."""
    try:
        tasks[idx-1]["done"] = True
        save_tasks(tasks)
        print(f"Completed task #{idx}")
    except IndexError:
        print(f"No task with ID #{idx}")

def remove_task(tasks, idx):
    """Remove task at 1-based index `idx`."""
    try:
        removed = tasks.pop(idx-1)
        save_tasks(tasks)
        print(f"Removed: {removed['desc']!r}")
    except IndexError:
        print(f"No task with ID #{idx}")

def print_help():
    print("""Usage:
  todo.py list
      List all tasks.
  todo.py add "task description"
      Add a new task.
  todo.py done <task_id>
      Mark task as completed.
  todo.py rm <task_id>
      Remove a task.
  todo.py help
      Show this help message.
""")

def run_interactive(tasks):
    """Interactive mode: prompt user for commands in a loop."""
    while True:
        print("\nCommands: list, add, done, rm, help, exit")
        choice = input("Enter command: ").strip().split()
        if not choice:
            continue
        cmd = choice[0].lower()
        if cmd == 'list':
            list_tasks(tasks)
        elif cmd == 'add':
            desc = " ".join(choice[1:]) if len(choice) > 1 else input("Task description: ").strip()
            add_task(tasks, desc)
        elif cmd in ('done', 'complete'):
            if len(choice) > 1 and choice[1].isdigit():
                complete_task(tasks, int(choice[1]))
            else:
                idx = input("Task ID to complete: ").strip()
                if idx.isdigit():
                    complete_task(tasks, int(idx))
                else:
                    print("Please enter a valid number.")
        elif cmd in ('rm', 'remove'):
            if len(choice) > 1 and choice[1].isdigit():
                remove_task(tasks, int(choice[1]))
            else:
                idx = input("Task ID to remove: ").strip()
                if idx.isdigit():
                    remove_task(tasks, int(idx))
                else:
                    print("Please enter a valid number.")
        elif cmd == 'help':
            print_help()
        elif cmd in ('exit', 'quit'):
            print("Goodbye!")
            break
        else:
            print(f"Unknown command: {cmd}")
            print_help()

def run_gui(tasks):
    """GUI mode: open a free-form text area for task management."""
    root = tk.Tk()
    root.title("To-Do List")
    root.geometry("400x400")
    root.configure(bg="#fafafa")

    # Free-form text area for tasks
    text = tk.Text(root, font=("Helvetica", 14), bd=0, highlightthickness=1, relief=tk.FLAT)
    text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_text():
        text.delete("1.0", tk.END)
        for task in tasks:
            text.insert(tk.END, task["desc"] + "\n")

    def save_text(event=None):
        lines = text.get("1.0", tk.END).strip().splitlines()
        tasks[:] = [{"desc": line, "done": False} for line in lines if line.strip()]
        save_tasks(tasks)

    # Bind any change in text to saving tasks
    text.bind("<KeyRelease>", save_text)

    load_text()
    root.mainloop()

def main():
    tasks = load_tasks()
    if len(sys.argv) == 1:
        run_gui(tasks)
        return
    if len(sys.argv) < 2 or sys.argv[1] == 'help':
        print_help()
        return

    cmd = sys.argv[1]
    if cmd == 'list':
        list_tasks(tasks)
    elif cmd == 'add' and len(sys.argv) >= 3:
        add_task(tasks, " ".join(sys.argv[2:]))
    elif cmd in ('done', 'complete') and len(sys.argv) == 3:
        complete_task(tasks, int(sys.argv[2]))
    elif cmd in ('rm', 'remove') and len(sys.argv) == 3:
        remove_task(tasks, int(sys.argv[2]))
    else:
        print(f"Unknown command: {cmd!r}")
        print_help()

if __name__ == '__main__':
    main()