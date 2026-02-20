#!/bin/bash
# Paranoid Credential Scanner - Pre-commit Hook
# Scans staged files for potential credentials before commit

echo "Scanning for credentials..."

# Patterns to detect (basic regex compatible with bash 3.2)
PATTERNS="sk_[a-zA-Z0-9]{20,}|pk_[a-zA-Z0-9]{20,}|sb_[a-zA-Z0-9]{20,}|AKIA[0-9A-Z]{16}|gh[pousr]_[a-zA-Z0-9]{36,}|postgres://|mysql://|mongodb://|redis://"

# Check if file should be skipped
should_skip() {
    local file="$1"
    # Skip shell scripts (they often contain example patterns in comments)
    if [[ "$file" == *.sh ]]; then
        return 0
    fi
    # Skip other common patterns
    case "$file" in
        *.git|*node_modules*|*__pycache__*|*.venv|venv|*.env*|*.lock|*.json|*.yaml|*.yml)
            return 0
            ;;
    esac
    return 1
}

# Scan a single file - returns 1 if credential found, 0 otherwise
scan_file() {
    local file="$1"
    
    # Skip binary files
    if file "$file" 2>/dev/null | grep -qE "(image|video|binary|MPE|compressed)"; then
        return 0
    fi
    
    # Skip files > 1MB
    local size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
    if [[ "$size" -gt 1048576 ]]; then
        return 0
    fi
    
    # Check for patterns
    if grep -E "$PATTERNS" "$file" 2>/dev/null; then
        echo "  ^ Potential credential in: $file"
        return 1  # Found issue
    fi
    
    return 0  # Clean
}

# Main - track issues globally
total_issues=0
files_scanned=0

# Get staged files
for file in $(git diff --cached --name-only --diff-filter=ACM 2>/dev/null); do
    [[ -z "$file" ]] && continue
    
    if should_skip "$file"; then
        continue
    fi
    
    if [[ -f "$file" ]]; then
        files_scanned=$((files_scanned + 1))
        scan_file "$file"
        result=$?
        if [[ $result -eq 1 ]]; then
            # scan_file returns 1 (credential found)
            total_issues=$((total_issues + 1))
        fi
    fi
done

echo ""
echo "Scan complete: $files_scanned files scanned"

if [[ $total_issues -gt 0 ]]; then
    echo "ABORTING commit: $total_issues potential credential(s) found"
    echo ""
    echo "If you are sure this is a false positive, force with:"
    echo "  git commit --no-verify"
    exit 1
else
    echo "No credentials detected"
    exit 0
fi
