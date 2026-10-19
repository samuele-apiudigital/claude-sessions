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
| `cs`      | live full-screen dashboard (+ web view)      |
| `cs -o`   | print once and exit                          |
| `cs -a`   | also show sessions ended in the last 24h     |
| `cs -t`   | classic table layout                         |
| `cs -j`   | JSON output                                  |
| `cs -s`   | web dashboard on http://127.0.0.1:7421       |
| `cs -w`   | open the web dashboard instead of the TUI    |

Keys: arrows select, Enter or click focuses the session's app, `/` opens the chat,
`p` searches projects, `a` toggles ended sessions, `r` refreshes, `w` opens the web view, `q`/Esc quits.

`cs` also serves the web dashboard in the background and shows an `open web view ↗` link on the bottom
line (click it or press `w`). It uses the same port as `cs -s` (`7421` or `$CS_PORT`); if a
`cs -s` or another `cs` is already serving there, it links to that one instead. The server
stops when `cs` quits.

Focus works for VS Code (window of the session's folder), Terminal.app and iTerm2
(exact tab by tty). Other terminals (e.g. Warp) are only brought to the front.

## Web dashboard

`cs -s` serves the same dashboard as a web page: tiles, agents, context bars, usage limits
bar and the chat, refreshed every 2s. It listens on `127.0.0.1:7421` (or the first free port
if that one is taken); `cs -s 8080` or `CS_PORT=8080 cs -s` uses a fixed port. The page lives in
`web/index.html` and is re-read on every load.

`cs -w` does the same and opens the page in your browser, without the terminal dashboard. If a
`cs` or `cs -s` is already serving on that port, it just opens that one and exits.

`cs -w`, `w` and the `open web view ↗` link open the installed app instead of a browser tab when
there is one for the same port (Chrome, Edge or Brave apps in `~/Applications`).

Keys: arrows select, Enter or click focuses the session's app, `/` opens the chat (Esc closes),
`p` searches projects, `a` toggles ended sessions, `t` switches between tiles and the table layout, `r` refreshes.

It can be installed as an app (its own window and Dock icon): press `i`, or use the install
button in Chrome's address bar; in Safari use File › Add to Dock. The app needs `cs -s`
running on the same port; while the server is down it shows the last page as offline and
reloads itself when the server is back.

### Themes

Pick a theme from the select in the top-right corner. Themes are listed in `.settings.json`,
which also stores the selected one (the select writes it back; editing the file by hand works too,
it is read on every request):

```json
{
  "projects": "~/Projects",
  "theme": "terminal",
  "themes": [
    { "id": "terminal", "title": "Terminal", "file": "Terminal-theme.css" },
    { "id": "claude", "title": "Claude", "file": "Claude-theme.css" }
  ]
}
```

Each theme is one complete stylesheet in `web/themes/`. To add one, copy a theme file, restyle
it, and add an entry to `themes`. The page sets some colours inline, so a theme must define the
tokens listed at the top of `Terminal-theme.css`.

It only accepts requests addressed to `127.0.0.1`/`localhost` that carry a token generated at
startup, so other websites can't drive the chat (which runs with permissions bypassed).

## Projects

The line above the chat lists the git repos you used most recently with Claude (from
`~/.claude/projects`); click one to open it in VS Code. `p` searches all repos in the projects
folder: type to filter, arrows select, Enter opens, Esc closes. In the web view the line is a row
of chips with a search box; the folder at its right end shows the projects folder, click it to
change it.

The projects folder is `projects` in `.settings.json` (default `~/Projects`, colon-separate several).
Repos are found up to three levels deep. `CS_REPO_ROOTS`, if set, overrides it.

## Chat

Press `/` (or click the `›` line) to talk to a small Claude of its own, separate from
your sessions: "open claude-sessions in VS Code", "show ariston in Finder". Enter sends,
Esc closes, `/clear` starts a new chat. It knows the git repos in the projects folder
and your live sessions, and runs headless (`claude -p`) with every tool and MCP server
and permissions bypassed, so it acts without asking.

| Variable          | Default                                         |
|-------------------|-------------------------------------------------|
| `CS_CHAT_MODEL`   | `haiku`                                         |
| `CS_REPO_ROOTS`   | overrides the projects folder (colon-separated) |
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
