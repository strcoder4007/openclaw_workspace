# Screenshot to Telegram

## Purpose
Capture a screenshot of a local development project running in Google Chrome and send it to the user's Telegram.

## Chat ID
- Telegram Chat ID: **6695264047** (from TOOLS.md)
- Bot: @COO_str4007_bot

## Workflow

### Step 1: Open project in Chrome (if needed)
If the project isn't already open in Chrome:
```bash
open -a "Google Chrome" http://localhost:5173/easynews/
```

Or navigate to the correct localhost URL for the project.

### Step 2: Capture browser window screenshot
```bash
peekaboo image --app "Google Chrome" --window-title "EASYNEWS" --path /tmp/screenshot.png --retina
```

To find the correct window title:
```bash
peekaboo list windows --app "Google Chrome" --json
```

### Step 3: Send to Telegram
```bash
curl -s -X POST "https://api.telegram.org/bot8260347392:AAEYuu0HVdMKfYGIA7iUgmUwUdKlihJ9a3g/sendPhoto" \
  -F "chat_id=6695264047" \
  -F "photo=@/tmp/screenshot.png" \
  -F "caption=Screenshot from <project-name>"
```

## Usage

When user asks for a screenshot:
1. Determine the correct localhost URL for their project
2. Open it in Chrome if not already running
3. Capture the browser window with peekaboo
4. Send to Telegram using the chat ID

## Notes

- Always use **Google Chrome** (not Arc)
- Target the specific browser window by title or use `--mode window`
- Use `--retina` for high-res screenshots
- Chat ID is stored in TOOLS.md as reference
