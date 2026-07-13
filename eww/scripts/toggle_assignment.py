#!/usr/bin/env python3
import json
import os
import sys

if len(sys.argv) < 2:
    sys.exit(1)

target_title = sys.argv[1]
home = os.path.expanduser("~")
json_path = os.path.join(home, ".config/eww/assignments.json")

try:
    with open(json_path, "r") as f:
        data = json.load(f)
except Exception:
    sys.exit(1)

# Find the task and flip its completed status
for task in data:
    if task.get("title") == target_title:
        task["completed"] = not task.get("completed", False)
        break

with open(json_path, "w") as f:
    json.dump(data, f, indent=2)