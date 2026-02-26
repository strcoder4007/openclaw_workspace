# MEMORY.md - Curated Durable Facts

_Small, structured. Verified facts only. Review regularly._

---

## Configured Models (Active)

| Role | Model | Provider | Source | Last Validated |
|------|-------|----------|--------|----------------|
| **Primary** | MiniMax M2.5 | minimax | config | 2026-02-20 |
| **Heartbeat** | MiniMax M2.5 | minimax-portal | config | 2026-02-20 |
| **Fallback** | Gemini 3.1 Pro Preview | google-gemini-cli | config | 2026-02-20 |
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

Whenever I ask about BMW Z4 OLX Analysis or BMW price/best deals, analyze 2015-2018 BMW Z4 e89 listings on OLX India https://www.olx.in/en-in/items/q-bmw-z4?isSearchCall=true

## Constraints

- Session idle timeout: 30 minutes
- Always verify before executing external actions
- **NEVER use em dashes (—) in any writing** — replace with commas, periods, or rewrite the sentence

## Self-Improvement

See AGENTS.md. Simple format in `memory/learnings.md` — just date + what I learned.

---

_Review this file periodically. Remove expired entries. Keep it small._
