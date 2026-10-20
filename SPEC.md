# claude-sessions — repo report

> Snapshot spec, 2026-07-19. One commit behind nothing: `main`, remote `origin` (github.com/samuele-apiudigital/claude-sessions-manager).

## What it is

A macOS tool that renders a live dashboard of your **Claude Code sessions** — in the terminal (full-screen TUI) and as a local web app. One tile per session showing status, context-usage bar, model, token counts, working dir, git branch, current task, the session's subagents/workflows, plus an account rate-limit bar. A built-in chat panel ("Ask Claude") runs a headless `claude -p` instance that can act on your machine (open repos in VS Code, Finder, URLs…).

## Layout

| Path | Lines | What |
|---|---|---|
| `claude-sessions` | 1119 | POSIX `sh` shim that `exec`s `python3 -I` with an embedded Python program (stdlib only). All logic lives here. |
| `web/index.html` | 594 | Single-file web dashboard: HTML + CSS hooks + vanilla JS, no build step. |
| `web/themes/*.css` | 809 | Three complete stylesheets (Terminal, Claude, Dracula); themes are listed in `.settings.json`. |
| `web/sw.js`, `web/manifest.webmanifest`, `web/icons/` | — | PWA: installable app, offline fallback (network-first, `/api/` never cached). |
| `extras/` | 30 | `statusline-snippet.sh` (feeds the usage bar), Warp launch config, launchd plist for start-at-login. |
| `install.sh` | 12 | Symlinks the script into `~/.claude/scripts`, adds the `cs` alias to `~/.zshrc`. |
| `.settings.json` | 18 | User config: `projects` folder(s), selected `theme`, theme list. Read per-request, written back by the web UI. |

~2.9k lines total. No dependencies, no tests, no CI.

## Architecture

### Data sources (read-only)
- `~/.claude/sessions/*.json` — live session registry (pid, status, cwd, entrypoint).
- `~/.claude/projects/*/<sid>.jsonl` — transcripts; parsed line-by-line in `stats()` for tokens, model, turns, tool calls, task list, titles.
- `~/.claude/projects/*/<sid>/subagents/` — agent transcripts + workflow journals (`agent_detail()`).
- `~/.claude/state/rate-limits.json` — written by the statusline snippet.

### Modes (arg parsing in the shim)
`cs` TUI · `-o` once · `-a` +ended (last 24h) · `-t` table · `-j` JSON · `-s [port]` serve web only · `-w` open web app and exit if already served.

### Web server
`ThreadingHTTPServer` on `127.0.0.1:7421` (`CS_PORT`, or first free port). Serves `web/` re-read per request, plus:

- `GET /api/state` — sessions + usage + chat + projects + cfg (2s server-side cache).
- `POST /api/focus | /api/theme | /api/open | /api/settings | /api/chat`.

Security model: Host header must be `127.0.0.1`/`localhost` on the serving port; all POSTs require a per-run `X-CS-Token` (random, injected into the page as `__CS_TOKEN__`). CSP + nosniff headers. Reasonable for a local-only tool.

### Chat
`claude -p` with `--permission-mode bypassPermissions`, `stream-json`, default model `haiku` (`CS_CHAT_MODEL`). Runs in a dedicated cwd (`~/.claude/state/cs-chat`) and its own session id; the system prompt injects the repo list + live sessions. Shared state between TUI and web (one `CHAT` buffer, guarded by locks).

### TUI
Alt-screen, cbreak on `/dev/tty`, 10 Hz render loop with 2s data refresh, mouse (X10/SGR) click support, east-asian-width-aware padding/clipping. Focus detection walks the process parent chain to find the terminal/IDE app, then AppleScript-selects the exact tab (Terminal.app, iTerm2) or `open -a` (VS Code/Cursor, Warp).

## Notable qualities

- **Very compact** — the whole product is one script + one HTML file; trivially readable and portable.
- **Zero deps** — stdlib Python, vanilla JS, no build.
- **Nice UX details**: PWA with offline fallback, theme system with hot-reload, rainbow logo on "ultracode", agent/workflow tracking with lifecycle states (running/lost/completed/failed/stopped), recent-projects bar with fuzzy-ish search.
- **macOS-only** by design: `open`, `osascript`, AppleScript, launchd, `~/Applications` app detection.

## Risks / rough edges

- **One 1.1k-line file**: monolith; TUI, server, chat, stats all interleaved. Fine at this size, but growing features will hurt.
- **No tests, no CI** — transcript parsing depends on Claude Code's JSONL schema drifting; a schema change silently degrades stats (parsing is exception-swallowing everywhere).
- **bypassPermissions chat** — powerful and intentional; the token/host guard is the only protection. Don't ever bind beyond loopback.
- **`python3 -I` + heredoc**: `CS_SELF` must point at the script so `web/` and `.settings.json` resolve; running it via a copy elsewhere breaks web serving.
- **`find_repos()` walks up to 3 levels** over the whole projects folder on every 2s cycle — fine for a few hundred repos, could get slow on a large tree (no cache, no mtime pruning).
- **Status bar depends on the user installing** the statusline snippet; without it the usage bar shows "no data yet".
- **`web/index.html` re-read per request** with `__CS_TOKEN__`/`__CS_THEME__` string replacement — works, but means the page is effectively server-rendered; any JS caching of the page would pin a stale token (the SW is network-first to compensate).

## Suggested next steps (if continuing)

1. Extract transcript parsing into a module with a couple of fixture tests.
2. Add `cs -h/--help` (currently only the header comment documents flags).
3. Cache `find_repos()` results keyed on folder mtime.
4. Consider a `pyproject.toml`/Makefile if the single-file trick is ever dropped.
