#!/bin/bash

# Initialize variables to keep track of the current state
last_ws=""

while true; do
    # Get the current focused workspace ID safely
    current_ws=$(hyprctl monitors -j | jq '.[] | select(.focused == true) | .activeWorkspace.id' 2>/dev/null)
    
    # If it failed to read, default to workspace 1
    if [ -z "$current_ws" ]; then
        current_ws="1"
    fi

    # Only output if the workspace actually changed to avoid spamming Eww
    if [ "$current_ws" != "$last_ws" ]; then
        echo "$current_ws"
        last_ws="$current_ws"
    fi

    # Check every 50 milliseconds for snappy, near-instant updates
    sleep 0.05
done