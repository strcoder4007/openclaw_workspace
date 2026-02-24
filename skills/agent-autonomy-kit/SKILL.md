---
name: agent-autonomy-kit
version: 1.0.0
description: Stop waiting for prompts. Keep working. Includes parallel agent dispatch, plan execution, and subagent-driven development.
homepage: https://github.com/itskai-dev/agent-autonomy-kit
metadata:
  openclaw:
    emoji: "🚀"
    category: productivity
---

# Agent Autonomy Kit

Transform your agent from reactive to proactive.

## Quick Start

1. Create `tasks/QUEUE.md` with Ready/In Progress/Blocked/Done sections
2. Update `HEARTBEAT.md` to pull from queue and do work
3. Set up cron jobs for overnight work and daily reports
4. Watch work happen without prompting

## Key Concepts

- **Task Queue** — Always have work ready
- **Proactive Heartbeat** — Do work, don't just check
- **Continuous Operation** — Work until limits hit

See README.md for full documentation.

---

## Dispatching Parallel Agents

> Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies.

### When to Use

**Use when:**
- 3+ test files failing with different root causes
- Multiple subsystems broken independently
- Each problem can be understood without context from others

**Don't use when:**
- Failures are related (fix one might fix others)
- Need to understand full system state
- Agents would interfere with each other

### The Pattern

1. **Identify Independent Domains** — Group failures by what's broken
2. **Create Focused Agent Tasks** — Each agent gets specific scope, clear goal, constraints
3. **Dispatch in Parallel** — Multiple agents work simultaneously
4. **Review and Integrate** — Read summaries, verify fixes don't conflict

### Agent Prompt Structure

Good agent prompts are:
1. **Focused** — One clear problem domain
2. **Self-contained** — All context needed to understand the problem
3. **Specific about output** — What should the agent return?

---

## Executing Plans

> Use when you have a written implementation plan to execute.

### The Process

**Step 1: Load and Review Plan**
1. Read plan file
2. Review critically — identify questions or concerns
3. If concerns: Raise before starting

**Step 2: Execute Batch**
Default: First 3 tasks
- Mark each as in_progress
- Follow each step exactly
- Run verifications as specified
- Mark as completed

**Step 3: Report**
When batch complete:
- Show what was implemented
- Show verification output
- Say: "Ready for feedback."

**Step 4: Continue**
Based on feedback:
- Apply changes if needed
- Execute next batch
- Repeat until complete

**Step 5: Complete Development**
After all tasks verified:
- Use finishing-a-development-branch skill
- Follow that skill to verify tests, present options, execute choice

### Integration

**Required workflow skills:**
- **using-git-worktrees** — Set up isolated workspace before starting
- **finishing-a-development-branch** — Complete development after all tasks

---

## Subagent-Driven Development

> Use when executing implementation plans with independent tasks in the current session.

### vs. Executing Plans (Parallel Session)

- Same session (no context switch)
- Fresh subagent per task (no context pollution)
- Two-stage review after each task: spec compliance first, then code quality
- Faster iteration (no human-in-loop between tasks)

### The Process

1. **Read plan** — Extract all tasks with full text, note context
2. **Per Task:**
   - Dispatch implementer subagent with full task text + context
   - Implementer works, commits, self-reviews
   - Dispatch spec reviewer subagent (confirm code matches spec)
   - Dispatch code quality reviewer subagent
   - Mark task complete
3. **After all tasks** — Dispatch final code reviewer
4. **Complete** — Use finishing-a-development-branch

### Required Workflow Skills

- **using-git-worktrees** — REQUIRED: Set up isolated workspace before starting
- **writing-plans** — Creates the plan this skill executes
- **requesting-code-review** — Code review for reviewer subagents
- **finishing-a-development-branch** — Complete development after all tasks
- **test-driven-development** — Subagents follow TDD for each task

### Red Flags

**Never:**
- Start implementation on main/master branch without explicit consent
- Skip reviews (spec compliance OR code quality)
- Proceed with unfixed issues
- Dispatch multiple implementation subagents in parallel
- Start code quality review before spec compliance is approved
