# Framework v0.2 and Codebook v0.2: Observable Cognitive Contributions in Human-AI Research Collaboration

Status: DRAFT v0.2 for human review, 2026-10-21. Supersedes v0.1 (kept unchanged as `framework_v0.1.md`). Written by openwork/claude-sonnet-5.5 (session ses_ea32c9901ffe7o77BUt54LtH2Q) from human directions I012 and I013.
Changes from v0.1: unit of analysis is the ROUND (human decision I013); coding is multi-label with actor attached to each label; types are no longer exclusive; evaluation/choice handling, boundary cases and coder design updated.
Evidence base: only sources with notes in `research/fulltext/` (cited as [Sxxx]). Sources not read are NOT used as grounds.
Everything marked (HYPOTHESIS) is a design choice to be tested in the pilot, not a finding.

## 1. Construct and scope

**Cognitive contribution (CC)**: an externalized *move* by an actor (human, or AI agent) that adds to or changes the shared research state, and that can be identified from the trace alone.

We code what is observable (text, instruction, tool-mediated artifact change). We do **not** infer internal cognition. This follows the stance of content analysis of manifest content and the indicator logic of Garrison et al., who note that the latent process is not reliably codable and so derive manifest indicators [S029]; Kirsh & Maglio likewise stress that an epistemic motive is an inference [S014]. Every code is therefore a claim about *what a move does in the shared record*, not about what the actor thought.

**Why a new scheme.** Existing schemes either type cognitive phases for one learner population without actor attribution [S029], code initiative/control rather than cognitive content [S058], or code delegation style per conversation [S049]. We found none that types the cognitive kind of each human and AI move across a whole project (provisional; search incomplete).

**Paradigm adjustment (human input I012).** Classical taxonomies place knowledge as what a thinker already has, and decisions/evaluations/designs as operations on it [S001, S002]. When an AI is a source of new knowledge to a human expert, knowledge is also something that is *contributed and transferred*. So Knowledge is a contribution type here, with an epistemic-transfer flag (Section 4).

## 2. Four contribution types (multi-label: a round carries a SET of actor-type tags)

| Code | Type | Core question for the coder | Closest theory ground |
|---|---|---|---|
| K | Knowledge | Does the move introduce information, a concept, a method, a source, or a situational fact into the shared record? | Knowledge types (factual, conceptual, procedural, metacognitive [S001]; situational, conceptual, procedural, strategic [S002]) |
| P | Proposal | Does the move put forward a candidate for the project (idea, option, plan, structure, wording, design, analysis) that has not yet been committed to? | Design: formulation/synthesis incl. externalised structure, documentation [S013]; development phase search/design [S008] |
| D | Decision | Does the move commit the project to something (choose, accept, reject, fix scope/goal/constraint, terminate)? | Intelligence-design-choice [S007]; identification/selection, evaluation-choice, authorisation [S008] |
| M | Metacognition | Does the move monitor or regulate *how the work is being done or how reliable it is* (checking, error detection, planning the process, calibrating confidence)? | Metacognitive knowledge/experiences/goals/actions [S022]; GenAI metacognitive demands: prompt formulation, iteration, output evaluation, automation strategy [S059]; decision control as "meta-decision-making" [S008] |

### 2.2 Mixed categories
A round typically contains several contributions, possibly of different types and possibly by both actors. Each is recorded as a separate tag `actor:type[.subtype]` with an evidence anchor (message id and a short quote). Examples: `human:D1`, `AI:K2`, `AI:P2`, `AI:M3`, `human:M2`. Two tags of the same actor with different types in one round (e.g. `human:M2` and `human:D1`) are normal, not coder disagreement. Where the coder judges one tag dominant, mark it `primary`; others are `secondary`.
Residual codes (not cognitive contributions; kept so that coverage is complete):
- **X Execution**: carrying out a specified step with no new content (running a tool, writing a file as specified, formatting). Human note: execution contains little cognition (blueprint-following).
- **C Coordination**: acknowledgement, greeting, turn management, thanks, status echo with no content.
- **Z Unclassifiable** (log why).

### 2.1 Subtypes (secondary code)

K (knowledge)
- K1 Fact/source: specific information, citation, data, quote from a source.
- K2 Concept/explanation: definition, theory, relation among ideas, interpretation of a source.
- K3 Method/procedure: how to do something (tool use, analysis procedure, standard).
- K4 Situated context: facts about the project's situation known only to a participant (constraints, deadlines, advisor opinion, prior history, intentions). Mostly human; de Jong's *situational* knowledge [S002].

P (proposal)
- P1 Frame: candidate question, goal, hypothesis, construct, contribution claim.
- P2 Structure/plan: candidate design, taxonomy, outline, workflow, schema.
- P3 Content: candidate text, code, table, figure, coded result, argument.
- P4 Alternative/revision: a candidate that replaces or modifies an earlier candidate (must link to it).

D (decision)
- D1 Set: fixes goal, question, scope, constraints, requirements for the product.
- D2 Select: accepts, rejects, chooses among alternatives, approves, terminates an approach.
- Evaluation and choice are NOT split (human I013: conceptually different, but evaluation usually carries preference and choice; consistent with Mintzberg et al., who could separate them in only 18 of 83 instances [S008]). Rule: an evaluative statement that expresses preference or acceptability is D2; a check of correctness/reliability with no preference expressed is M1. Where both are present, assign both tags (mixed, Section 2.2).

M (metacognition)
- M1 Monitor: checks, verifies, detects an error or gap, asks for status or evidence, flags that something was not read/verified.
- M2 Regulate: plans or reorders the process, decomposes the task, changes strategy or tooling, sets process rules (e.g. recording, verification protocol), delegates/instructs how to work.
- M3 Calibrate: states uncertainty, limits, confidence, or provenance of its own output.

## 3. Decision rules for boundaries

R1 **Object vs process.** A move that changes *what the research product is or contains* is K/P/D. A move about *how we work or how reliable the work is* is M. Test: "if removed, would the paper/data/codebook differ, or only the way we produced and checked it?"
R2 **Proposal vs decision.** Proposals offer; decisions commit. A human saying "I think we could do X" is P; "do X" / "yes, use X" is D2. An AI producing a draft is P3 until a human adopts it (the adoption is a separate D2 move).
R3 **Knowledge vs proposal.** K states what is (or is claimed to be) the case or how something works. P states what we could do or produce. A synthesis of a literature that only reports it is K2; a synthesis that recommends a design is split into K2 + P.
R4 **Verification.** Checking correctness of a claim or output = M1. The *fact found by checking* (e.g. "Crossref shows the title is X") = K1 as a separate move if it is reported.
R5 **Mixed content within a round.** Do not force one code. Record every distinct contribution as its own `actor:type` tag (Section 2.2). Choose `primary` only for the tag that most shapes the round's outcome (HYPOTHESIS: this substitutes for Garrison's "code up/down" tie-break, which solved the one-label-per-message problem [S029]).
R5b **Same content, two actors.** If the AI proposes and the human adopts in the same round, record `AI:P*` and `human:D2` as two tags; do not merge them.
R6 **Direction setting.** Setting the topic, scope or requirement is D1 even if phrased as a question; asking for information is K only if it supplies content, otherwise it is coded by its function: a question that directs the work is M2 or D1 depending on R1.
R7 **Corrections.** A human correcting an AI error: the detection is M1; the instruction to redo is M2; the replacement content, if the human writes it, is P/K with actor = human and flagged `manual_change` (CFP requires such changes be disclosed).



## 4. Unit of analysis: the round (human decision I013)

**Definition (operational, HYPOTHESIS to confirm in dry run).** A round starts at one human message in a session and ends just before the next human message in the same session. It includes everything in between: the assistant's replies, tool calls, files written and any sub-agent sessions spawned (their content is attributed to `AI-subagent`, and their parent prompt is attributed to the parent AI, not to the human; event E013). A sub-agent session is not a separate round; it belongs to the round that spawned it. Rounds are identified by the starting human message id.

Rationale and cost.
- A round is clearly demarcated in the raw export and length is decided by the participants, not the coder; Garrison et al. used the same argument for the message unit [S029].
- Garrison et al. also warn that a unit can contain several cues, and used one-label tie-break rules [S029]. Here, following the human decision, a round may carry several labels, including contributions by both actors; so the unit is coded as a **set of actor-type tags**, not one label.
- Cost: rounds are few. This session so far has only about 6 human messages, i.e. about 6 rounds, although each round contains a lot of AI work (dozens of assistant messages, several sub-agents). Presence-by-round counts will give small totals; the paper must say that the analysis is descriptive and case-based (analytic, not statistical generalisation [S076, S074]).
- Mitigation: every tag carries an evidence anchor (message id + short quote), so a finer analysis (message or move level) can be done later without recoding rounds. Round-level coding remains the primary, pre-specified analysis.

## 5. What is recorded per round

Round header (derived by script, not coded): session id, round id (starting human message id), start/end time, models and agent names that appear, number of assistant messages, tool calls, sub-agents spawned, files changed (artifact paths).

Tags (coded): each tag has

| Field | Values |
|---|---|
| actor | human / AI-primary / AI-subagent |
| type.subtype | K1..K4, P1..P4, D1..D2, M1..M3, X, C, Z |
| primary | yes / no (at most one primary per actor per round) |
| stage | problem formulation, literature, theory, design, analysis, interpretation, writing, verification, revision, governance, tooling (CFP's nine functions plus governance and tooling) |
| evidence | message id + quote (<=25 words) |
| origin | new / responds-to(tag or round id) |
| uptake (on the later tag) | adopted / adopted-modified / rejected / questioned / no-response |
| epistemic_transfer (K tags) | explicit-new / no-evidence |
| manual_change | yes/no (human hand-edit not mediated by AI; CFP disclosure) |

Origin and uptake: tracing where an idea came from and whether it was taken up is motivated by linkography and grounding research, which we could NOT read (S053, S054); this is our design, not grounded in them. Initiative as an observable is supported by Walker & Whittaker's control-shift categories [S058].

Derived distribution measures (computed, not coded):
1. Presence share: for each type and stage, proportion of rounds in which each actor has at least one tag.
2. Proposer-committer matrix: for P tags, who proposed and who committed (D2) = origin x uptake.
3. Knowledge-flow: K tags by actor and epistemic_transfer.
4. Primary-tag distribution (dominance), reported separately from presence.
5. Trajectory over rounds (stage x type), descriptive.

## 6. Coder design (human decision I013)

- **Two independent LLM coders**, supplied by the human and different from each other and (preferably) from the model family that produced most AI moves. They code blind to the designer's codes. Their model names, versions, settings and prompts are recorded.
- **Designer/coordinator = the primary AI (openwork/claude-sonnet-5.5).** It authors the codebook, prepares coding packets, runs the agreement analysis and drafts the adjudication proposals. It is **not an independent coder**: it designed the scheme and produced most AI-side content. Its designer reference codes are reported separately and never counted toward independent agreement.
- **Human**: adjudicates disagreements and codes a stratified subsample independently (size to be set). Human adjudication is logged as intervention.
- **Blinding**: strip model/actor labels where feasible; actor is often recoverable from content, so blinding is partial and reported as such. Self-preference evidence (S071) concerns summary quality, not contribution coding; applied here by analogy only.
- **Packet**: for each round, the coder sees the round transcript with message ids, tool calls summarised, and the codebook entries, and outputs the tag set in a fixed JSON/CSV schema. Prompt = codebook entries (code, definition, when to use, when not to use, examples), constrained label set; this follows the codebook-centred prompt that performed best in Xiao et al. [S068].
- **Agreement**: Krippendorff's alpha with bootstrap CI [S061, partial], minimum acceptable value fixed before the evaluation phase. Because tags are sets, compute alpha per binary variable (actor x type present in round) and report per type. Kappa values in prior work [S068: LLM vs expert .61 and .38 against expert-expert .88/.90; S029: .35-.74; S069: .16-.31 rising to .51-.65] are context, not thresholds.
- **Reconciliation**: each disagreement is classified as coder error vs definition problem and the codebook is revised [S064]; revisions are versioned.

## 7. Phases and contamination control

Because the codebook will be revised after looking at data, we separate:
- **Development set**: rounds that exist when the codebook is drafted/revised. Used for iteration; reported as exploratory.
- **Frozen evaluation set**: rounds produced after codebook freeze (v1.0). Used for the reported agreement and distribution results.
- Every codebook version, freeze time and set boundary is logged. A reviewer can then see that agreement was not tuned on the evaluation set.
(HYPOTHESIS: feasible only if the project continues generating enough rounds after freeze before 2026-10-25; to be decided by the human, see sequencing options.)

## 8. Worked examples from this project's own record (calibration; coded by the drafting AI, NOT reliable)

| Round content (paraphrase) | Tags |
|---|---|
| Human forwards the call email and proposes the topic (origin session) | human:D1 (primary), human:K4 |
| Human states recording requirements (all sessions, sub-agents, model/framework, raw data) | human:D1 (primary), human:M2 |
| Human: "model the externalised form of cognition; we cannot guess it; survey the literature first" | human:M2 (primary, human adjudication I013), human:D1 (secondary). Human judged "organising literature" to lean M with some D. |
| AI proposes a function x stage x attribution taxonomy from memory; later abandoned | AI:P2 |
| AI reports that it read only abstracts for 12 sources | AI:M3 |
| Sub-agent report corrects Amershal to Amershi | AI-subagent:M1, AI-subagent:K1 |
| Human: "AI supplies new knowledge to experts, so knowledge should be a type" | human:K2 (clear K, human adjudication I013), human:D1 (secondary: sets the construct) |
| AI revises framework accordingly | AI:P4 (origin = human tag; uptake = adopted-modified) |

## 9. Known weaknesses (to disclose)
1. One project, one main AI model family; most AI content is produced by the same family as the designer. Mitigation in Section 6; residual self-influence remains.
2. Few rounds; presence-based counts are coarse; evidence anchors allow later finer coding.
3. A round can bundle many functions; presence tags hide how much of the round each took. Dominance (primary) partly compensates.
4. Human cognition not reaching the trace (reading, offline thought, advisor conversations) is invisible. The intervention log is a partial, self-generated trace.
5. M/D/P boundaries are expected to be the hardest. Garrison's kappa rose .35 -> .74 across three rounds of refinement [S029]; low early agreement is an expected finding.
6. The designer is also an author of the contributions being coded, and the human supplies the final adjudication. This is the nature of the self-referential design and is itself disclosed.
7. Several read sources are third-party/preprint copies; quotes need checking against licensed versions before manuscript use. Sources not read (S053, S054, S020, S021, S028, S075 etc.) are not used as grounds.
8. Evaluation of the scheme as a design-science artifact [S072 third-party scan; S073 not read] is planned, not yet specified.