# Environment record (update whenever a tool, model, or setting changes)

Captured: 2026-10-21 (Asia/Shanghai) in session `ses_ea32c9901ffe7o77BUt54LtH2Q`.

| Item | Value |
|---|---|
| Host OS | Microsoft Windows NT 10.0.26300.0 |
| Agent host app | OpenWork Desktop 0.18.59 |
| Agent runtime | OpenCode 1.18.30 |
| Primary agent / model | agent `openwork`, model `claude-sonnet-5.5` via provider `github-copilot` (id `github-copilot/claude-sonnet-5.5`) |
| Shell used by agent | cmd.exe; Windows PowerShell 5.1.26100.9711 (full path only) |
| Not available on agent PATH | python, node, git, sqlite3 |
| Workspace | `<project>` (not a git repo) |
| Model settings | temperature / reasoning effort etc. are not exposed to the agent; the exact per-message model, agent name and system prompt are in each raw session file (`messages[].info`) |
| Skills installed (global) | see `<available_skills>` in the raw session system prompt; project skill: `project-provenance-logging` |
| Time zone | Asia/Shanghai (UTC+08:00) |

Authoritative per-session metadata (framework, version, models) is generated into `session_registry.csv` by `scripts/sync_sessions.ps1`.
This file only records what is NOT in raw sessions (machine, runtime, tools).

## Change log
- 2026-10-21: initial snapshot.
- 2026-10-22 (retroactive entry, written in session `ses_e9dd5da08ffe0Ul310mqUTSi6K`): the figure rebuild of events E045 to E054 is logged under `opencode/big-pickle (MiniMax-Flash)`; after the human rated its figure aesthetics as poor (I036) the work continues with `github-copilot/claude-sonnet-5.5` (E055). Tools added or used in this stretch: Sivia live draw.io MCP (`<home>\Tools\Sivia`, `SIVIA_HOME=<home>\.sivia`), draw.io desktop for export, Python 3.11 with Pillow at `%LOCALAPPDATA%\Programs\Python\Python311`. The agent shell is cmd.exe without System32 on PATH, so full paths are used.
