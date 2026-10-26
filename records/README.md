# records/ — provenance & process record (append-only evidence)

Purpose: make the human–AI division of labour of this project inspectable (ICIS PDW workflow appendix,
Human–AI Contribution Disclosure) AND provide the raw data for the paper's own analysis (the project is
self-referential: its sessions are the dataset).

| Path | What | Who writes | Editable? |
|---|---|---|---|
| `raw_sessions/<id>.json` | Full OpenCode session export (all messages, tool calls, model, agent, system prompt) | `scripts/sync_sessions.ps1` | NO (regenerated snapshots only) |
| `raw_sessions/external/` | Transcripts from other agents/frameworks | human or agent drops file | NO after drop |
| `session_registry.csv` | One row per session: framework, version, agent, models, parent/child, hash, counts | script (+ manual `role_in_project`, `notes`) | only manual columns |
| `snapshot_log.csv` | Every snapshot taken: time, sha256, size, message count | script | NO |
| `extra_sessions.txt` | Session ids outside this folder that belong to the project | agent/human | append |
| `logs/interventions.csv` | Every material human intervention (choice, feedback, redirect, manual edit) + reason | agent, confirmed by human | append-only |
| `logs/events.csv` | Errors, failures, abandoned approaches, detections and responses | agent/human | append-only |
| `logs/verification.csv` | Citation / code / data / cross-model checks and results | agent/human | append-only |
| `logs/artifacts.csv` | Files produced, by whom (session/model), verification status | agent | append (update status column via new row note) |
| `environment.md` | Machine, runtime, tooling not visible in raw sessions | agent | update + change log |

## Rules of thumb
- Raw data is evidence: never edit, delete, or "clean" it. Summaries live elsewhere.
- Raw sessions may contain personal paths, system prompts and account names. They are PRIVATE until reviewed;
  publish only via a reviewed/redacted copy (e.g. `opencode export --sanitize`) and never credentials.
- Sync at: session start, after every milestone/artifact, before any sub-agent finishes its report is used,
  before leaving a session, and before submission (final freeze with hashes).
- Sub-agents: they are separate sessions in the same DB and get picked up by the sync script; the spawning
  agent must also log the spawn (task description, `task_id`, sub-agent type) in `events.csv`.
- Human interventions are logged by quote/summary + message id once the id is available (re-sync, then fill `message_id`).
