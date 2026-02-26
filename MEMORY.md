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

## Constraints

- Session idle timeout: 30 minutes
- Always verify before executing external actions
- **NEVER use em dashes (—) in any writing** — replace with commas, periods, or rewrite the sentence

## Self-Improvement Skill

### Log Formats

**Learning Entry** (LEARNINGS.md):
```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending | resolved | promoted

### Summary
One-line description

### Details
Full context: what happened, what was wrong, what's correct

### Metadata
- Source: conversation | error | user_feedback
- See Also: LRN-20250110-001
```

**Error Entry** (ERRORS.md):
```markdown
## [ERR-YYYYMMDD-XXX] command_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending

### Summary
Brief description

### Error
```
Actual error message
```

### Context
What was attempted

### Suggested Fix
How to resolve
```

### Detection Triggers

**Corrections** → learning (correction):
- "No, that's not right..."
- "Actually, it should be..."
- "You're wrong about..."

**Feature Requests** → feature request:
- "Can you also..."
- "I wish you could..."

**Knowledge Gaps** → learning (knowledge_gap):
- User provides new information
- Documentation is outdated

**Errors** → error entry:
- Non-zero exit code
- Exception or stack trace
- Unexpected output

### Promotion Criteria

Promote when:
- Applies across multiple files/features
- Prevents recurring mistakes
- Documents project conventions

### ID Format

- `LRN-YYYYMMDD-XXX` - Learning
- `ERR-YYYYMMDD-XXX` - Error
- `FEAT-YYYYMMDD-XXX` - Feature Request

---

_Review this file periodically. Remove expired entries. Keep it small._
