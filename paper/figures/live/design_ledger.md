# Figure content ledger for the live Sivia rebuild

Session `ses_e9dd5da08ffe0Ul310mqUTSi6K` (2026-10-22). Both figures are rebuilt through the Sivia live
draw.io MCP tools (`drawio_live_*`), driven by `build_fig1.mjs` and `build_fig2.mjs`, with
`dxlib.mjs` holding the shared design tokens and drawing helpers.

## Why the rebuild

The published figures (`paper/figures/fig1_final.png`, `fig2_final.png`) were produced by a Python
generator that writes draw.io XML directly (event E045). This rebuild goes through the live graph API,
raises the minimum type size for print legibility and unifies the actor vocabulary.

## Shared decisions

| Decision | Value | Reason |
| --- | --- | --- |
| Canvas | 1440 x 960 px (Figure 1), 1440 x 900 px (Figure 2) | 6.15 in print width, so 1 px = 0.3075 pt |
| Type ladder | panel 26 px (8.0 pt), sub 24 px (7.4 pt), body 22 px (6.8 pt), small 20 px (6.2 pt) | the old figures used 14 px, about 4.3 pt, which is below print legibility |
| Actors | Human, Primary agent, Sub-agents | the old Figure 2 said only "AI"; the paper says primary AI agent and sub-agents |
| Coder identity | Coder A and Coder B in the figure, GPT and Gemini in the caption | Table 1 and the appendix carry the model names |
| Connectors | orthogonal, arrowhead touching a boundary, no line through a label | live audit rule `arrowhead-intrusion` and `connector-path-through-object` |
| Charts | schematic, labelled `schematic` | a reader could otherwise mistake the bars for measured data |
| Numerals in Figure 1 | none | Figure 1 is the method overview; the numbers live in Tables 1 to 4 |
| Numerals in Figure 2 | the six coder count pairs only | these are the reference counts of the transition analysis |
| Elements | reuse of `paper/figures/elements_b` and `elements_c` | one shared style, already cut out and QA-passed; the working Azure deployment is kept for a missing glyph (event E048) |
| Title inside the figure | none | the caption carries the title |

## Figure 1. From recorded sessions to qualitative analysis

Message: recorded sessions become units, units carry actor and type tags, and the tagged units answer
existence, distribution and transition questions, while every manuscript revision feeds new sessions
back into the record.

Reading order: left to right along the top band (Recorded project, Units, Tags), then the lower band
(Existence, Distribution, Transition), then the return lane.

Canvas 1440 x 1000 px. The top band holds panels A (36 to 496), B (510 to 810) and C (824 to 1432);
the lower band holds D (36 to 490), E (506 to 960) and F (976 to 1432).

| Region | x range | Content |
| --- | --- | --- |
| A Recorded project | 36 to 496 | head with the human icon, `Human`, `Primary agent` and the agent icon; a chat timeline of eight turns read from the recorded session, the human turns stacked on the left, the agent turns on the right, a grey spine in the middle with one dot per turn, a tool-step row of three gears, and an export row of the pages and manuscript icons with the label `exported records` |
| B Units | 510 to 810 | rule label `One response per unit`; four unit cards, the human unit facing left and the agent units facing right, tool-step gear rows merged into the following bubble, a spawned sub-agent pair, a dotted cut line with scissors and the label `Units are linked only within one session` |
| C Tags | 824 to 1432 | left zone 836 to 1088: one unit under review with the three tool gears, a fork to Coder A and Coder B, their tag chips, a multi-tag unit and the coding manual; right zone 1100 to 1420: the agreement block with percent agreement, Cohen's kappa and Krippendorff's alpha, the four type tiles with their one-line definitions, the execution marker and the boundary rule `Product changes` / `Only the process changes` |
| D Existence | 36 to 490 | matrix of three actors by four types, a filled dot for a pair both coders tag, a mixed-contribution scene with a check badge, `schematic` label |
| E Distribution | 506 to 960 | grouped bar chart of four types by actor, stage strip of nine stage icons, `schematic` label |
| F Transition | 976 to 1432 | human and agent lanes, five type chips in zigzag order with arrows, `Interaction modes` legend of three arrow glyphs, `schematic` label |
| Return lane | 8 to 1432 | manuscript icon at the right, label `Each revision adds sessions and the coding is repeated`, single arrowhead into panel A |

Bubble shape, decided after the human review of the v1 PNG (intervention I034): a plain rounded
rectangle with `arcSize=18` and a triangle tail on the speaker's side. The draw.io callout shape was
dropped because its wavy speech-bubble outline and its downward pointer read as an odd shape in print.
The tail is drawn first and covered by the body, so the body outline hides the base edge of the triangle.

Panel A layout, decided after the human review of the v2 draft (intervention I035): the two speakers
are separated, but the turns of one speaker stack on that side instead of alternating one by one, and
the empty areas are removed. The eight turns are the opening of the recorded session, abridged into
English. The measured result is 87 percent content rows in panel A with a largest empty band of
12 px, 87 percent in panel B, 99 percent in panel C, and no empty band above 21 px in any panel.

Existence matrix values follow the agreed counts in `research/coding/final/existence.csv`:
Human K, P, D, M present; Primary agent K, P, D, M present; Sub-agents K, P, M present, D absent.

## Figure 2. Six interaction modes, a worked case and mixed contribution

Message: transitions fall into six recurring interaction modes, and a mixed contribution appears when
both actors add explicit content to the same output.

Canvas 1440 x 900 px. Panel G (8 to 844) holds the six lanes, panel H (856 to 1432) the worked case,
panel I (8 to 1432, 608 to 892) the mixed contribution and the bare approval.

| Region | x range | Content |
| --- | --- | --- |
| G Six interaction modes | 8 to 844 | column headers `Human` and `Primary agent`, six numbered lanes with a type tile per side, a direction arrow in the middle, the mode name and the two coder counts, a note that the arrow points from the earlier unit to the later one |
| H Worked case | 856 to 1432 | `Human` and `Primary agent` headers, a grey spine, four numbered cards in zigzag order with the messages `25 sources read in full.`, `Knowledge is one dimension.`, `Framework v0.1 drafted.` and `A round may mix tags.`, each with its type tile, and the `Typology` output with two gears |
| I Mixed contribution | 8 to 1432 | left half `Both add content` with a human and an agent bubble, two arrows into a checked `Typology` output and the note `Both actors changed the output.`; right half `Bare approval` with the agent bubble, a short `OK.` bubble, a solid arrow into a grey output and a dashed arrow that carries no content, with the note `The approval adds no content.` |

Lane data from `research/coding/final/transitions.csv`, counts as coder A (GPT) and coder B (Gemini):

| Lane | Mode | Chips | Direction | Counts |
| --- | --- | --- | --- | --- |
| 1 | Direction and drafting | Human Decision, agent Proposal | human first | 8, 6 |
| 2 | Proposal and commitment | agent Proposal, Human Decision | agent first | 7, 6 |
| 3 | Supply and reframing | agent Knowledge, Human Decision | agent first | 1, 3 |
| 4 | Regulation and response | Human Decision or Metacognition, agent Metacognition | human first | 8, 9 |
| 5 | Challenge | agent Proposal, Human Metacognition | agent first | 2, 4 |
| 6 | Autonomous work | agent Metacognition, agent Knowledge | agent only | 39, 22 |

The counts of lane 4 are the sum of `H:D -> AI:M` (3, 6) and `H:M -> AI:M` (5, 3), the counts of lane 6
the sum of `AI:M -> AI:M` (32, 12) and `AI:M -> AI:K` (7, 10). The arrow in a lane points from the
earlier unit to the later one, so lane 1 points to the right and lane 2 to the left. Lane 6 has no human
turn and carries its arrow between the two agent tiles.

The worked case in panel H follows the recorded session: the agent's report on the readings (S01-U031),
the human's reframing of Knowledge as a type (S01-U032), the agent's framework and codebook draft
(S01-U034), the human's ruling on the coding unit and on evaluation (S01-U035) and the resulting
typology (S01-U039). The bubble texts are abridged English renderings of those messages.

Terminology fix carried by this rebuild: the old figure called the agent side "AI" and gave the
worked case the generic label `AI lane`. The rebuild names the two lanes `Human` and `Primary agent`
and keeps the coder identity in the caption.

