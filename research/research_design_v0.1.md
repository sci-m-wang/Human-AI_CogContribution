# Research design v0.1 (qualitative single case, self-referential)

Status: DRAFT for human review, 2026-10-21. Author: openwork/claude-sonnet-5.5; decisions by human: I017, I018, I019, I020. Not a manuscript.

## 1. Purpose and stance
Describe, from the recorded trace of one AI-led research project, what human and AI cognitive contributions exist, how they are distributed across categories, and how they pass between actors. Qualitative, descriptive and interpretive: existence and patterns are the findings; numbers are symbolic reference only (I018). Generalisation is analytic: to the typology and to conditions under which the patterns appear, not to a population of projects (Eisenhardt 1989 [S074]; Lee & Baskerville 2003 [S076]).
Boundary of the claim: what is visible in the trace. Thought that never reached the trace is out of scope.

## 2. Research questions (human formulation I018)
**RQ1 Existence.** Do human, AI, and mixed human-AI cognitive contributions each exist in the project? This addresses two common worries: "once AI is available, is the human unnecessary?" and "is AI only an execution tool with no ideas of its own?" For mixed contributions, what collaboration modes appear?
**RQ2 Distribution.** Across which categories do human and AI contributions fall (what do humans do, what does the AI mainly do)? Counts are given for reference only.
**RQ3 Transition.** What patterns of transition between human and AI contributions occur, and what interaction modes do they represent, including those that involve mixed contributions?
Method reliability (agreement between coders, boundary problems) is discussed in the Discussion, not an RQ.

## 3. Key definitions
- **Cognitive contribution**: externalised move that adds to or changes the shared research state, identifiable from the trace (codebook v1.0/1.1). Types K, P, D, M; non-cognitive X, C, Z.
- **Existence criterion (RQ1)**: an actor-type combination "exists" if at least one unit has an *agreed* tag (both independent coders) with evidence quote, and the human adjudicates the exemplar. A type judged absent is also reported with the closest near-miss.
- **Mixed contribution (human ruling I019)**: both actors contribute to the same output, each with explicit expression (e.g. AI supplies knowledge, human proposes a scheme based on it). Not mixed: a bare approval, or a run of "ok"/"confirmed" without content. Content-based test: the human unit adds, changes or reasons about something.
- **Output**: a project artefact or decision-bearing text that persists (e.g. a codebook version, a unit definition, a research question set, a verification method). Mixed contributions are identified per output.
- **Transition**: adjacent pair of units in one session timeline (plus explicit spawn/report links), written `actor:primary-type -> actor:primary-type` (human ruling: primary tags). Corrections are not a separate category (I020).
- **Interaction mode**: a recurring transition pattern, named and described, with representative excerpts.

## 4. Data
All sessions of the project (human ideation session, main session, sub-agent sessions, coder sessions) recorded by the provenance mechanism; units per codebook (one response). Each manuscript revision updates the corpus; analyses are rerun and differences between versions are themselves documented (human: iteration is interesting, I015). Development set = units existing at codebook freeze; evaluation set = units after freeze. Current counts are not fixed in any wording (I015).
Coders: two independent LLMs (GPT-6.1-sol, Gemini-4-argon). Primary agent = designer/coordinator, not an independent coder. Human adjudicates disagreements and reviews exemplars.

## 5. Analysis procedure (qualitative)
**Step 1 Existence matrix (RQ1).** For actor x type (human, AI-primary, AI-subagent x K, P, D, M) list agreed tags and 1-3 exemplar quotes each. Answer the two worry-questions with the evidence, and with what the trace cannot show.
**Step 2 Mixed contributions (RQ1, RQ3).** Identify outputs; for each, list the units that contributed and their tags; apply the I019 test; classify mixed ones into collaboration modes by *which type each actor supplied* (e.g. AI K + human P; human K4 + AI P; human D + AI P). Record near-misses (relays, bare approvals).
**Step 3 Distribution (RQ2).** Describe by category and actor with presence counts and by-stage lists, with representative content ("what humans do", "what AI mainly does"). Report both coders' counts and both agreement statistics as reference only. Do not interpret small differences. Also tabulate by research stage (CFP functions plus governance and tooling) to show where in the project each actor's contributions fall.
**Step 4 Transitions (RQ3).** Build primary-tag sequences within sessions; list transition types that occur, sorted by frequency but interpreted by content. Group into interaction modes (candidates from examples: proposal-commitment relay `AI:P -> human:D`; supply-and-reframe `AI:K -> human:K/P/D`; delegation-report `human:M/D -> AI:M(spawn) -> AI:K`; human-redirect appears as ordinary `human:M` units). Name each mode, give excerpts, say which involve mixed contributions.
**Step 5 Version comparison.** Re-code at each major manuscript revision (same codebook version); report what changed in existence, distribution and modes.
**Step 6 Reflexive check.** Human reviews exemplars and modes; every adjudication logged. The AI-as-coder-and-author conflict is disclosed.

## 6. Evidence standards
Each claim cites unit ids and a short quote. Counts are never the sole basis for a claim. A mode needs at least two independent instances or is labelled "single instance". Claims about sources use only read sources.

## 7. Discussion topics reserved (human I018)
Method reliability and boundary problems (M vs X; narration units; uptake instability; agreement statistics reported), self-preference risk, small N, invisibility of off-trace cognition, designer = coded author, design-science evaluation.

## 8. Resolved by the human (I021)
1. Mixed contributions are identified at the level of outputs: accepted.
2. RQ2 distribution is also reported by research stage (literature, theory, design, governance, ...): added to Step 3.
3. No separate treatment of AI autonomous decisions: the `autonomous` flag stays an optional note (see v1.1 C5) and is not an analysis section.
Still open: approval to freeze codebook v1.1 (C1-C7) and re-code.
