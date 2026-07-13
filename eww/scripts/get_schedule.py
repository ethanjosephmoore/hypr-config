#!/usr/bin/env python3
import json
from datetime import datetime

def get_current_schedule():
    # 1. Map out Week A
    week_a = {
        "Monday":    ["Maths", "English", "Science", "History", "Geography", "Art"],
        "Tuesday":   ["French", "Maths", "PE", "PE", "Computing", "English"],
        "Wednesday": ["Science", "Science", "Maths", "Music", "Drama", "English"],
        "Thursday":  ["RE", "Geography", "English", "Maths", "Biology", "Chemistry"],
        "Friday":    ["Physics", "Computing", "History", "Maths", "English", "Study"],
        "Saturday":  [], "Sunday": []
    }
    
    # 2. Map out Week B
    week_b = {
        "Monday":    ["English", "Maths", "History", "Science", "Art", "Geography"],
        "Tuesday":   ["Computing", "French", "English", "Maths", "PE", "PE"],
        "Wednesday": ["Drama", "Music", "English", "Science", "Science", "Maths"],
        "Thursday":  ["Biology", "Chemistry", "RE", "Geography", "Maths", "English"],
        "Friday":    ["Study", "Physics", "Maths", "Computing", "History", "English"],
        "Saturday":  [], "Sunday": []
    }
    
    # 3. Figure out if it's Week A or Week B based on the calendar week number
    # %V gets the ISO week number (1 to 53)
    week_num = int(datetime.now().strftime("%V"))
    
    if week_num % 2 == 0:
        current_week_matrix = week_a
        week_label = "Week A"
    else:
        current_week_matrix = week_b
        week_label = "Week B"
        
    # 4. Get today's day name and fetch the lessons
    current_day = datetime.now().strftime("%A")
    lessons = current_week_matrix.get(current_day, [])
    
    # Weekend fallback
    if not lessons:
        return {
            "week": week_label,
            "day": current_day,
            "lessons": [{"period": i+1, "subject": "No Lessons"} for i in range(6)]
        }
        
    return {
        "week": week_label,
        "day": current_day,
        "lessons": [{"period": i+1, "subject": sub} for i, sub in enumerate(lessons)]
    }

if __name__ == "__main__":
    print(json.dumps(get_current_schedule()))