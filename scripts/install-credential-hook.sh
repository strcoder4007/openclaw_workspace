#!/bin/bash
# Install credential scanner as git hooks
# Run from your repository root: ./install-credential-hook.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCANNER_SCRIPT="$SCRIPT_DIR/credential-scanner.sh"

# Make the scanner executable
chmod +x "$SCANNER_SCRIPT"

# Detect if we're in a git repo
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Not in a git repository"
    exit 1
fi

GIT_DIR="$(git rev-parse --git-dir)"
REPO_ROOT="$(git rev-parse --show-toplevel)"
HOOKS_DIR="$GIT_DIR/hooks"

# Create hooks directory if it doesn't exist
mkdir -p "$HOOKS_DIR"

# Create a wrapper hook that calls the scanner with correct path
# This fixes the path issue when hook is copied to .git/hooks/
cat > "$HOOKS_DIR/pre-commit" << 'WRAPPER_EOF'
#!/bin/bash
# Pre-commit hook - Credential Scanner
# This wrapper finds the scanner relative to repo root

REPO_ROOT="$(git rev-parse --show-toplevel)"
SCANNER="$REPO_ROOT/credential-scanner.sh"

exec "$SCANNER" staged
WRAPPER_EOF

chmod +x "$HOOKS_DIR/pre-commit"

# Also install as commit-msg hook for extra paranoia
cp "$HOOKS_DIR/pre-commit" "$HOOKS_DIR/commit-msg"

echo ""
echo "✅ Credential scanner installed!"
echo ""
echo "Hooks installed to:"
echo "  - $HOOKS_DIR/pre-commit"
echo "  - $HOOKS_DIR/commit-msg"
echo ""
echo "The scanner will run before every commit and check:"
echo "  - Staged files for credential patterns"
echo "  - API keys (sk_, pk_, sb_, etc.)"
echo "  - Tokens (GitHub, AWS, etc.)"
echo "  - Database connection strings"
echo "  - JWT tokens"
echo "  - High-entropy strings (30+ char base64)"
echo ""
echo "To scan all files (not just staged) manually:"
echo "  ./credential-scanner.sh all"
echo ""
echo "To bypass (NOT RECOMMENDED):"
echo "  git commit --no-verify"
