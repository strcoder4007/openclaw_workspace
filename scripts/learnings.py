#!/usr/bin/env python3
"""
Learnings manager - simple auto-logging
"""
import os
from datetime import datetime

LEARNINGS_FILE = os.path.expanduser("~/.openclaw/workspace/memory/learnings.md")

def add_learning(what_learned, category="general"):
    """Append a learning to the file"""
    entry = f"- {datetime.now().strftime('%Y-%m-%d %H:%M')}: {what_learned}\n"
    
    # Check if file exists and has content
    if os.path.exists(LEARNINGS_FILE):
        with open(LEARNINGS_FILE, "r") as f:
            content = f.read()
        
        # Check if today's section exists
        today = datetime.now().strftime('%Y-%m-%d')
        if f"## {today}" in content:
            # Append to today's section
            lines = content.split("\n")
            insert_idx = None
            for i, line in enumerate(lines):
                if line.strip() == f"## {today}":
                    insert_idx = i + 1
                    break
            if insert_idx:
                lines.insert(insert_idx, entry)
                content = "\n".join(lines)
        else:
            # Add new section
            content += f"\n## {today}\n{entry}"
    else:
        content = f"# Learnings\n\n## {datetime.now().strftime('%Y-%m-%d')}\n{entry}"
    
    with open(LEARNINGS_FILE, "w") as f:
        f.write(content)
    
    print(f"Logged: {what_learned}")

def get_learnings():
    """Read all learnings"""
    if os.path.exists(LEARNINGS_FILE):
        with open(LEARNINGS_FILE, "r") as f:
            return f.read()
    return ""

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(get_learnings())
    else:
        add_learning(" ".join(sys.argv[1:]))
