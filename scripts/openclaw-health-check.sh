#!/bin/bash

# OpenClaw Daily Health Check & Repair Script
# Run this daily to maintain OpenClaw health
# Can be run as cron job

# === CONFIG ===
LOG_DIR="$HOME/.openclaw/logs"
OPENCLAW_DIR="$HOME/.openclaw"
TELEGRAM_CHAT_ID="6695264047"
HEALTH_LOG="$LOG_DIR/health-check-$(date +%Y-%m-%d).log"

# === COLORS ===
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1" | tee -a "$HEALTH_LOG"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1" | tee -a "$HEALTH_LOG"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" | tee -a "$HEALTH_LOG"; }

# === INIT ===
echo "=== OpenClaw Health Check ===" | tee -a "$HEALTH_LOG"
echo "Date: $(date)" | tee -a "$HEALTH_LOG"
echo "" | tee -a "$HEALTH_LOG"

ISSUES=()
FIXES=()
ALERT_ITEMS=()

# === 1. GATEWAY CHECK ===
log_info "Checking Gateway..."
if curl -s -f --max-time 5 http://127.0.0.1:18789/health > /dev/null 2>&1; then
    log_info "Gateway running ✓"
else
    log_error "Gateway NOT responding!"
    ISSUES+=("Gateway not responding")
    
    # Try restart
    if command -v openclaw &> /dev/null; then
        log_info "Attempting restart..."
        openclaw gateway restart > /dev/null 2>&1 &
        sleep 8
        if curl -s -f --max-time 5 http://127.0.0.1:18789/health > /dev/null 2>&1; then
            log_info "Gateway restarted ✓"
            FIXES+=("Restarted gateway")
        else
            log_error "Restart failed"
            ALERT_ITEMS+=("Gateway won't start - check logs")
        fi
    fi
fi

# === 2. DISK CHECK ===
log_info "Checking disk..."
DISK_USAGE=$(df "$HOME" | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 90 ]; then
    log_error "Disk critical: ${DISK_USAGE}%"
    ISSUES+=("Disk at ${DISK_USAGE}%")
    ALERT_ITEMS+=("Disk space critical: ${DISK_USAGE}%")
elif [ "$DISK_USAGE" -gt 80 ]; then
    log_warn "Disk warning: ${DISK_USAGE}%"
    ISSUES+=("Disk at ${DISK_USAGE}%")
else
    log_info "Disk OK: ${DISK_USAGE}%"
fi

# === 3. MEMORY CHECK ===
log_info "Checking memory..."
MEMORY_LOG="$LOG_DIR/memory-history.log"

# Get current memory stats
if command -v vm_stat &> /dev/null; then
    # macOS - use top for easier memory reading
    MEM_INFO=$(top -l 1 -n 0 2>/dev/null | grep "PhysMem")
    if [ -n "$MEM_INFO" ]; then
        # Format: "PhysMem: 1234M used (123M wired), 1234M unused"
        USED_MEM=$(echo "$MEM_INFO" | awk '{print $2}')
        WIRED_MEM=$(echo "$MEM_INFO" | awk '{print $4}' | sed 's/,//')
        
        log_info "Memory: $MEM_INFO"
        
        # Extract just the number for history
        USED_GB=$(echo "$USED_MEM" | sed 's/[A-Za-z]//g')
        USED_UNIT=$(echo "$USED_MEM" | sed 's/[0-9.]//g')
        
        if [ "$USED_UNIT" = "G" ]; then
            USED_GB_INT=${USED_GB%.*}
        elif [ "$USED_UNIT" = "M" ]; then
            USED_GB_INT=0
        else
            USED_GB_INT=0
        fi
        
        # Store for comparison
        echo "$(date +%Y-%m-%d),${USED_GB_INT}GB" >> "$MEMORY_LOG"
        
        # Check for spike
        if [ -f "$MEMORY_LOG" ]; then
            YESTERDAY=$(tail -2 "$MEMORY_LOG" | head -1 | cut -d',' -f2 | sed 's/GB//')
            if [ -n "$YESTERDAY" ] && [ "$YESTERDAY" -gt 0 ] && [ "$USED_GB_INT" -gt $((YESTERDAY * 150 / 100)) ]; then
                log_warn "Memory spike: ${USED_GB_INT}GB (was ${YESTERDAY}GB yesterday)"
                ISSUES+=("Memory spike: ${USED_GB_INT}GB vs ${YESTERDAY}GB")
            fi
        fi
    fi
    
elif command -v free &> /dev/null; then
    # Linux
    TOTAL_MEM=$(free -g | grep Mem | awk '{print $2}')
    USED_MEM=$(free -g | grep Mem | awk '{print $3}')
    USED_PERCENT=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
    
    log_info "Memory: ${USED_MEM}GB / ${TOTAL_MEM}GB (${USED_PERCENT}%)"
fi

# Check Gateway process memory
GATEWAY_PID=$(pgrep -f "openclaw" | head -1)
if [ -n "$GATEWAY_PID" ]; then
    GATEWAY_MEM=$(ps -o rss= -p "$GATEWAY_PID" 2>/dev/null | awk '{print int($1/1024)}')
    log_info "Gateway: ${GATEWAY_MEM}MB (PID: $GATEWAY_PID)"
    
    # Alert if gateway using too much
    if [ "$GATEWAY_MEM" -gt 1000 ]; then
        log_warn "Gateway using ${GATEWAY_MEM}MB - high!"
        ISSUES+=("Gateway high memory: ${GATEWAY_MEM}MB")
    fi
else
    log_warn "Gateway process not found"
fi

# === 4. CONFIG VALIDITY ===
log_info "Checking config..."
if [ -f "$OPENCLAW_DIR/openclaw.json" ]; then
    if node -e "JSON.parse(require('fs').readFileSync('$OPENCLAW_DIR/openclaw.json'))" 2>/dev/null; then
        log_info "Config valid ✓"
    else
        log_error "Config INVALID!"
        ISSUES+=("Invalid JSON config")
        ALERT_ITEMS+=("Config file has invalid JSON")
    fi
else
    log_error "Config missing!"
    ISSUES+=("No config file")
    ALERT_ITEMS+=("Config file missing!")
fi

# === 5. LOG ERRORS ===
log_info "Checking logs..."
if [ -d "$OPENCLAW_DIR/logs" ]; then
    ERROR_LOGS=$(find "$OPENCLAW_DIR/logs" -name "*.log" -mtime -1 -exec grep -l "error\|Error\|FATAL\|CRITICAL" {} \; 2>/dev/null)
    ERROR_COUNT=$(echo "$ERROR_LOGS" | grep -v "^$" | wc -l)
    
    if [ "$ERROR_COUNT" -gt 0 ]; then
        log_warn "$ERROR_COUNT log files with errors"
        ISSUES+=("$ERROR_COUNT files with errors")
        
        # Extract recent errors (last 3 unique)
        RECENT_ERRORS=$(find "$OPENCLAW_DIR/logs" -name "*.log" -mtime -1 -exec grep -h "error\|Error" {} \; 2>/dev/null | tail -5 | sort -u)
        if [ -n "$RECENT_ERRORS" ]; then
            echo "$RECENT_ERRORS" | head -3 | while read line; do
                log_info "  Error: ${line:0:100}"
            done
        fi
    else
        log_info "No recent errors ✓"
    fi
fi

# === 6. SESSIONS ===
log_info "Checking sessions..."
if [ -d "$OPENCLAW_DIR/agents/default/sessions" ]; then
    SESSION_COUNT=$(find "$OPENCLAW_DIR/agents/default/sessions" -name "*.json" 2>/dev/null | wc -l)
    SESSION_SIZE=$(du -sm "$OPENCLAW_DIR/agents/default/sessions" 2>/dev/null | cut -f1)
    log_info "Sessions: $SESSION_COUNT files, ${SESSION_SIZE}MB"
    
    # Auto-prune if too large
    if [ "$SESSION_SIZE" -gt 500 ]; then
        log_warn "Sessions large - pruning old entries..."
        # Keep only last 50 sessions
        find "$OPENCLAW_DIR/agents/default/sessions" -name "*.json" -mtime +30 -delete 2>/dev/null
        FIXES+=("Pruned old sessions")
        log_info "Pruned old sessions"
    fi
fi

# === 7. CRON JOBS ===
log_info "Checking cron..."
if command -v openclaw &> /dev/null; then
    CRON_OUTPUT=$(openclaw cron list 2>&1)
    if echo "$CRON_OUTPUT" | grep -qE "error|Error|failed"; then
        log_error "Cron issue detected"
        ISSUES+=("Cron job listing failed")
    else
        # Check for failed runs
        FAILED_JOBS=$(echo "$CRON_OUTPUT" | grep -E "failed|error" || true)
        if [ -n "$FAILED_JOBS" ]; then
            log_warn "Some cron jobs may have failed"
            ISSUES+=("Cron job failures detected")
        else
            log_info "Cron jobs OK ✓"
        fi
    fi
fi

# === 8. CLEANUP ===
log_info "Cleaning up..."
# Old logs
OLD_LOGS=$(find "$OPENCLAW_DIR/logs" -name "*.log" -mtime +7 -type f 2>/dev/null | wc -l)
if [ "$OLD_LOGS" -gt 0 ]; then
    find "$OPENCLAW_DIR/logs" -name "*.log" -mtime +7 -type f -delete 2>/dev/null
    FIXES+=("Deleted $OLD_LOGS old logs")
    log_info "Cleaned $OLD_LOGS old logs"
fi

# === SUMMARY ===
echo "" | tee -a "$HEALTH_LOG"
echo "========================================" | tee -a "$HEALTH_LOG"
echo "           SUMMARY" | tee -a "$HEALTH_LOG"
echo "========================================" | tee -a "$HEALTH_LOG"

if [ ${#ISSUES[@]} -eq 0 ] && [ ${#ALERT_ITEMS[@]} -eq 0 ]; then
    log_info "All checks passed! ✓"
else
    [ ${#ISSUES[@]} -gt 0 ] && log_warn "Issues: ${#ISSUES[@]}"
    [ ${#ALERT_ITEMS[@]} -gt 0 ] && log_error "Needs attention: ${#ALERT_ITEMS[@]}"
fi

[ ${#FIXES[@]} -gt 0 ] && log_info "Fixed: ${#FIXES[@]}"

echo "" | tee -a "$HEALTH_LOG"

# === TELEGRAM ALERT IF NEEDED ===
if [ ${#ALERT_ITEMS[@]} -gt 0 ]; then
    MESSAGE="🚨 *OpenClaw Health Alert*%0A%0A"
    for item in "${ALERT_ITEMS[@]}"; do
        MESSAGE+="• $item%0A"
    done
    MESSAGE+="%0AIssues found: ${#ISSUES[@]}%0A"
    MESSAGE+="Fixes applied: ${#FIXES[@]}"
    
    curl -s "https://api.telegram.org/bot$(cat $OPENCLAW_DIR/.telegram-bot-token 2>/dev/null)/sendMessage?chat_id=$TELEGRAM_CHAT_ID&text=$MESSAGE&parse_mode=Markdown" > /dev/null 2>&1
    log_info "Alert sent to Telegram"
fi

echo "Log: $HEALTH_LOG"
