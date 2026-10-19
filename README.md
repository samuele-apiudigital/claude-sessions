# claude-sessions

A full-screen terminal dashboard for your running Claude Code sessions (macOS).
One tile per session with status, context usage, model, tokens, working directory,
git branch, current task, the session's subagents and workflows, plus a fixed usage-limit
bar at the bottom.

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
| `cs -s`   | web dashboard on http://127.0.0.1:7421       |

Keys: arrows select, Enter or click focuses the session's app, `/` opens the chat,
`a` toggles ended sessions, `r` refreshes, `q`/Esc quits.

Focus works for VS Code (window of the session's folder), Terminal.app and iTerm2
(exact tab by tty). Other terminals (e.g. Warp) are only brought to the front.

## Web dashboard

`cs -s` serves the same dashboard as a web page: tiles, agents, context bars, usage limits
bar and the chat, refreshed every 2s. It listens on `127.0.0.1:7421` (or the first free port
if that one is taken); `cs -s 8080` or `CS_PORT=8080 cs -s` uses a fixed port. The page lives in
`web/index.html` and is re-read on every load.

Keys: arrows select, Enter or click focuses the session's app, `/` opens the chat (Esc closes),
`a` toggles ended sessions, `t` switches between tiles and the table layout, `r` refreshes.

It can be installed as an app (its own window and Dock icon): press `i`, or use the install
button in Chrome's address bar; in Safari use File › Add to Dock. The app needs `cs -s`
running on the same port; while the server is down it shows the last page as offline and
reloads itself when the server is back.

It only accepts requests addressed to `127.0.0.1`/`localhost` that carry a token generated at
startup, so other websites can't drive the chat (which runs with permissions bypassed).

## Chat

Press `/` (or click the `›` line) to talk to a small Claude of its own, separate from
your sessions: "open claude-sessions in VS Code", "show ariston in Finder". Enter sends,
Esc closes, `/clear` starts a new chat. It knows the git repos under `CS_REPO_ROOTS`
and your live sessions, and runs headless (`claude -p`) with every tool and MCP server
and permissions bypassed, so it acts without asking.

| Variable          | Default                                         |
|-------------------|-------------------------------------------------|
| `CS_CHAT_MODEL`   | `haiku`                                         |
| `CS_REPO_ROOTS`   | `~/Projects` (colon-separated)                  |
| `CS_CHAT_ROWS`    | `8` chat lines shown                            |

## Agents

Each tile lists the subagents (Agent tool) and workflows the session started. Running ones
show their type, description, current tool (or the workflow's phase and agents done/started)
and elapsed time. Finished ones stay listed for 60s with ✓ (done), ✗ (failed) or ■ (stopped),
then only count in the `done` total. The header shows how many agents are running across all
sessions.

| Variable          | Default                                         |
|-------------------|-------------------------------------------------|
| `CS_AGENT_ROWS`   | `4` agent lines per tile (then `+N more`)       |

## Colours

- orange logo: always; rainbow when the session is in ultracode
- orange status: running, grey: waiting / ended

## Usage limits bar

Claude Code only passes rate limits to the status line. Add
`extras/statusline-snippet.sh` to your statusLine script so it writes
`~/.claude/state/rate-limits.json`, which the dashboard reads.

## Open at login (Warp)

Edit `YOUR_USER` in `extras/warp-launch-configuration.yaml`, then copy it to `~/.warp/launch_configurations/`
and `extras/com.user.claude-sessions.plist` to `~/Library/LaunchAgents/`, then
`launchctl load` it.

## Data sources

- live sessions: `~/.claude/sessions/*.json`
- transcripts: `~/.claude/projects/*/<sessionId>.jsonl`
- agents: `~/.claude/projects/*/<sessionId>/subagents/` (agent transcripts, workflow journals)
- limits: `~/.claude/state/rate-limits.json`
