#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime

def get_relative_time(due_date_str):
    try:
        # Parse day/month/year format matching your add_assignment script
        due_date = datetime.strptime(due_date_str, "%d/%m/%Y")
        now = datetime.now()
        # Strip time to compare exact days remaining
        today = datetime(now.year, now.month, now.day)
        delta = (due_date - today).days

        if delta == 0:
            return "Today"
        elif delta == 1:
            return "Tomorrow"
        elif delta < 0:
            return f"{abs(delta)}d ago"
        else:
            return f"{delta}d left"
    except Exception:
        return due_date_str

def main():
    home = os.path.expanduser("~")
    json_path = os.path.join(home, ".config/eww/assignments.json")

    # If file doesn't exist, output an empty list so Eww doesn't break
    if not os.path.exists(json_path):
        print(json.dumps([]))
        return

    try:
        with open(json_path, "r") as f:
            raw_assignments = json.load(f)
    except Exception:
        print(json.dumps([]))
        return

    # Filter out tasks where the due date has already passed
    now = datetime.now()
    today = datetime(now.year, now.month, now.day)
    assignments = []

    for task in raw_assignments:
        try:
            due_str = task.get("due", "")
            task_date = datetime.strptime(due_str, "%d/%m/%Y")
            # Only keep the assignment if it is due today or in the future
            if task_date >= today:
                assignments.append(task)
        except Exception:
            # Fallback to keep the task if the date format is unexpected
            assignments.append(task)

    formatted_list = []
    for task in assignments:
        # Handle old JSON elements safely by defaulting to False
        is_completed = task.get("completed", False)
        due_str = task.get("due", "")
        
        # Build the exact data dictionary Eww is expecting
        formatted_task = {
            "title": task.get("title", "Untitled Task"),
            "relative": get_relative_time(due_str),
            "completed": is_completed,
            "class": "completed" if is_completed else "",
            "box_class": "check-box checked" if is_completed else "check-box",
            "mark": "✔" if is_completed else " "
        }
        formatted_list.append(formatted_task)

    # Sort tasks so completed ones drop to the bottom of the list
    formatted_list.sort(key=lambda x: x["completed"])

    # Print the clean JSON string for Eww's defpoll to consume
    print(json.dumps(formatted_list))

if __name__ == "__main__":
    main()