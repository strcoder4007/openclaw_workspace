# HEARTBEAT.md

## Check Rotation

Use `heartbeat-state.py` to track and rotate checks fairly:
```bash
python3 /Users/str/.openclaw/workspace/scripts/heartbeat-state.py  # Get next check
python3 /Users/str/.openclaw/workspace/scripts/heartbeat-state.py run <check>  # Mark done
```

Checks to rotate through: email, teams, calendar, weather

## Checks

### Email
- Run: `gog gmail search "is:unread" --max 5`
- Flag urgent emails

### Teams
- Browser required (Chrome extension must be attached)
- Check Activity section for @mentions

### Calendar
- Run: `gog calendar events primary --upcoming 24h`
- Flag events in next 24h

### Weather
- Run: `curl wttr.in` or check weather skill
- Relevant if human might go out
