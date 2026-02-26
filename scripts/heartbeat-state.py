#!/usr/bin/env python3
"""
Heartbeat state manager - tracks which checks ran last
"""
import json
import os
from datetime import datetime

STATE_FILE = os.path.expanduser("~/.openclaw/workspace/memory/heartbeat-state.json")

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"lastChecks": {"email": None, "teams": None, "calendar": None, "weather": None}, "lastMaintenance": None}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def get_next_check():
    """Return the check that hasn't run in the longest time"""
    state = load_state()
    now = datetime.now().timestamp()
    
    # Find the oldest check
    oldest = None
    oldest_time = float('inf')
    
    for check, last_run in state["lastChecks"].items():
        if last_run is None:
            # Never run - prioritize this
            return check, None
        age = now - last_run
        if age < oldest_time:
            oldest_time = age
            oldest = check
    
    return oldest, oldest_time

def mark_check_run(check_name):
    """Mark a check as having run now"""
    state = load_state()
    state["lastChecks"][check_name] = datetime.now().timestamp()
    save_state(state)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        # Print next check
        check, age = get_next_check()
        if age:
            print(f"Next check: {check} (last ran {int(age/60)} min ago)")
        else:
            print(f"Next check: {check} (never run)")
    elif sys.argv[1] == "run":
        check = sys.argv[2] if len(sys.argv) > 2 else get_next_check()[0]
        mark_check_run(check)
        print(f"Marked {check} as run")
    elif sys.argv[1] == "list":
        state = load_state()
        now = datetime.now().timestamp()
        for check, last in state["lastChecks"].items():
            if last:
                mins = int((now - last) / 60)
                print(f"{check}: {mins} min ago")
            else:
                print(f"{check}: never")
