#!/usr/bin/env bash
# OpenClaw nightly update script - commits workspace, checks for updates, updates if needed
# Runs at 11:55 PM daily via cron

set -e

SCRIPT_DIR="/Users/str/.openclaw/workspace/scripts"
WORKSPACE_DIR="/Users/str/.openclaw/workspace"
LOG_FILE="$SCRIPT_DIR/openclaw-nightly.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

cd "$WORKSPACE_DIR"

log "=== Starting nightly update ==="

# Step 1: Commit workspace changes
log "Checking for workspace changes..."
if [[ -n $(git status --porcelain 2>/dev/null) ]]; then
    git add -A
    git commit -m "Nightly commit $(date '+%Y-%m-%d %H:%M:%S')"
    log "Workspace committed"
else
    log "No changes to commit"
fi

# Step 2: Check for OpenClaw updates
log "Checking for OpenClaw updates..."
CURRENT_VERSION=$(openclaw --version 2>/dev/null || npm list -g openclaw 2>/dev/null | grep openclaw | head -1 || echo "unknown")

# Get latest version from npm
LATEST_VERSION=$(npm view openclaw version 2>/dev/null || echo "unknown")

log "Current: $CURRENT_VERSION | Latest: $LATEST_VERSION"

# Compare versions
if [[ "$CURRENT_VERSION" != "$LATEST_VERSION" && "$LATEST_VERSION" != "unknown" ]]; then
    log "Update available! Updating OpenClaw..."
    
    # Update OpenClaw
    npm update -g openclaw 2>&1 | tee -a "$LOG_FILE"
    
    log "Restarting OpenClaw..."
    openclaw gateway restart
    
    log "=== Update complete ==="
else
    log "OpenClaw is up to date"
    log "=== Nightly done ==="
fi
