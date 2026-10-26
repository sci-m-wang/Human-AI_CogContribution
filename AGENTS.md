# Project rules (mandatory for every agent, in every session, including sub-agents)

Project: ICIS 2026 PDW "Autonomous Scholarship" submission — cognitive-contribution distribution in
human–AI research collaboration. Self-referential: this project's own collaboration sessions are the data.

## R0. Read first
Before doing any work in this folder, load and follow the skill `project-provenance-logging`
(`.opencode/skills/project-provenance-logging/SKILL.md`). If your framework cannot load skills, read that file directly.
Sub-agents: the spawning agent MUST paste "Obey AGENTS.md and the project-provenance-logging skill" into the sub-agent prompt.

## R1. Everything is recorded
All sessions (any model, any agent framework, any tool, sub-agents, new/other sessions) are raw data.
Run `records/scripts/sync_sessions.ps1` (see skill) at session start, after milestones, and before finishing.
Non-OpenCode transcripts go in `records/raw_sessions/external/` and are registered.
Never edit or delete anything in `records/raw_sessions/`.

## R2. Human–AI division of labour (CFP requirement)
Humans orchestrate and remain accountable; AI performs substantive work. When a human spots an error, prompt the AI to fix it
rather than silently replacing the output with undisclosed human work. Every material human intervention, error, abandoned
approach and verification step goes into `records/logs/*.csv` (append-only).

## R3. Integrity
- No fabricated citations. Every reference must be verified against a real source (DOI/publisher/Crossref/Semantic Scholar/arXiv)
  and logged in `records/logs/verification.csv`. Unverified items are marked `UNVERIFIED` and must not enter the manuscript.
- No hidden instructions to reviewers, no invented data, no false disclosure.
- No credentials or personal data in committed/shared artifacts.

## R4. Submission constraints
Main paper <= 8 pages (excluding references and workflow appendix) in the ICIS template
(`ICIS-2026_-Paper-Submission-Template-v3.docx`). Workflow appendix is mandatory. Deadline 2026-10-25 23:59 AoE.
Code, coding manual, skills and logs go to appendix / repository.

## R5. Language
Conversation with the human: Chinese. Manuscript: English.
