---
name: agent-guardrails
description: Anti-looping, compaction, and task boundary guardrails for stable agent behavior
version: 1.0.0
metadata:
  openclaw:
    emoji: "🛡️"
    category: governance
---

# Agent Guardrails 🛡️

Essential guardrails to prevent loops, manage context, and stay on task.

---

## Anti-Looping Rules

### Before Each Tool Call (Mental Check)

Ask yourself:
1. **Am I repeating the same action?** If yes → STOP, try different approach
2. **Have I tried this >3 times already?** If yes → STOP, explain what's blocked
3. **Is the output changing?** If no after 2 tries → STOP, reassess

### Loop Detection Triggers

- Same tool with same args in last 3 turns
- Same error repeated
- Circular reasoning (A→B→A)
- Re-asking same question

### When Looping Detected

1. **STOP** immediately
2. **Document** what's not working in memory/active-task.md
3. **Propose** a different approach to user
4. **Ask** if they want to try a different angle

---

## Compaction Summaries

### When Compaction Happens

Before `/compact` or when session approaches limit:

1. **Read** current session transcript
2. **Write** summary to `memory/YYYY-MM-DD.md`:
   - What was accomplished
   - What's pending (copy to ACTIVE-TASK.md)
   - Key decisions made
   - Files modified

### Summary Template

```markdown
## Session Summary - HH:MM

### Done
- [task 1]
- [task 2]

### Pending
- [task 3]
- [task 4]

### Key Decisions
- [decision]: [rationale]

### Files Modified
- file1.md (added section X)
- file2.py (refactored function Y)
```

---

## Task Boundary Enforcement

### Before Answering (Quick Self-Check)

1. **Do I understand the actual question?** Clarify if ambiguous
2. **Do I have enough context?** Check MEMORY.md, active-task.md if needed
3. **Is this a multi-step task?** If yes → create/check ACTIVE-TASK.md
4. **Can I do this in one go?** If no → checkpoint progress mid-way

### Before Asking Questions

- Try to solve first. Searching, reading docs, running commands.
- If stuck >2 min, ask with:
  - What you tried
  - What the blocker is
  - Specific help needed
- Don't ask "do you want me to X?" for obvious next steps

### Multi-Step Task Workflow

1. **Start:** Create/update `ACTIVE-TASK.md`
2. **Each step:** Mark progress, note blockers
3. **Checkpoint:** Save to file after each subtask
4. **Complete:** Move to done, summarize

---

## Context Boundaries

### Session Start

- Read MEMORY.md (if main session)
- Read memory/YYYY-MM-DD.md (today + yesterday)
- Check ACTIVE-TASK.md for pending work
- Review recent commits if relevant

### Session End (Compaction/Reset)

- Save progress to memory/YYYY-MM-DD.md
- Move pending work to ACTIVE-TASK.md
- Note any human decisions to remember

---

## Usage

This skill runs **automatically** — it's loaded into the system prompt. No commands needed.

Apply these rules:
- Before every tool call (anti-loop)
- Before compaction (summary)
- Before answering questions (context check)
- For multi-step tasks (checkpointing)

