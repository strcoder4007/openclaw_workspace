# MEMORY.md - Curated Durable Facts

_Small, structured. Verified facts only. Review regularly._

---

## Environment

| Fact | Value | Source | Last Validated | Expires |
|------|-------|--------|----------------|---------|
| Host OS | Darwin 25.3.0 (arm64) | runtime | 2026-02-18 | Never |
| Node | v22.17.0 | runtime | 2026-02-18 | Never |
| Shell | zsh | runtime | 2026-02-18 | Never |
| Projects Dir | /Users/str/Projects | TOOLS.md | 2026-02-18 | Never |
| Timezone | Asia/Calcutta | system | 2026-02-18 | Never |

## Configured Models (Active)

| Role | Model | Provider | Source | Last Validated |
|------|-------|----------|--------|----------------|
| **Primary** | MiniMax M2.5 | minimax-portal | config | 2026-02-20 |
| **Heartbeat** | Gemini 3 Pro Preview | google-gemini-cli | config | 2026-02-20 |
| **Fallback** | MiniMax M2.1 | minimax-portal | config | 2026-02-20 |
| **Available** | GPT-5 Mini | openai | config | 2026-02-20 |

## User Preferences

| Preference | Value | Source | Last Validated | Expires |
|------------|-------|--------|----------------|---------|
| News Requests | Minimum 10 items, detailed with short sentence summary | str4007 | 2026-02-19 | Never |
| Web Search | Use web_fetch + Serper API (SERPER_API_KEY) or SerpAPI (SERP_API_KEY) for web search | str4007 | 2026-02-20 | Never |
| Measurement System | Metric (kg, km, cm, etc.) | str4007 | 2026-02-20 | Never |
| Currency | Indian Rupees (₹) | str4007 | 2026-02-20 | Never |

## Infrastructure Keys

| Service | Status | Source | Last Validated |
|---------|--------|--------|----------------|
| OpenAI | Configured | config | 2026-02-20 |
| MiniMax | Configured | config | 2026-02-20 |
| Google/Gemini | Configured | config | 2026-02-20 |
| DeepSeek | Key Present | config | 2026-02-20 |
| OpenRouter | Key Present | config | 2026-02-20 |
| Groq | Key Present | config | 2026-02-20 |
| ElevenLabs | Key Present | config | 2026-02-20 |

## Constraints

- Session idle timeout: 30 minutes
- Always verify before executing external actions

---

_Review this file periodically. Remove expired entries. Keep it small._
