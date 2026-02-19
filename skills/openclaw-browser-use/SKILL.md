---
name: browser-cli
description: OpenClaw browser control via CLI. Use when managing browser tabs, snapshots, screenshots, navigation, clicks, or typing. Supports two profiles: 'openclaw' (isolated managed browser) and 'chrome' (system browser profile). Commands: openclaw browser tabs, open, close, focus, snapshot, screenshot, navigate, click, type. Configure in ~/.openclaw/openclaw.json.
---

# Browser CLI

Manage OpenClaw's browser control server and run browser actions.

## Profiles

| Profile | Description |
|---------|-------------|
| `openclaw` | Managed, isolated Chrome/Brave/Edge (no extension required) |
| `chrome` | System browser profile (uses the system Chrome/Chromium user data) |

**Default:** `chrome`. Use `--browser-profile openclaw` for managed mode.

## Quick Start

```bash
# Check status
openclaw browser --browser-profile openclaw status

# Start managed browser
openclaw browser --browser-profile openclaw start

# Open a URL
openclaw browser --browser-profile openclaw open https://example.com

# Get page snapshot
openclaw browser --browser-profile openclaw snapshot
```

## Tabs Management

```bash
# List all tabs
openclaw browser tabs

# Open new tab
openclaw browser open https://docs.openclaw.ai

# Focus tab
openclaw browser focus <targetId>

# Close tab
openclaw browser close <targetId>
```

## Snapshot & Screenshot

```bash
# Get page snapshot (DOM structure)
openclaw browser snapshot

# Full-page screenshot
openclaw browser screenshot

# Screenshot with custom options
openclaw browser screenshot --full-page
openclaw browser screenshot --type jpeg --quality 80
```

## Actions (UI Automation)

```bash
# Navigate to URL
openclaw browser navigate https://example.com

# Click element (by ref)
openclaw browser click <ref>

# Type into element (by ref)
openclaw browser type <ref> "hello world"

# Other actions: hover, drag, select, fill, press
openclaw browser hover <ref>
openclaw browser press <ref> Enter
```

## Profile Management

```bash
# List profiles
openclaw browser profiles

# Create new profile
openclaw browser create-profile --name work --color "#FF5A36"

# Delete profile
openclaw browser delete-profile --name work
```

## Common Flags

| Flag | Description |
|------|-------------|
| `--browser-profile <name>` | Choose profile (default from config) |
| `--url <wsUrl>` | Gateway WebSocket URL |
| `--token <token>` | Gateway token |
| `--timeout <ms>` | Request timeout |
| `--json` | Machine-readable output |

## Configuration

Edit `~/.openclaw/openclaw.json`:

```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "chrome",
    "headless": false,
    "profiles": {
      "openclaw": {
        "cdpPort": 18800,
        "color": "#FF4500"
      },
      "work": {
        "cdpPort": 18801,
        "color": "#0066CC"
      }
    }
  }
}
```

**Notes:**
- Set `defaultProfile: "openclaw"` for managed browser by default
- Browser service binds to loopback on port derived from gateway.port
- Use `attachOnly: true` to only attach to running browsers (never launch)
