#!/bin/sh
# Links claude-sessions into ~/.claude/scripts and adds the `cs` alias.
set -e
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$HOME/.claude/scripts"
ln -sf "$here/claude-sessions" "$HOME/.claude/scripts/claude-sessions"
chmod +x "$here/claude-sessions"
grep -q "alias cs=" "$HOME/.zshrc" 2>/dev/null || \
    echo "alias cs='$HOME/.claude/scripts/claude-sessions'" >> "$HOME/.zshrc"
echo "installed. open a new shell and run: cs"
