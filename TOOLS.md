# TOOLS.md - Operational Notes

_Runtime environment details. Changes frequently._

---

## Projects Directory
- Main path: `/Users/str/Projects`
- Datahat path: `/Users/str/Datahat`

## Tech Stack (Current)

- **Python:** venv `.venv` or `venv` in each project
- **Node.js:** nvm (`~/.nvm/versions/node/`)
- **Package Manager:** pnpm (global)

## API Keys / Environment

- OpenAI API: configured
- MiniMax OAuth: configured
- Google Gemini: available

## Telegram

- Bot: @AI_Engineer_str4007_bot
- Chat ID: 6695264047
- Send screenshot: `bash ~/scripts/telegram-screenshot.sh`
- Screenshot preference: Browser window only (Google Chrome --mode window)
- Screenshot tool: `skills/screenshot-telegram` (captures Chrome window + sends to Telegram)

## Installed Skills

- `python` — Python development
- `github` — GitHub CLI
- `docker` — Docker management
- `skills-search` — skills.sh search
- `gemini-cli` — Gemini CLI for coding tasks
- `llm-supervisor` — Rate limit handling with Ollama fallback
- `memory-keeper` — Memory checkpointing and session persistence
- `agent-autonomy-kit` — Agent autonomy and self-direction
- `agent-guardrails` — Anti-looping and task boundary guardrails
- `job-search` — Job hunting and application tracking
- `youtube` — YouTube video search and details
- `youtube-watcher` — YouTube transcript fetching
- `summarize` — URL/file summarization
- `humanizer` — Remove AI writing patterns
- `mcp-skill` — MCP server tools
- `linkedin-profile-crawler` — LinkedIn profile data
- `screenshot-telegram` — Capture and send screenshots to Telegram
- `peekaboo-screenshot` — macOS UI capture
- `openclaw-browser-use` — Browser automation

---

_Note: Detailed project info should stay in USER.md or separate project docs. This file is for environment-specific tooling notes._
