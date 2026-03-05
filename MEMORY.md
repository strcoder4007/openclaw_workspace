# MEMORY.md - Curated Durable Facts

_Small, structured. Verified facts only. Review regularly._

---

## Configured Models (Active)
_Last Reviewed: 2026-03-06_

| Role | Model | Provider | Source | Last Validated |
|------|-------|----------|--------|----------------|
| **Primary** | MiniMax M2.5 | minimax | config | 2026-02-20 |
| **Heartbeat** | MiniMax M2.5 | minimax-portal | config | 2026-02-20 |
| **Fallback** | Gemini 3.1 Pro Preview | google-gemini-cli | config | 2026-02-20 |
| **Available** | GPT-5 Mini | openai | config | 2026-02-20 |

## User Preferences
_Last Reviewed: 2026-03-06_

| Preference | Value | Source | Last Validated | Expires |
|------------|-------|--------|----------------|---------|
| News Requests | Minimum 10 items, detailed with short sentence summary | str4007 | 2026-02-19 | Never |
| Web Search | Use web_fetch + Serper API (SERPER_API_KEY) or SerpAPI (SERP_API_KEY) for web search | str4007 | 2026-02-20 | Never |
| Measurement System | Metric (kg, km, cm, etc.) | str4007 | 2026-02-20 | Never |
| Currency | Indian Rupees (₹) | str4007 | 2026-02-20 | Never |

## Infrastructure Keys
_Last Reviewed: 2026-03-06_

| Service | Status | Source | Last Validated |
|---------|--------|--------|----------------|
| OpenAI | Configured | config | 2026-02-20 |
| MiniMax | Configured | config | 2026-02-20 |
| Google/Gemini | Configured | config | 2026-02-20 |
| DeepSeek | Key Present | config | 2026-02-20 |
| OpenRouter | Key Present | config | 2026-02-20 |
| Groq | Key Present | config | 2026-02-20 |
| ElevenLabs | Key Present | config | 2026-02-20 |

## Persistent Instructions
_Last Reviewed: 2026-03-06_

- Session idle timeout: 30 minutes
- Always verify before executing external actions
- **NEVER use em dashes (—) in any writing** — replace with commas, periods, or rewrite the sentence
- When asked about BMW Z4 OLX Analysis or BMW price/best deals, analyze 2015-2018 BMW Z4 e89 listings on OLX India https://www.olx.in/en-in/items/q-bmw-z4?isSearchCall=true

## 🔍 To Verify
_Things that need confirmation_

- [ ] All model configs above need re-validation (Last Validated Feb 20, now Mar 6)
- [ ] Verify DeepSeek, OpenRouter, Groq keys are still working
- [ ] Check if GPT-5 Mini is still available

## Self-Improvement
_Last Reviewed: 2026-03-06_

See AGENTS.md. Simple format in `memory/learnings.md` — just date + what I learned.

---

_Review this file quarterly. Update review dates when making changes. Move verified facts here from daily memory._
