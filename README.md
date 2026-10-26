# Artifact bundle: Who Contributes What in Human-AI Research (ICIS 2026 PDW on Autonomous Scholarship)

This bundle holds the structured research artifacts behind the submission. It is a redacted copy. The project is its own data: a human orchestrator and AI agents produced the paper, and every session was recorded.

## What is here

| Folder | Content |
|---|---|
| `research/` | Framework drafts v0.1 and v0.2, codebooks v1.0 and v1.1 (frozen, with change list), research design, literature candidates and access status, reference metadata (Crossref), analysis and build scripts (`research/tools`) |
| `research/coding/` | Unit tables (`units_final.csv` has the 265 coded units with their full text, `units_all_v1_146.csv` the 146 units of run 1), exclusion lists with the rules that removed units, agreement, existence, stage, transition and mechanism outputs of run 1 (`final/`) and run 2 (`final_v2/`), and the raw outputs of both coders (`coder_results/*.jsonl`) |
| `records/` | The four append-only logs (interventions, events, verification, artifacts), the session registry, the environment record, the logging scripts and the redacted verbatim human messages |
| `AGENTS.md`, `.opencode/skills/...` | The project rules and the logging skill that every agent had to follow |
| `paper/` | Manuscript and appendix build scripts, the submitted PDFs, figure sources (`drawio`, generation prompts and records, icon assets, live build scripts) |
| `submission/` | The single submission PDF, the script that assembled it and its scan report |

## How to reproduce the numbers

1. `research/coding/units_final.csv` and `research/coding/final_v2/coder_results/` hold the units and both coders' tags.
2. `research/tools/analysis_v2.py` computes agreement, existence, stage and transition tables. `research/tools/mechanism_analysis_v2.py` computes delegation episodes and the fate of AI proposals.
3. `paper/numbers_v4.py` reads those outputs, and `paper/build_paper.py` asserts every number that the text states.
Absolute paths in the scripts point to the original machine and appear here as `<project>` or `<home>`. Adjust them before running.

## What is not included, and why

- **Raw session exports** (about 130 MB of text, 69 sessions). They contain tool outputs with local paths, user and resource names, forwarded third-party email text and other personal details that a pattern-based redaction cannot make safe with certainty. The text of every unit that the analysis used is in `units_final.csv`, and every human message is in `records/verbatim/human_messages_verbatim_redacted.csv`. Reviewers can request the raw exports under confidentiality.
- **A forwarded third-party email** (the call for participation sent to the human by an advisor). Its text is replaced by a placeholder in `records/verbatim/human_messages_verbatim_redacted.csv`, in the unit tables (unit S02-U001) and in two evidence quotes of the coder outputs. The coders saw the original, so the coded unit and the released unit differ in this one text. The public call for papers is in the submission package.
- **Source texts** read during the project (open and third-party copies). They are copyrighted. `research/source_access_status.csv` lists each source and how far it was read.
- **Large intermediate files** of the figure work (generation sheets and early draw.io versions).

## Redaction

User name, local paths, email addresses, an organiser’s name, cloud resource names and the author’s name are replaced by placeholders (`<user>`, `<home>`, `<project>`, `[email]`, `an organiser`, `[resource]`, `[azure-endpoint]`, `[author]`). The logs, the codebooks and the coder outputs are otherwise verbatim. Chinese original wording of the human is kept. A leak scan of this folder is in `RELEASE_SCAN.txt`.

## Known defects

- The log rows I022, I033 and I035 were written in a garbled encoding. The correct originals are in `records/verbatim/human_messages_verbatim_redacted.csv`.
- Some log timestamps were typed by hand and run ahead of the clock (see event E074).
- Absolute paths in the scripts point to the original machine. Some analysis scripts read the run 1 coder outputs from `%TEMP%`, and copies of these outputs are in `research/coding/final/coder_results`.

## License (proposal, the authors decide)

Text, data and figures: CC BY 4.0, as the submission form asks for accepted papers. Code: MIT.
