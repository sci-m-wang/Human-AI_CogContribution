# Framework v0.1 and Codebook v0.1: Observable Cognitive Contributions in Human-AI Research Collaboration

Status: DRAFT v0.1 for human review, 2026-10-21. Written by openwork/claude-sonnet-5.5 (session ses_ea32c9901ffe7o77BUt54LtH2Q) from human direction I012.
Evidence base: only sources with notes in `research/fulltext/` (cited as [Sxxx]). Sources not read are NOT used as grounds.
Everything marked (HYPOTHESIS) is a design choice to be tested in the pilot, not a finding.

## 1. Construct and scope

**Cognitive contribution (CC)**: an externalized *move* by an actor (human, or AI agent) that adds to or changes the shared research state, and that can be identified from the trace alone.

We code what is observable (text, instruction, tool-mediated artifact change). We do **not** infer internal cognition. This follows the stance of content analysis of manifest content and the indicator logic of Garrison et al., who note that the latent process is not reliably codable and so derive manifest indicators [S029]; Kirsh & Maglio likewise stress that an epistemic motive is an inference [S014]. Every code is therefore a claim about *what a move does in the shared record*, not about what the actor thought.

**Why a new scheme.** Existing schemes either type cognitive phases for one learner population without actor attribution [S029], code initiative/control rather than cognitive content [S058], or code delegation style per conversation [S049]. We found none that types the cognitive kind of each human and AI move across a whole project (provisional; search incomplete).

**Paradigm adjustment (human input I012).** Classical taxonomies place knowledge as what a thinker already has, and decisions/evaluations/designs as operations on it [S001, S002]. When an AI is a source of new knowledge to a human expert, knowledge is also something that is *contributed and transferred*. So Knowledge is a contribution type here, with an epistemic-transfer flag (Section 4).

## 2. Four contribution types (primary code, mutually exclusive per move)

| Code | Type | Core question for the coder | Closest theory ground |
|---|---|---|---|
| K | Knowledge | Does the move introduce information, a concept, a method, a source, or a situational fact into the shared record? | Knowledge types (factual, conceptual, procedural, metacognitive [S001]; situational, conceptual, procedural, strategic [S002]) |
| P | Proposal | Does the move put forward a candidate for the project (idea, option, plan, structure, wording, design, analysis) that has not yet been committed to? | Design: formulation/synthesis incl. externalised structure, documentation [S013]; development phase search/design [S008] |
| D | Decision | Does the move commit the project to something (choose, accept, reject, fix scope/goal/constraint, terminate)? | Intelligence-design-choice [S007]; identification/selection, evaluation-choice, authorisation [S008] |
| M | Metacognition | Does the move monitor or regulate *how the work is being done or how reliable it is* (checking, error detection, planning the process, calibrating confidence)? | Metacognitive knowledge/experiences/goals/actions [S022]; GenAI metacognitive demands: prompt formulation, iteration, output evaluation, automation strategy [S059]; decision control as "meta-decision-making" [S008] |

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
- (HYPOTHESIS) Appraisal and choice are not split: in Mintzberg et al. evaluation and choice were separable in only 18 of 83 instances [S008]. Pure evaluative judgment without commitment goes to M1 if it concerns correctness/reliability, otherwise to D2 if it states acceptability.

M (metacognition)
- M1 Monitor: checks, verifies, detects an error or gap, asks for status or evidence, flags that something was not read/verified.
- M2 Regulate: plans or reorders the process, decomposes the task, changes strategy or tooling, sets process rules (e.g. recording, verification protocol), delegates/instructs how to work.
- M3 Calibrate: states uncertainty, limits, confidence, or provenance of its own output.

## 3. Decision rules for boundaries

R1 **Object vs process.** A move that changes *what the research product is or contains* is K/P/D. A move about *how we work or how reliable the work is* is M. Test: "if removed, would the paper/data/codebook differ, or only the way we produced and checked it?"
R2 **Proposal vs decision.** Proposals offer; decisions commit. A human saying "I think we could do X" is P; "do X" / "yes, use X" is D2. An AI producing a draft is P3 until a human adopts it (the adoption is a separate D2 move).
R3 **Knowledge vs proposal.** K states what is (or is claimed to be) the case or how something works. P states what we could do or produce. A synthesis of a literature that only reports it is K2; a synthesis that recommends a design is split into K2 + P.
R4 **Verification.** Checking correctness of a claim or output = M1. The *fact found by checking* (e.g. "Crossref shows the title is X") = K1 as a separate move if it is reported.
R5 **Multi-function utterances.** Segment into moves (Section 5). If still mixed, code the **dominant function** and record the secondary code in `secondary`. Tie-break: code to the later of K -> P -> D (Garrison's code-up logic for multi-phase messages [S029], adapted; HYPOTHESIS).
R6 **Direction setting.** Setting the topic, scope or requirement is D1 even if phrased as a question; asking for information is K only if it supplies content, otherwise it is coded by its function: a question that directs the work is M2 or D1 depending on R1.
R7 **Corrections.** A human correcting an AI error: the detection is M1; the instruction to redo is M2; the replacement content, if the human writes it, is P/K with actor = human and flagged `manual_change` (CFP requires such changes be disclosed).

## 4. Attributes recorded for every move (observables only)

| Attribute | Values | Why |
|---|---|---|
| actor | human / AI-primary-agent / AI-subagent | Actor is derived from session lineage and message source, **not** from `role=user` (in child sessions the user message is the parent AI's prompt; event E013). |
| session, message_id, part | ids | Traceability. |
| type, subtype, secondary | codes above | |
| stage | problem formulation, literature, theory, design, analysis, interpretation, writing, verification, revision, governance, tooling | Mirrors the CFP's required contribution account (problem formulation, literature, theory, research design, analysis, interpretation, writing, verification, revision). |
| origin | new / responds-to(move_id) | Provenance chain. The idea of tracing idea origin and uptake through links between moves comes from linkography and grounding research, which we have NOT read (S053, S054 not accessible); treat as our own design, not as grounded in them. |
| uptake (coded on the responding move) | adopted / adopted-modified / rejected / questioned / no-response | Distinguishes who *proposed* from who *committed*. Initiative as a trace concept is supported by Walker & Whittaker's abdication/repetition/interruption control shifts [S058]. |
| epistemic_transfer (K moves) | explicit-new (receiver states it was new or changes behaviour based on it) / no-evidence | Captures the paradigm shift in I012 in observable form. Absence of evidence is not evidence of non-novelty. |
| manual_change | yes/no | A human hand-edit not mediated by the AI (disclosure requirement). |
| artifact | path(s) changed, if any | Links moves to products. |

## 5. Unit of analysis (HYPOTHESIS, to be fixed after pilot)

- Garrison et al. chose the message as unit because it is clearly demarcated, length is decided by the author, and it gives enough information to infer the process; they warn that sub-message units are harder to identify reliably [S029].
- Agentic AI turns break that assumption: one assistant message can contain a summary, a proposal, a decision request and many tool calls.
- **Proposed unit: the move** = a contiguous span of one message/part that realises one dominant function. Segmentation rule: a new move starts when the function changes under R5. Tool calls are coded X unless the call *is* the content (e.g. a verification query whose purpose is M1; then the parent move is coded M1 and the call is an indicator).
- Pilot compares message-level vs move-level on agreement (Krippendorff's alpha with bootstrap CI, minimum fixed before coding [S061, partial]).

## 6. Codebook entry format (after MacQueen et al. [S064])
Each code: code, brief definition, full definition, when to use, when NOT to use, examples. Entries below are brief definitions only; full entries are produced during pilot iteration. Pre-registered procedure: independent double coding; every disagreement diagnosed as coder error vs definition problem; recode; single codebook editor [S064].

## 7. Worked examples from this project's own record (for calibration; coded by the drafting AI, NOT reliable)

| Move (paraphrase) | Actor | Code | Note |
|---|---|---|---|
| Human forwards the call-for-participation email and proposes the topic | human | D1 (also K4 for the email) | Topic selection; primary D1. |
| Human: "records must cover other agents, sub-agents, new sessions, with model and framework" | human | D1 | Requirement for the product/appendix. |
| Human: "cognition's externalized form is what must be modelled; the two of us cannot guess it; first survey the literature" | human | M2 (redirect) + D1 | Disputable under R1: it changes how we justify the framework (process) and the research design (object). Pilot will show disagreement. |
| AI proposes a function x stage x attribution taxonomy from memory | AI | P2 | Later abandoned (E008). |
| AI reports it read only abstracts for 12 sources | AI | M3 | Calibration of its own output. |
| Sub-agent reports Amershi not "Amershal" | AI-subagent | M1 (detection) + K1 (the corrected fact) | Two moves. |
| Human: "knowledge should be a type because AI supplies new knowledge to experts" | human | P1/K2 | Reasoned claim about the construct; arguably P1 (proposes the frame). Boundary case K2 vs P1. |
| AI revises the framework in response | AI | P4 | Responds-to the human move; uptake of human claim = adopted-modified. |

## 8. Known weaknesses (to disclose)
1. Only one project, one main AI model family; the same family produced most AI moves and will draft codes (self-preference risk; evidence from summarisation [S071]). Mitigation: blind actor/model labels where possible, a coder from a different model family, human double coding of a stratified subsample, report kappa/alpha per type.
2. Moves are unequal in weight; counts alone mislead. Planned complement: link moves to artifact changes (consequentiality). (HYPOTHESIS)
3. Human cognition that never reaches the trace (reading, thinking, offline conversation with the advisor, decisions made off-chat) is invisible. Reported as a limitation; partially covered by the human intervention log (records/logs/interventions.csv), which is itself a trace we create.
4. The M vs D vs P boundaries are expected to be the hardest (cf. exploration/integration confusion in Garrison; kappa rose from .35 to .74 over three rounds [S029]). Early low agreement is an expected finding, not a failure.
5. Several read copies are third-party/preprint versions; quotes must be re-checked before manuscript use.
6. Evaluation of the scheme as a design-science artifact [S072 third-party scan; S073 not read] is planned but not yet specified.
