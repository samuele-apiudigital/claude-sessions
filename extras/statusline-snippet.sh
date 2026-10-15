# Add right after `input=$(cat)` in your Claude Code statusLine script.
# It shares the account rate limits with the dashboard's usage bar.
if [ -n "$input" ]; then
    mkdir -p "$HOME/.claude/state"
    printf '%s' "$input" | jq -ce 'select(.rate_limits != null) | {ts: (now | floor), rate_limits: .rate_limits}' \
        > "$HOME/.claude/state/rate-limits.json.tmp" 2>/dev/null \
        && mv "$HOME/.claude/state/rate-limits.json.tmp" "$HOME/.claude/state/rate-limits.json"
fi
