#!/usr/bin/env python3
import json
import os
import subprocess

home = os.path.expanduser("~")
json_path = os.path.join(home, ".config/eww/assignments.json")

def get_input():
    # 1. Pop up a text entry window for the title
    title_cmd = ["zenity", "--entry", "--title=New Assignment", "--text=Enter assignment title:"]
    title = subprocess.check_output(title_cmd).decode("utf-8").strip()
    
    if not title: return

    # 2. Pop up a calendar window to select the due date
    cal_cmd = ["zenity", "--calendar", "--title=Due Date", "--text=Select the deadline:", "--date-format=%d/%m/%Y"]
    due_date = subprocess.check_output(cal_cmd).decode("utf-8").strip()
    
    if not due_date: return

    # 3. Read existing data and add the new task
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append({"title": title, "due": due_date})

    # 4. Save back to the JSON file
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    try:
        get_input()
    except subprocess.CalledProcessError:
        pass # User clicked cancel