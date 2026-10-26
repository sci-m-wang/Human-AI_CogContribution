# Evidence synthesis v1 (grounded only in sources actually read)

Status: DRAFT for human review. Date 2026-10-21. Author: openwork/claude-sonnet-5.5 (session ses_ea32c9901ffe7o77BUt54LtH2Q).
Rule: every statement below cites a note in `research/fulltext/` whose ACCESS is FULLTEXT_READ or PARTIAL (flagged). Parent agent spot-checked S008, S029 (read directly), S049, S068, S071. Other notes are sub-agent reports, not independently re-read. Many copies are third-party/preprint versions: verify quotes against licensed versions before the manuscript.
Access summary (research/source_access_status.csv): FULLTEXT_READ 25, PARTIAL 9, ABSTRACT_ONLY 12, NOT_ACCESSED 8.

## 1. What the read sources say about the *forms* of cognition

| Finding | Source (note) | Consequence for our scheme |
|---|---|---|
| Revised Bloom is a **two-dimensional table** (cognitive process x knowledge type), the hierarchy is explicitly relaxed; knowledge types: factual, conceptual, procedural, metacognitive; processes: remember, understand, apply, analyze, evaluate, create; it classifies *intended objectives*, not what learners did | S001 | "Knowledge" is a **dimension** crossing the process axis, not a peer of process types. The human's folk type "knowledge" maps to this dimension. |
| Knowledge types: situational, conceptual, procedural, strategic; "declarative" is a *quality* (vs compiled), not a type | S002 | Do not code "declarative knowledge" as a contribution type. |
| Simon: exactly 3 phases (intelligence, design, choice); execution is more decision-making; recursive; choice may be "almost pro forma" | S007 (OCR copy of 1960 book; clean-copy check needed) | Decision is a process with upstream stages; "choice" alone is a thin act. |
| Mintzberg et al.: 12 elements (3 phases, 3 supporting routines, 6 dynamic factors); recognition, diagnosis, search, design, screen, evaluation-choice, authorisation; decision control = "meta-decision-making"; recycling in all 25 processes (95 recycles); evaluation and choice separable in only 18 of 83 instances; diagnosis and design called most important; supporting routines leave "little trace" | S008 (reprint; read by parent) | (i) Evaluate vs choose is hard to separate in observed data -> expect low reliability if split; (ii) meta-decision/control and diagnosis are exactly the parts that are poorly visible in traces; (iii) coding must allow cycling, not a linear phase model. |
| Gero & Kannengiesser FBS: function/behaviour/structure; processes formulation, synthesis, analysis, evaluation, documentation, reformulation; synthesis explicitly includes externalising structure (sketching) | S013 (Wayback copy) | Design-protocol precedent: "expression" is a *process of making structure* (synthesis/documentation), not a separate cognitive type. |
| Kirsh & Maglio: epistemic action defined cognitively (reduces space/time/unreliability of mental computation); the epistemic motive is **inferred**, players did not report it | S014 | Supports treating externalisation as part of thinking, and warns that motive attribution is an inference step we must flag. |
| Clark & Chalmers: coupling conditions (constancy, availability, automatic endorsement, past endorsement); a one-off lookup does not qualify | S016 | Whether the AI counts as part of the human's cognitive system is conditional; keep "who contributed" as an observable-trace question, not a metaphysical one. |
| Risko & Gilbert: offloading is action-based, a metacognitive feedback model, often occurs with no objective benefit | S017 | Offloading is an *attribute of a human-AI interaction* (what was handed over), not a cognitive type. |
| Flavell: four classes - metacognitive knowledge, experiences, goals/tasks, actions/strategies; knowledge splits person/task/strategy | S022 | Monitoring, redirecting, verifying are metacognition; needs its own place. |
| Tankelevitch et al. 2024: GenAI imposes metacognitive demands: prompt formulation, iteration, output evaluation, automation strategy; models the *user only*, conceptual paper, no coding | S059 | Gives a candidate human-side metacognitive vocabulary; no AI side, no reliability. |

## 2. What the read sources say about coding *observable* traces

| Finding | Source | Consequence |
|---|---|---|
| Garrison et al.: 4 phases (triggering event, exploration, integration, resolution) + "other"; **message-level unit**; latent processes are not reliably codable, so they derived manifest *indicators* + attitude *descriptors*; "code down/up" tie-break rules; kappa .35, .49, .74 over 3 rounds (CR .45/.65/.84), 95 messages, 2 coders; main confusion exploration vs integration; authors call the target "latent projective" | S029 (manuscript copy, read by parent) | Template for our procedure: latent construct -> indicators -> tie-break rules -> multi-round reconciliation; expect low early kappa. Message unit too coarse for agent turns. |
| Walker & Whittaker: initiative coded via utterance types (assertion, command, question, prompt) and control shifts (abdication, repetition/summary, interruption); no reliability reported; codes *who holds initiative*, not cognitive quality | S058 | Gives an observable operationalisation of **who leads** and uptake; initiative != cognitive contribution. |
| Handa et al. (Anthropic): unit = one conversation; 5 collaboration patterns (directive, feedback loop, task iteration, learning, validation) grouped automative/augmentative; 57% augmentation vs 43% automation; human validation in appendix not read; cannot see how outputs are used | S049 (main text; read by parent) | Closest *method* relative; differs in unit (conversation), scope (population, no project), axis (delegation style, not cognitive type of each party). |
| Clio: facets Request/Language/Task/Concerning; no cognitive scheme; summary accuracy 96%, Spearman .84 etc.; no kappa/alpha; cannot determine intent | S060 | LLM-as-analyser of conversations has precedent but validation reported as accuracy, not chance-corrected. |
| Vaccaro et al. 2024 (partial): 106 experiments, 370 effect sizes; human-AI combination worse than the best of either (g = -0.23), better than human alone (0.64); decision tasks g = -0.27; creation g = 0.19 (n.s. in the note) | S035 (PARTIAL) | Motivates *type of cognitive work* as a moderator; supports the decision/content-creation distinction at task level. Confirm numbers against full text. |
| Lee et al. CHI 2025 (partial): n=319, 936 examples; higher confidence in GenAI associated with less critical thinking; work shifts toward verification, integration, stewardship | S047 (PARTIAL) | Human contribution shifting toward verification/integration — a hypothesis to test in our data, from self-report. |
| CoAuthor (partial): 1,445 sessions, 63 writers; 72.6% of final text by writers; suggestion acceptance 72.3% | S051 (PARTIAL) | Trace-level human/AI attribution exists for text edits only. |
| Costa et al. 2025 (abstract only): AbductivAI model, human as "reflexive agent", AI as analytical partner / participant in distributed cognition, tested on 323 abstracts | S075 (ABSTRACT_ONLY) | **Near neighbour, unread: novelty claim vs this paper is not permitted until the full text is read.** |

## 3. Method sources (read)

- Codebook entry (MacQueen 1998, S064): code, brief definition, full definition, when to use, when not to use, examples; double-code, diagnose disagreement as coder error vs definition problem, recode; agree criteria in advance; one codebook editor; staged coding above ~40 codes.
- Reliability (S061 partial): Krippendorff's alpha with bootstrap CI; minimum alpha set before coding; the 0.667/0.80 convention is NOT in that paper (do not attribute it to Hayes & Krippendorff 2007).
- Human-AI coding precedent: CoAIcoder (S069 partial, preprint): kappa .16-.31 (phase 1) -> .51-.65 (phase 3); Xiao et al. (S068): GPT-3 vs expert kappa .61 (binary) and .38 (4 categories) vs expert-expert .88/.90; codebook-centred prompts best; "design codebooks for LLMs".
- LLM self-preference (S071): self-recognition and self-preference correlate; label-swap changed GPT-4 self-preference 0.73 -> 0.32 on XSUM; recommended mitigations in our setting: blind labels where possible, at least one different-family coder, both orders/repeats, human adjudication subset; evidence is for summarisation quality, not contribution coding.
- Design science (S072 third-party scan; S073 abstract only): frame the codebook as a method/model artifact; evaluation methods (observational, analytical, experimental, testing, descriptive).
- Single case (S074 Eisenhardt; S076 Lee & Baskerville): generalise from description to theory (type ET), not to other settings by sample size.

## 4. Provisional implication for the framework (NOT a decision; for discussion)

1. The three folk types do not sit on one axis: "knowledge" is a **dimension** (S001, S002); "decision" is a **process family** with upstream diagnosis/design and cycling (S007, S008); "expression/design" is the **making of externalised structure** (S013, S014).
2. A contribution should therefore be describable by at least: **what cognitive process it performs** (process axis) x **what kind of content/knowledge it concerns** (knowledge dimension), plus **provenance attributes** (who originated; how it was taken up) that are observable (S058; linkography and grounding sources still unread).
3. **Metacognitive control** (monitoring, redirecting, verifying) needs an explicit place (S022, S008 decision control, S059).
4. Evaluate vs choose may not be reliably separable in traces (S008: 18/83); decide by pilot kappa, not a priori.
5. Unit: message-level is the precedent (S029) but agentic turns need sub-turn "move" units; this must be decided and justified in the codebook (actor rule: in child sessions role=user is the parent AI, event E013).

## 5. Still unread and needed (human help requested)
S020 Chi & Wylie 2014; S021 Chi 1997; S028 Ericsson & Simon 1980; S025 Klahr & Dunbar 1988 (abstract only); S012 Dorst & Cross 2001 (abstract only); S053 Clark & Brennan 1991; S054 Goldschmidt linkography; S057 Hesse et al.; S063 Campbell et al. 2013; S073 Gregor & Hevner 2013; S075 Costa et al. 2025 (CC-BY, SAGE blocks scripts); S040 Dell'Acqua et al.; S056 Weinberger & Fischer 2006 and S055 ENA (open PDF, blocked by CAPTCHA for scripts).
