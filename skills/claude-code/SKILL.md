---
name: claude-code
description: Use Claude Code (with MiniMax M2.5) for coding tasks. Spawns claude in a PTY for interactive output.
---

# Claude Code Skill

Use Claude Code (configured with MiniMax M2.5) for coding tasks.

## Configuration

Claude Code is configured with MiniMax M2.5 via `~/.claude/settings.json`:
- ANTHROPIC_BASE_URL: https://api.minimax.io/anthropic
- ANTHROPIC_AUTH_TOKEN: your MiniMax API key
- Default model: MiniMax-M2.5

## Usage

### Basic Commands

```bash
# One-shot prompt (headless mode)
claude -p "Your prompt here"

# With auto-approval (no prompts)
claude -p --approval-mode=full-auto "Build me a REST API"

# Skip permission prompts entirely
claude -p --dangerously-skip-permissions "Delete all .tmp files"

# Specify working directory
claude -p --dangerously-skip-permissions -C ~/Projects/myapp "Fix the login bug"
```

### Slash Commands

In interactive mode (claude without -p):
- `/usage` - Check rate limits and usage
- `/stats` - View usage statistics with activity graph
- `/chrome` - Toggle browser integration
- `/mcp` - Manage MCP servers
- `/clear` - Clear conversation and start fresh

### Advanced

```bash
# Resume a session
claude -r

# With specific model
claude -m MiniMax-M2.5 -p "Your task"

# Read from file
claude -p "$(cat prompt.txt)"

# Pipe input
echo "Fix the bug" | claude -p -
```

## Invocation Patterns

### From OpenClaw (PTY required)

```bash
# Simple one-shot
bash pty:true command:"claude -p 'Build a todo app in React'"

# With auto-approval
bash pty:true command:"claude -p --dangerously-skip-permissions 'Add auth to the API'"

# Specific project
bash pty:true workdir:~/Projects/myapp command:"claude -p --dangerously-skip-permissions 'Refactor the auth module'"

# Background task
bash pty:true background:true workdir:~/Projects/myapp command:"claude -p --dangerously-skip-permissions 'Build a full CRUD API'"
```

## Best Practices

1. **Break down big tasks** - Instead of "Build an entire app", do "Create the project structure", then "Add authentication", then "Add CRUD"

2. **Use auto-approval** - For batch tasks, use `--dangerously-skip-permissions` to avoid prompts

3. **Check /usage** - Monitor your MiniMax credits usage

4. **Use CLAUDE.md** - Create a `CLAUDE.md` file in project root with project-specific instructions

5. **Workdir matters** - Always set `workdir:` to scope Claude to the right project

## Fallback

If Claude Code fails, try gemini-cli:
```bash
bash pty:true command:"gemini -m gemini-3.1-pro-preview 'Your prompt'"
```
