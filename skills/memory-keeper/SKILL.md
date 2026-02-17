---
name: memory-keeper
description: Memory checkpointing, active task management, and session persistence
version: 1.0.0
metadata:
  openclaw:
    emoji: "💾"
    category: memory
---

# Memory Keeper 💾

Session memory dies on compaction. Save everything to files.

---

## Core Rule

> **If it's not saved to a file, it's gone.**

Your context window compresses. Sessions reset. Only files persist.

---

## File Types

| File | Purpose | When to Update |
|------|---------|----------------|
| `MEMORY.md` | Long-term facts, preferences, verified info | Weekly review |
| `memory/YYYY-MM-DD.md` | Daily logs, work done, decisions | End of session |
| `ACTIVE-TASK.md` | Current multi-step task progress | Every subtask |

---

## Daily Memory (memory/YYYY-MM-DD.md)

### What to Log

- Tasks started and completed
- Key decisions made (with rationale)
- Commands run and their output
- Errors encountered and how resolved
- Anything you'd want to remember next session

### Format

```markdown
# 2026-02-18

## Work Done
- [HH:MM] Task: description

## Decisions
- Chose approach X over Y because: [reason]

## Commands
- `command` → output summary

## Pending
- Task to continue

## Notes
- Something interesting learned
```

---

## Active Task (ACTIVE-TASK.md)

### For Multi-Step Tasks Only

Create when task has >1 step AND will take >10 min.

### Template

```markdown
# Active Task: [Title]

## Goal
[What we're trying to achieve]

## Steps
- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## Progress
- [2026-02-18 02:30] Started step 1
- [2026-02-18 02:45] Step 1 done, output: X

## Blockers
- None / Waiting on: Y

## Next Step
Step 2: [description]
```

---

## Checkpoint Rules

### When to Checkpoint

1. **Before** any pause >5 min
2. **After** each subtask completion
3. **Before** compaction (/compact)
4. **Before** answering a question (check if work pending)
5. **When** switching between different tasks

### What to Save

- Current progress (% complete)
- What just finished
- What's next
- Any outputs needed for next step
- Files that were modified

### Never Forget

- Running experiments? Save params + results to file
- Found a bug? Document it before context clears
- Made a decision? Write the why, not just the what

---

## Memory Retrieval

### Before Starting New Work

1. Read `memory/YYYY-MM-DD.md` (recent days)
2. Check `ACTIVE-TASK.md` for pending work
3. Scan `MEMORY.md` for relevant context

### Session Start Checklist

- [ ] Read today's memory file
- [ ] Read yesterday's memory file
- [ ] Check ACTIVE-TASK.md
- [ ] Check MEMORY.md if main session

---

## Usage

### Commands

No commands — this runs automatically.

### Trigger Phrases

- "this will take a while" → create ACTIVE-TASK.md
- "let me continue" → read ACTIVE-TASK.md first
- "compacting" → save full summary first
- "reset" → ensure all progress saved

---

## Anti-Patterns

**Don't:**
- Keep mental notes ("I'll remember this")
- Assume session won't reset
- Skip logging "boring" steps
- Answer without checking pending work first

**Do:**
- Write everything down
- Check ACTIVE-TASK.md before continuing
- Summarize after each significant step
- Save before context clears

