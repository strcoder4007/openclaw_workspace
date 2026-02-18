# Peekaboo Screenshot Agent

## Purpose
Take screenshots of the screen, specific windows, or applications using Peekaboo and deliver them to the user in the chat.

## Workflow

### Step 1: Capture the screenshot
```bash
peekaboo see --mode screen --path /tmp/screenshot.png
```

If you want to capture a specific app/window:
```bash
# Capture specific app (e.g., Arc browser)
peekaboo see --app Arc --mode window --path /tmp/screenshot.png

# Capture frontmost window
peekaboo see --mode frontmost --path /tmp/screenshot.png

# Capture menu bar
peekaboo see --mode screen --menubar --path /tmp/screenshot.png
```

### Step 2: Verify the screenshot was saved
```bash
ls -la /tmp/screenshot.png
```

### Step 3: Read and display the image
Use the `read` tool to display the image:
```
read file_path=/tmp/screenshot.png
```

### Step 4: If image is broken/not displaying
Try these alternatives:

**Option A: Convert to JPEG**
```bash
sips -s format jpeg /tmp/screenshot.png --out /tmp/screenshot.jpg
```

**Option B: Use a different path**
```bash
# Save directly to workspace
peekaboo see --mode screen --path /Users/str/.openclaw/workspace/screenshot.png
```

**Option C: Check file integrity**
```bash
file /tmp/screenshot.png
head -c 20 /tmp/screenshot.png  # Should show PNG header
```

### Step 5: For Telegram delivery
If the user wants the image on Telegram:
- The image must be in a supported format (PNG, JPEG)
- Use the `message` tool with `media` parameter to send to Telegram

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Screen recording permission required" | User must enable in System Settings → Privacy & Security → Screen Recording |
| "Window not found" | App has no windows; use `--mode screen` instead |
| Image broken/not showing | Convert to JPEG: `sips -s format jpeg input.png --out output.jpg` |
| Permission errors | Check Accessibility permissions in System Settings |

## Example Response Format

After capturing, respond with:

```
📸 Screenshot captured!

[insert image using read tool]

Saved to: /tmp/screenshot.png
```

## Important Notes

- Always verify the file exists before claiming success
- If the image doesn't display in chat, convert to JPEG format
- Use `--mode screen` as fallback when specific app capture fails
- Peekaboo stores captures in /tmp by default unless --path specifies otherwise
