---
name: project-provenance-logging
description: Mandatory in this ICIS PDW project. Use at the start, at every milestone and before finishing any session or sub-agent task in this workspace, and whenever a human intervention, error, abandoned approach, verification, new artifact, new model/agent/framework, or sub-agent spawn occurs. Records raw sessions and structured process logs for the workflow appendix and for the paper's own analysis.
---

# Project provenance logging (project-level, mandatory)

Applies to every agent/model/framework working in this workspace, including sub-agents and sessions opened elsewhere.
Evidence lives in `records/` (see `records/README.md`). All paths are relative to the workspace root.

## 1. At session start
1. Read `AGENTS.md`.
2. Run the sync: `"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -ExecutionPolicy Bypass -File records\scripts\sync_sessions.ps1`
   (PATH may lack System32; use the full path. On macOS/Linux use `pwsh` if available.)
3. Check your own session id appears in `records/session_registry.csv`. If your session started outside this folder,
   append its id to `records/extra_sessions.txt` and sync again.
4. If you are a non-OpenCode agent (Claude Code, Codex, web chat, ...): save your raw transcript/export into
   `records/raw_sessions/external/<label>.<ext>`, sync, then fill agent_framework, framework_version, models, role_in_project.
5. If model, framework version, tool set or machine differs from `records/environment.md`, add a change-log line.

## 2. During work — append rows (never rewrite old rows)
Use IDs `I###`, `E###`, `V###`, `A###` (next free number). Timestamps ISO-8601 with offset (+08:00).
- `logs/interventions.csv` — any human choice, feedback, redirection, manual edit, approval/rejection, scope change.
  Record who, stage, type, a faithful summary (quote key words), the stated reason, how the AI responded, affected files.
  Stages: problem_formulation, literature, theory, design, analysis, interpretation, writing, verification, revision, governance, tooling.
- `logs/events.csv` — errors, tool failures, hallucinations caught, abandoned approaches, sub-agent spawns
  (include sub-agent type, task_id, session id if known, prompt gist), model/framework switches. Include detection method and response.
- `logs/verification.csv` — each citation check (DOI/URL/source, result verified|not_found|mismatch), code run, data check, cross-model check.
- `logs/artifacts.csv` — each file created/changed that matters: who/which session/model, what, verification status.
- Quote/summarise human messages faithfully; do not embellish. If unsure whether something is a "material intervention", log it.

## 3. Sub-agents
When spawning a sub-agent: log an `events.csv` row (spawn), instruct it to obey `AGENTS.md` + this skill, and after it finishes
run the sync so its session (a child session in the same DB) is captured, then record in `session_registry.csv`
`role_in_project` for it. Do not use sub-agent output in the manuscript before it is verified.

Note: `opencode session list` HIDES child sessions; `sync_sessions.ps1` finds them by scanning exported transcripts for
session ids (parentID set). If a sub-agent's session is missing, add its id (from the task result `task_id`) to `records/extra_sessions.txt`.
In a child session the lone `role=user` message is the parent AI's prompt, not a human.

## 4. Before finishing a turn that produced artifacts / at milestones / before ending
1. Update `logs/*.csv`.
2. Run the sync (this also snapshots the current session; the last assistant message of the *running* turn is not yet in the
   export — the next sync will contain it, so always sync at the start of the next session/turn too).
3. Fill `message_id` for earlier interventions when ids become available (look in the raw JSON `messages[].info.id`).

## 5. Final freeze (before submission, 2026-10-25)
Sync, record hashes (`snapshot_log.csv`), produce a redacted shareable copy (`opencode export <id> --sanitize`) after human review,
and generate the appendix tables from the logs. Never include credentials or personal data.

## Do-nots
- Never edit/delete `records/raw_sessions/*`.
- Never log secrets (API keys, tokens). The system prompt in raw files contains env-var NAMES only; still review before sharing.
- Never backfill or reword the past to look better; late entries must say they are late (`timestamp` = real time, text says "retroactive").
