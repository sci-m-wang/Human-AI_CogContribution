# Codebook v1.0-draft: Observable Cognitive Contributions in Human-AI Research Collaboration

Status: v1.0 FROZEN on human approval (see records/logs/events.csv for timestamp), 2026-10-21. Supersedes framework_v0.2.md (kept as record). Drafted by openwork/claude-sonnet-5.5 (designer/coordinator, NOT an independent coder), session ses_ea32c9901ffe7o77BUt54LtH2Q. Human (responsible author; designer, proposer, reviewer) directions: I012, I013, I014, I015.
Evidence base: sources with notes in research/fulltext/ ([Sxxx]); unread sources are not used as grounds. (HYPOTHESIS) marks design choices not grounded in a source.

## 0. Construct
A **cognitive contribution** is an externalized move by an actor that adds to or changes the shared research state and is identifiable from the trace alone. We code manifest content; we do not infer internal cognition (indicator logic as in Garrison et al. [S029]; epistemic motive is an inference [S014]).
Paradigm note (I012): knowledge is a contribution type because an AI can supply new knowledge to a human expert; classical taxonomies treat it as what the decider already holds [S001, S002].

## 1. Unit of analysis (revised by I014; HYPOTHESIS operationalisation)
Human decision: a coding unit is **one model response**, not a whole human-to-human interaction; a sub-agent dispatch is a unit, possibly several.
Dry run (research/rounds_dryrun.csv, 499 assistant messages): the export stores every LLM step as an assistant message; 424 of 499 (85%) carry no text (tool calls only). Coding each step would produce mostly empty units. Operational definition:

- **AI unit (a "response")** = one assistant message that contains visible text OR spawns a sub-agent, **together with the tool-only assistant messages since the previous AI unit or human message in the same session** (its work context). Tool calls are evidence, not units.
- **Human unit** = one human message. (In sub-agent sessions the lone `role=user` message is the parent AI's prompt and is attributed to the parent AI, event E013.)
- **Sub-agent session** = its own units under actor `AI-subagent`; the spawning response (parent) carries a link to the child session id. Child final reports are the main text-bearing units.
- Unit id = message id of the text-bearing/anchor message. Every unit has: session, message ids covered, models/agent names, tool names used, files written.
- Volume is not fixed: the corpus grows with the project, so every reported count is tied to a dated snapshot (sync hash in records/snapshot_log.csv) and the unit table is regenerated per coding run. Analysis is mainly qualitative and case-based; generalise to theory, not population (Lee & Baskerville [S076], Eisenhardt [S074]). Each major manuscript revision is re-coded; differences between versions are themselves reported.

## 2. Types (multi-label per unit)
A unit gets a SET of tags `actor:type.subtype`. A response may mix several types and may contain contributions attributable to both actors (e.g. the AI quoting or executing a human instruction: the instruction stays a human tag on the human unit; do not re-tag it on the AI unit). Mark at most one `primary` tag per unit.

Residual: X, C, Z. Cognitive types: K, P, D, M.

### K Knowledge
Brief: introduces information, a concept, a method, a source or a situational fact into the shared record.
Full: the move states or reports what is (or is claimed to be) the case, or how something works, and is offered as input to the work.
Use when: it reports facts, summarises or explains a source/theory, explains how a tool/standard/method works, or states project context unknown to the other party.
Do NOT use when: the move only recommends what to do (P), commits (D), or checks reliability (M1). A literature summary that recommends a design is K2 + P (split).
Subtypes: K1 fact/source/data/quote; K2 concept/explanation/interpretation; K3 method/procedure/standard; K4 situated context (project facts, constraints, deadlines, advisor opinion, intentions).
Flag `epistemic_transfer`: explicit-new if the receiver says it was new or changes behaviour because of it; else no-evidence (absence is not proof of non-novelty).
Examples (this project): AI reports the Mintzberg result that evaluation and choice were separable in 18 of 83 cases (AI:K1); human states the advisor will present at the PDW (human:K4); AI explains what Krippendorff's alpha requires (AI:K3).

### P Proposal
Brief: puts forward a candidate for the project that is not yet committed to.
Full: an idea, option, plan, structure, wording, analysis or artifact offered for adoption, revision or rejection.
Use when: it presents a framing, taxonomy, plan, outline, draft text, code, table, figure, or an alternative/revision to an earlier candidate.
Do NOT use when: the move already commits (D) or only supplies background (K).
Subtypes: P1 frame (question, hypothesis, construct, contribution claim); P2 structure/plan (design, taxonomy, outline, workflow, schema); P3 content (text, code, table, figure, coded result, argument); P4 alternative/revision (must point to what it revises via `responds_to`).
Examples: AI offers framework v0.1 (AI:P2); AI rewrites it as v0.2 after human feedback (AI:P4, responds_to human unit, uptake adopted-modified); human suggests the change to rename expression/design to proposal (human:P1 and human:D2 if phrased as an instruction).

### D Decision
Brief: commits the project to something.
Full: fixes goals, scope, constraints or requirements, or selects/accepts/rejects/terminates. Evaluation and choice are not split (I013; separable in only 18 of 83 cases [S008]): an evaluative statement that expresses preference or acceptability is D2.
Use when: imperative/approving/rejecting language that changes what will be done or kept.
Do NOT use when: the move only offers an option (P) or checks correctness without expressing a preference (M1).
Subtypes: D1 set (goal, question, scope, requirement, constraint, rule for the product); D2 select (accept, reject, choose among alternatives, approve, stop an approach).
Examples: human fixes "unit = one model response" (human:D1); human: "keep M3" (human:D2); AI decides on its own to use a different fetching approach after a failure (AI:D2, flagged `autonomous`).
`autonomous` flag: a D by an AI actor that was not requested by a human instruction in the preceding human unit.

### M Metacognition
Brief: monitors or regulates how the work is done or how reliable it is.
Full: it is about the process or reliability of the work rather than about the product's content (rule R1).
Use when: checking or verifying, detecting an error or gap, asking for evidence or status, planning or re-planning the process, decomposing the task, changing strategy or tools, setting process rules, delegating work, or stating uncertainty, limits or provenance of one's own output.
Do NOT use when: the move changes what the paper/data/codebook contains (K/P/D).
Subtypes: M1 monitor (check, verify, detect error/gap, ask for evidence); M2 regulate (plan, decompose, redirect, set process rules, delegate); M3 calibrate (state uncertainty, limits, confidence, provenance of own output).
Examples: human redirects to survey the literature first (human:M2, with human:D1 secondary; human adjudication I013); AI reports it read only abstracts for 12 sources (AI:M3); human points out the AI's knowledge-as-dimension assumption fails when AI supplies knowledge (the claim itself is human:K2; the act of challenging the output is human:M1).
Grounds: metacognitive knowledge/experiences/goals/actions [S022]; GenAI metacognitive demands (prompt formulation, iteration, output evaluation, automation strategy) [S059]; decision control as "meta-decision-making" [S008].

### X Execution
Carries out a specified step with no new content: running a command, saving a file as specified, formatting, copying. Human note (I-project): execution holds little cognition. Not a cognitive contribution; recorded for coverage. Tool calls inside a unit are X unless their purpose is verification (then the unit has M1).
### C Coordination
Acknowledgement, greeting, turn management, thanks, status echo with no content.
### Z Unclassifiable
Use sparingly; the coder must state why.

## 3. Boundary rules
R1 Object vs process: "if removed, would the paper/data/codebook differ, or only how we produced/checked it?" first = K/P/D, second = M. (human-accepted, I013)
R2 Proposal vs decision: proposals offer; decisions commit. AI draft = P until a human adopts it (adoption is a separate human D2 on the human unit or on the next human unit).
R3 Knowledge vs proposal: K states what is/how it works; P states what we could do/produce.
R4 Verification: checking = M1; the fact found by checking, if reported = K1 as an additional tag.
R5 Mixed units: record every distinct contribution as its own tag; do not force one label. `primary` = the tag that most shapes the unit's outcome.
R5b Proposal + adoption in one unit: record both tags (AI:P*, human:D2 if the human adopts in a human unit).
R6 Direction: setting topic/scope/requirement = D1 even when phrased as a question; a question that merely seeks information = K only if it supplies content, otherwise by function (D1 or M2 by R1).
R7 Corrections: detection = M1; instruction to redo = M2; replacement content written by the human = P/K with `manual_change=yes`.
R8 Literature organising: summarising/organising sources leans M (organising the evidence process) with some D when it fixes what to include (human adjudication I013), but pure reporting of a source's content is K1/K2. Decide by R1.
R9 Attribution: actor comes from session lineage and message source, never from `role=user` alone.

## 4. Attributes per tag
actor (human / AI-primary / AI-subagent); type.subtype; primary (y/n); stage (problem formulation, literature, theory, design, analysis, interpretation, writing, verification, revision, governance, tooling) mirroring the CFP's required contribution account; evidence (message id + quote <=25 words); responds_to (unit id or none); uptake on later tag (adopted / adopted-modified / rejected / questioned / no-response); epistemic_transfer (K); autonomous (D by AI); manual_change (human hand-edit).
Origin/uptake tracing is our design; the supporting literature on linkography and grounding was not accessible [S053, S054]. Initiative as an observable is supported by Walker & Whittaker [S058].

## 5. Output schema (coders return JSON per unit)
{"unit_id": "...", "tags": [{"actor": "human|AI-primary|AI-subagent", "type": "K|P|D|M|X|C|Z", "subtype": "K1|...|null", "primary": true, "stage": "...", "evidence": {"message_id": "...", "quote": "..."}, "responds_to": "unit_id|null", "uptake": "adopted|adopted-modified|rejected|questioned|no-response|null", "epistemic_transfer": "explicit-new|no-evidence|null", "autonomous": true, "manual_change": false}], "uncertain": false, "note": "..."}

## 6. Coders, blinding, agreement
- Independent coders: two LLMs supplied by the human (GPT and Gemini; exact model ids, versions, settings and prompts logged). They receive only the codebook (sections 0-5) and the unit packet; they do not see the designer's codes.
- Designer reference codes (openwork/claude-sonnet-5.5) are reported separately; the designer is not an independent coder (it authored the scheme and most AI content).
- Human: independently codes a stratified subsample and adjudicates disagreements (each adjudication logged as intervention).
- Blinding: remove model and agent names from packets; actor remains recoverable from content, so blinding is partial and reported as such. Self-preference evidence concerns summary quality [S071]; applied by analogy.
- Agreement (human decision I015): report several statistics, not one: percent agreement, Cohen's kappa (pairwise), Krippendorff's alpha with bootstrap CI [S061, partial source], computed per binary variable (actor x type present in a unit) and per subtype where counts allow, plus the confusion pairs. No acceptance threshold is set now: the sample is small and the study is mainly qualitative; interpretation is deferred until results exist (stated openly, to avoid post-hoc threshold choice later we also report all values). Context from prior work, not thresholds: Garrison kappa .35-.74 over rounds [S029]; LLM vs expert kappa .61/.38 vs expert-expert .88/.90 [S068]; CoAIcoder .16-.31 to .51-.65 [S069].
- Reconciliation: classify each disagreement as coder error vs definition problem, revise, version the codebook [S064].

## 7. Phases (contamination control)
- Development set: all units existing at codebook freeze (dry run, framework design). Exploratory only.
- Evaluation set: units produced after freeze v1.0 (e.g. the paper-writing phase today). Used for reported agreement and distribution.
- Log: version, freeze timestamp, set boundary (records/logs). Once frozen, changes create v1.1 and are reported.

## 8. Derived measures (computed from tags, not coded)
1 presence share by actor x type x stage; 2 proposer-committer matrix (P tags: origin actor x D2 actor); 3 knowledge flow (K tags by actor, epistemic_transfer); 4 primary-tag dominance; 5 trajectory over time; 6 autonomous-decision share of AI D tags (degree of AI-led execution, relevant to CFP rubric).

## 8b. Roles and authorship (human question I015)
The CFP states human participants remain the responsible authors and orchestrators and that the disclosure documents contributions, not legal authorship of an AI. So the human is an author; the AI is not listed as author but is fully disclosed. The human's own role (designer of the research direction, proposer of constructs, reviewer/adjudicator) is not asserted by us; it is measured by this scheme (human P1/D/M/K tags) and reported with the same codebook. Affiliations and author order are to be set by the human with the advisor.

## 9. Known weaknesses (disclose)
Self-referential and single-project; most AI content from one model family and the designer is an author of the coded contributions; small N; presence hides weight; human cognition outside the trace is invisible (intervention log is a partial trace); M/D/P boundaries expected to be hardest; read copies of several sources are third-party/preprint versions; the scheme's design-science evaluation [S072 third-party scan; S073 not read] is only outlined; origin/uptake lacks grounding in unread literature.
