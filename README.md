# claude-sessions

A full-screen terminal dashboard for your running Claude Code sessions (macOS).
One tile per session with status, context usage, model, tokens, working directory,
git branch, current task, plus a fixed usage-limit bar at the bottom.

## Install

```sh
./install.sh        # symlinks into ~/.claude/scripts and adds the `cs` alias
```

Requires `python3` (stdlib only). Run `cs`.

## Usage

| Command   | What it does                                 |
|-----------|----------------------------------------------|
| `cs`      | live full-screen dashboard                   |
| `cs -o`   | print once and exit                          |
| `cs -a`   | also show sessions ended in the last 24h     |
| `cs -t`   | classic table layout                         |
| `cs -j`   | JSON output                                  |

Keys: arrows select, Enter or click focuses the session's app, `a` toggles ended
sessions, `r` refreshes, `q`/Esc quits.

Focus works for VS Code (window of the session's folder), Terminal.app and iTerm2
(exact tab by tty). Other terminals (e.g. Warp) are only brought to the front.

## Colours

- orange logo: always; rainbow when the session is in ultracode
- orange status: running, grey: waiting / ended

## Usage limits bar

Claude Code only passes rate limits to the status line. Add
`extras/statusline-snippet.sh` to your statusLine script so it writes
`~/.claude/state/rate-limits.json`, which the dashboard reads.

## Open at login (Warp)

Copy `extras/warp-launch-configuration.yaml` to `~/.warp/launch_configurations/`
and `extras/com.user.claude-sessions.plist` to `~/Library/LaunchAgents/`, then
`launchctl load` it.

## Data sources

- live sessions: `~/.claude/sessions/*.json`
- transcripts: `~/.claude/projects/*/<sessionId>.jsonl`
- limits: `~/.claude/state/rate-limits.json`
