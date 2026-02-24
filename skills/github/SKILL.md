---
name: github
description: "Interact with GitHub using the `gh` CLI. Use `gh issue`, `gh pr`, `gh run`, and `gh api` for issues, PRs, CI runs, and advanced queries. Includes git worktrees, code review, and branch management."
---

# GitHub Skill

Use the `gh` CLI to interact with GitHub. Always specify `--repo owner/repo` when not in a git directory, or use URLs directly.

## Pull Requests

Check CI status on a PR:
```bash
gh pr checks 55 --repo owner/repo
```

List recent workflow runs:
```bash
gh run list --repo owner/repo --limit 10
```

View a run and see which steps failed:
```bash
gh run view <run-id> --repo owner/repo
```

View logs for failed steps only:
```bash
gh run view <run-id> --repo owner/repo --log-failed
```

## API for Advanced Queries

The `gh api` command is useful for accessing data not available through other subcommands.

Get PR with specific fields:
```bash
gh api repos/owner/repo/pulls/55 --jq '.title, .state, .user.login'
```

## JSON Output

Most commands support `--json` for structured output.  You can use `--jq` to filter:

```bash
gh issue list --repo owner/repo --json number,title --jq '.[] | "\(.number): \(.title)"'
```

---

## Using Git Worktrees

> Use when starting feature work that needs isolation from current workspace.

### Directory Selection

Follow this priority order:

1. **Check existing directories:**
   ```bash
   ls -d .worktrees 2>/dev/null || ls -d worktrees 2>/dev/null
   ```

2. **Check CLAUDE.md for preference**

3. **Ask user** if neither exists

### Safety Verification (Project-Local)

**MUST verify directory is ignored before creating worktree:**

```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

If NOT ignored: Add to .gitignore and commit first.

### Creation Steps

```bash
# Detect project name
project=$(basename "$(git rev-parse --show-toplevel)")

# Create worktree with new branch
git worktree add "$path" -b "$BRANCH_NAME"

# Run project setup
npm install  # or pip install, cargo build, etc.

# Verify baseline
npm test  # or pytest, cargo test, etc.
```

---

## Finishing a Development Branch

> Use when implementation is complete, all tests pass, and you need to decide how to integrate work.

### Step 1: Verify Tests

```bash
# Run project's test suite
npm test  # or pytest, cargo test, go test ./...
```

If tests fail: Fix before proceeding.

### Step 2: Determine Base Branch

```bash
git merge-base HEAD main  # or master
```

### Step 3: Present Options

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

### Step 4: Execute Choice

**Option 1: Merge Locally**
```bash
git checkout <base-branch>
git pull
git merge <feature-branch>
# Verify tests on merged result
git branch -d <feature-branch>
```

**Option 2: Push and Create PR**
```bash
git push -u origin <feature-branch>
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

**Option 4: Discard** (confirm first with "Type 'discard' to confirm")

### Step 5: Cleanup Worktree

```bash
git worktree list | grep $(git branch --show-current)
git worktree remove <worktree-path>
```

---

## Receiving Code Review

> Use when receiving code review feedback, before implementing suggestions.

### The Response Pattern

```
1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words (or ask)
3. VERIFY: Check against codebase reality
4. EVALUATE: Technically sound for THIS codebase?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, test each
```

### Forbidden Responses

**NEVER:**
- "You're absolutely right!" (performative)
- "Great point!" / "Excellent feedback!"
- "Let me implement that now" (before verification)

**INSTEAD:**
- Restate the technical requirement
- Ask clarifying questions
- Push back with technical reasoning if wrong
- Just start working

### Handling Unclear Feedback

```
IF any item is unclear:
  STOP - do not implement anything yet
  ASK for clarification on unclear items
```

### When To Push Back

Push back when:
- Suggestion breaks existing functionality
- Reviewer lacks full context
- Violates YAGNI (unused feature)
- Technically incorrect for this stack

### Acknowledging Correct Feedback

```
✅ "Fixed. [Brief description of what changed]"
✅ "Good catch - [specific issue]. Fixed in [location]."

❌ "You're absolutely right!"
❌ "Thanks for catching that!"
```

---

## Requesting Code Review

> Use when completing tasks, implementing major features, or before merging.

### When to Request Review

**Mandatory:**
- After each task in subagent-driven development
- After completing major feature
- Before merge to main

### How to Request

```bash
# Get git SHAs
BASE_SHA=$(git rev-parse HEAD~1)
HEAD_SHA=$(git rev-parse HEAD)
```

Dispatch code review subagent with:
- What was implemented
- Plan or requirements
- BASE_SHA and HEAD_SHA
- Brief summary

### Act on Feedback

- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong (with reasoning)
