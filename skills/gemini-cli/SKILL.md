---
name: gemini-cli
description: Use Gemini CLI for one-shot coding or Q&A tasks. Spawns gemini in a PTY for interactive output.
metadata:
  {
    "openclaw": { "emoji": "♊️", "slashCommand": "gemini" },
  }
---

# Gemini CLI Skill

Use Gemini CLI for coding tasks, Q&A, or generation.

## Usage

```bash
# One-shot prompt (uses gemini-3.1-pro-preview by default)
gemini "Your prompt here"

# With specific model
gemini -m gemini-2.5-flash "Your prompt"

# With approval mode
gemini --approval-mode yolo "Build me a file"
```

## How to Invoke

When user types `/gemini <prompt>`:

1. Run via bash with PTY:
   ```bash
   bash pty:true command:"gemini -m gemini-3.1-pro-preview -p '<prompt>'"
   ```

2. For longer tasks, use background:
   ```bash
   bash pty:true background:true command:"gemini -m gemini-3.1-pro-preview -p '<prompt>'"
   ```

## Notes

- Requires `GEMINI_API_KEY` env var (already set in ~/.zshrc)
- Use `-p` for non-interactive (headless) mode
- `--approval-mode yolo` auto-approves all actions
- Default model is **gemini-3.1-pro-preview**
