import json, csv, os, re, sys, time, urllib.request, urllib.parse
sys.path.insert(0, r'<project>\research\tools')
from docx_builder import build
ROOT = r'<project>'
CODING = os.path.join(ROOT, 'research', 'coding', 'final')
FIG = os.path.join(ROOT, 'paper', 'figures')
OUT = os.path.join(ROOT, 'paper')

# ---------- numbers from the run 2 analysis outputs (see paper/numbers_v4.py), each one asserted
sys.path.insert(0, os.path.join(ROOT, 'paper'))
import numbers_v4 as N
from numbers_v4 import T1, T3, T_COD, T_EX, E, A
RISK = json.load(open(os.path.join(ROOT, 'research', 'references_is_v3.json'), encoding='utf-8'))
assert (N.N_UNITS, N.N_BY['human'], N.N_BY['AI-primary'], N.N_BY['AI-subagent'], N.N_PRIMARY_RESP, N.N_PROMPT, N.N_SESSIONS) == (265, 38, 187, 40, 177, 10, 13)
assert (A('human', 'D'), A('human', 'M'), A('human', 'K'), A('human', 'P')) == (28, 25, 12, 3)
assert (A('AI-primary', 'K'), A('AI-primary', 'P'), A('AI-primary', 'D'), A('AI-primary', 'M'), A('AI-primary', 'X')) == (40, 22, 4, 106, 68)
assert (A('AI-subagent', 'K'), A('AI-subagent', 'D'), A('AI-subagent', 'M')) == (10, 0, 12)
assert N.AI_D_UNITS == ['S01-U185', 'S03-U001', 'S04-U001', 'S05-U001'] and not N.BAD_EXEMPLARS
assert N.MODES == {1: (9, 9), 2: (9, 12), 3: (3, 4), 4: (17, 17), 5: (3, 4), 6: (85, 62)} and N.REPORT_COMMIT == (7, 6) and N.TRANS_TOTAL == (165, 146)
assert (N.N_EP, N.N_LONG, N.LONG_UNITS, N.EP_UNITS, N.MEDIAN_RUN) == (38, 11, 120, 177, 2.5) and N.LONG_XM == {'gpt': (113, 120), 'gemini': (110, 120)}
assert N.FATE_D == {'gpt': 19, 'gemini': 18} and len(N.FATE_LATER) == 21 and len(N.FATE) == 22
assert (N.PRIM_ALL, N.PRIM_146_R2, N.PRIM_146_R1) == (226, 122, 112) and len(N.T3) == 14
assert N.RT['gpt'][0] == 90 and N.RT['gemini'][0] == 95
assert N.RT['gpt'][1] == 79 and N.RT['gemini'][1] == 79
assert N.stage_tot('human')[0] == 68 and N.stage_tot('human')[1]['design'] == 20 and N.stage_tot('AI-primary')[0] == 172 and N.stage_tot('AI-subagent')[1]['literature'] == 16
assert round(min(float(r['kappa']) for r in N.AGMAIN), 2) == 0.22 and max(abs(float(r['alpha']) - float(r['kappa'])) for r in N.AGMAIN) < 0.04
T2 = [['Output', 'AI contribution', 'Human contribution', 'Mode'],
      ['Four-type typology', 'Literature synthesis (S01-U031), framework draft (S01-U034)', 'Knowledge as a type, Proposal replaces design (S01-U032)', 'AI Knowledge, human Proposal'],
      ['Unit of analysis', 'Draft rule (S01-U039), operational rule (S01-U042)', 'One model response as the unit (S01-U040)', 'Human Decision, AI Proposal'],
      ['Research questions', 'Candidate questions (S01-U069, S01-U072)', 'Three questions with reasons (S01-U070)', 'Human reformulation'],
      ['Mixed criterion', 'Draft criterion (S01-U072)', 'Same-output rule, no bare approvals (S01-U073)', 'Human reformulation'],
      ['Literature base', 'Surveys and notes (S01-U019, S01-U031)', 'Survey first, originals, skip closed sources (S01-U017, S01-U020, S01-U032)', 'Human Metacognition, AI Knowledge'],
      ['Figures 1 and 2', 'Whole-figure drafts, rebuilds (S01-U149, S01-U167)', 'Concrete examples, side tails (S01-U164, S13-U025, S13-U032)', 'Human reformulation'],
      ['Framing of the paper', 'Comparison with IS papers (S01-U174)', 'Co-author\u2019s comment, choice of option A (S01-U168, S01-U175)', 'Human reformulation']]
P = []
ORDER = ['dist', 'mixed', 'prop']
TN = {k: i + 1 for i, k in enumerate(ORDER)}
T_PROP = [['Proposition', 'Evidence in the case', 'Evidence that would count against it'],
          ['**P1 Bounded delegation.** A run of AI work opens with a human scope and ends in a hand-back to the human.',
           '11 of 38 runs hold 120 of 177 primary-agent responses, and 113 (GPT) and 110 (Gemini) of those are Execution or Metacognition. Of 9 long runs followed by a human message, 5 ended with a report and 4 with an intervention.',
           'Long runs that end with neither a report nor an intervention.'],
          ['**P2 Retained commitment.** Responsibility for tasks can move to the AI while accountability for the direction stays with the human.',
           'Decision in 28 of 38 human units and 4 of 187 primary-agent units. After an AI Proposal the human message carries a Decision in 19 and 18 of 21 cases.',
           'AI Decisions that set goals or scope and stand without human adoption.'],
          ['**P3 Knowledge-induced reframing.** Knowledge from one party changes the other party\u2019s construct or route when it fills a gap behind a pending decision.',
           'AI to human: S01-U031 to S01-U034 and S01-U044 to S01-U045. Human to AI: S13-U006 and S13-U010.',
           'Knowledge supply that leaves the construct or route unchanged although a decision is pending.']]

def p(t): P.append(('p', t))
def h1(t): P.append(('h1', t))
def h2(t): P.append(('h2', t))
def box(lines): P.append(('box', lines))

P.append(('title', 'Who Contributes What in Human-AI Research? A Qualitative Case Study of a Project That Analyses Itself'))

h1('Introduction')
p('Generative AI now takes part in every stage of scholarship, from the formulation of questions to the writing of manuscripts. Information systems (IS) researchers have begun to chart how the field should conduct its own work with it (Susarla et al., 2023). The call for this workshop asks every submission for a human-AI contribution account that covers nine research functions (ICIS 2026 PDW on Autonomous Scholarship, 2026). Current disclosure practice answers with a list of tasks, which shows activity and hides the kind of thinking behind it. A draft by the AI may rest on a scope that the human fixed, and an approval by the human may follow a framing that the AI proposed.')
p('The hidden layer matters for IS theory as well as for disclosure. IS research describes the division of labour between humans and AI mainly through delegation. Baird and Maruping (2021) offer delegation to and from agentic artifacts as a lens, Fügener et al. (2022) show that humans delegate knowledge work to AI poorly, and Seeber et al. (2020) treat machines as teammates. These accounts describe what is handed over and with what result. They leave open what each party thinks, so two widely held worries rest on assertion. One says that humans become unnecessary once AI can execute a research workflow. The other says that AI is an execution tool with no ideas of its own.')
p('This paper asks one plain question about this new kind of work and studies it where the full trace is available, in the project that produced the paper. The question is how humans and AI share the thinking when they do research together. Three sub-questions refine it.')
P.append(('bullets', ['**RQ1 Existence.** What kinds of thinking does each party contribute, and do some outputs draw on both?',
                      '**RQ2 Passing.** How does the thinking pass between the two as the work proceeds?',
                      '**RQ3 Explanation.** What explains this division and this sequence?']))
p('A human orchestrator directed AI agents in the project, and every session was recorded as it happened. The sessions are therefore both the data and the history of the manuscript\u2019s own production. We build a typology of observable cognitive contributions and code 265 units with two LLM coders from different model families. Human, AI and mixed contributions all exist. The human holds commitment and steers the process, the AI supplies knowledge, candidate proposals and verification, and seven outputs carry explicit contributions from both. The sequence follows a cycle of delegation, generation and commitment, which we state as three propositions.')
p('The paper makes three contributions to IS research. It offers a typology of observable cognitive contributions that treats knowledge as something an AI can supply. It offers a delegation and commitment account that explains why contributions divide and pass as they do, stated as propositions that other projects can test. It also provides a trace-based coding standard that makes the account inspectable.')

h1('Theoretical Background')
h2('Human-AI Work in Information Systems Research')
p('IS research frames the division of labour between humans and AI through delegation, configuration and performance. Baird and Maruping (2021) argue that agentic artifacts can take responsibility for tasks with ambiguous requirements and propose delegation to and from them as the organising lens. Fügener et al. (2022) show that humans misjudge their own metaknowledge and delegate knowledge work to AI poorly. Gr\u00f8nsund and Aanestad (2020) trace how humans and an algorithm were configured and reconfigured in one organisation. Seeber et al. (2020) set out a research agenda for machines as teammates, and Berente et al. (2021) name autonomy as a facet that managers of AI must decide. Automation and augmentation are intertwined (Raisch & Krakowski, 2021). A meta-analysis finds that human-AI combinations on average perform worse than the better party alone, with losses in decision tasks and gains in content creation (Vaccaro et al., 2024).')
p('Trace-based studies of what each party does are fewer. Handa et al. (2025) label conversations as automative or augmentative, and CoAuthor records keystroke-level co-writing in which writers produced 72.6% of the final text (Lee et al., 2022). Survey evidence suggests that effort shifts toward verification, integration and stewardship when workers use generative AI (Lee et al., 2025). In science, AI Co-Scientist assigns generation, critique and refinement to agents while scientists set goals and review results (Gottweis et al., 2026), and Lu et al. (2024) automate a whole machine learning research pipeline. Costa et al. (2025) describe a qualitative workflow in which the AI acts as analytical partner and the human as reflexive agent. These works describe contributions by task, outcome or role. We found no study that types the cognitive kind of each party\u2019s contribution across a whole project or explains why the work divides as it does.')
p('Coding schemes for related objects exist. Cognitive presence codes four phases of inquiry at message level among human participants (Garrison et al., 2001). Initiative coding records who holds control and leaves content aside (Walker & Whittaker, 1990). The typology below borrows the indicator logic of the first and the observable stance of the second.')
h2('A Typology of Cognitive Contributions')
p('The typology rests on cognition research. Cognitive taxonomies separate processes from knowledge types (Krathwohl, 2002), and knowledge divides into situational, conceptual, procedural and strategic kinds (de Jong & Ferguson-Hessler, 1996). Decision research describes choice as intelligence, design and choice (Simon, 1960), and Mintzberg et al. (1976) found evaluation and choice separable in only 18 of 83 instances. Design research treats externalised structure as part of thinking (Gero & Kannengiesser, 2004), and epistemic actions reduce the burden of mental computation (Kirsh & Maglio, 1994). Metacognition spans knowledge, experiences, goals and strategies (Flavell, 1979), and generative AI adds the demands of prompting and output evaluation (Tankelevitch et al., 2024). People hand cognitive demands to external resources according to a metacognitive evaluation of those demands (Risko & Gilbert, 2016).')
p('Two properties of these sources shape the typology. First, they place knowledge in the thinker, so that evaluation, choice and design operate on what the thinker already holds. When an AI agent supplies knowledge that a human expert did not hold, knowledge becomes something that is contributed, and we treat Knowledge as a type. Second, cognition is inferred from what is observable. Garrison et al. (2001) derived manifest indicators for each latent phase of inquiry, and we classify what a move does in the shared record.')
p('A cognitive contribution is an externalised move by an actor that adds to or changes the shared research state and can be identified from the trace. Figure 1, in the next section, shows the types and the pipeline in which they are used. Knowledge introduces a fact, concept, method or situational context. Proposal offers a candidate, such as a frame, structure, text or revision, that is not yet committed to. Decision commits the project by setting a goal, scope or constraint, or by selecting, rejecting or stopping an option. Metacognition checks or steers how the work is done and how reliable it is. Execution carries out a specified step without new content. Evaluation and choice form one type, since evaluation usually carries preference.')
p('One rule separates object from process. If removing a move would change the product, the move is Knowledge, Proposal or Decision. If it would change how the product was made or checked, the move is Metacognition. Proposals offer and decisions commit, so an AI draft is a Proposal until a human adopts it, and the adoption is a separate Decision. The codebook defines subtypes and boundary rules for each type. Knowledge, for instance, divides into fact or source, concept or explanation, method or procedure, and situated context.')

h1('Research Design')
h2('Case and Data')
p('The case is the project that produced this manuscript, studied with the case research strategy established for IS (Benbasat et al., 1987). One human orchestrator directed a primary AI agent (claude-sonnet-5.5), which dispatched sub-agents on the same model to survey and read literature. Every session was exported with message-level provenance, model, agent name and parent session. The corpus comprises 13 sessions, namely the ideation session, the main working session, ten sub-agent sessions and a second primary-agent session that redrew the figures. These yield 265 units, of which 38 are human messages, 177 are primary-agent responses, 10 are primary-agent prompts to sub-agents and 40 are sub-agent responses. The corpus ends at the human message that asked for the recoding reported here (S01-U186). Empty messages, continuation prompts and context summaries that the agent framework inserted were removed (27 units). The designer of the typology also produced most of the units that the typology classifies, so the case is reflexive.')
P.append(('image', os.path.join(FIG, 'fig1_final.png'), 5.6))
P.append(('caption', 'Figure 1. From recorded sessions (A) through units (B) and tags (C) to the analyses of existence (D), distribution (E) and transitions (F), from which the account of delegation and commitment is built. Bubble texts abridge project messages.'))
h2('Units and Coding')
p('A unit is one model response. A human unit is one human message. An AI unit is an assistant message that contains visible text or dispatches a sub-agent, together with the tool-only steps that precede it. Tool-only steps (999 of 1,225 assistant messages) serve as evidence for the unit that follows. A unit may carry several tags, each with an actor and a type, and at most one primary tag per actor. Each tag carries a stage label drawn from the workshop\u2019s research functions plus governance and tooling, and an evidence quotation. The codebook gives each code a definition, rules for use and non-use, and examples (MacQueen et al., 1998).')
p('Two independent coders, GPT-6.1-sol and Gemini-4-argon, coded every unit with the frozen codebook (version 1.1) as their instruction, as in the LLM annotation studies of Gilardi et al. (2023) and Xiao et al. (2023). Each ran in an isolated session with the codebook and the units, in chunks of up to 20. Each received the unit text, truncated at 2,500 characters, and an actor hint with model names masked. The primary agent designed the codebook and coordinated the coding, and the analysis uses the codes of the two coders alone. The human approved each codebook version and ruled on boundary cases. The coding standard is a method artifact in the design-science sense (Hevner et al., 2004).')
p('The coding was run twice. Run 1 coded the first 146 units. When the framing of the manuscript changed, run 2 recoded these units together with 119 later ones, as the project rules require at each larger revision. We report run 2 and state where run 1 differs.')
h2('Analysis')
p('We turn each question into observable terms. For RQ1, an actor-type pair counts as present when both coders assign it to at least one unit. A contribution is mixed when both actors add explicit expression to the same output that adds, changes or reasons about content, and bare approvals do not count. For RQ2, we order the cognitive units within each session, write each transition between consecutive units as actor and primary type, and group recurring transitions by content into interaction modes.')
p('For RQ3, we build theory from the case evidence in the manner of case research (Eisenhardt, 1989). We divide each session into delegation episodes, each beginning with a human message and holding the AI responses up to the next human message. We read the episodes against the codes to see what opens and closes a run of AI work, which party commits, and how knowledge changes a construct. The propositions generalise analytically (Lee & Baskerville, 2003). We report percent agreement, Cohen\u2019s kappa and Krippendorff\u2019s alpha with bootstrap intervals for each actor-type presence variable (Artstein & Poesio, 2008, Hayes & Krippendorff, 2007). We also compare the two runs on the 146 units that both coded.')

h1('Findings')
h2('What Each Party Contributes (RQ1)')
p('Human contributions occur in all four types (Table %d). Decision appears in 28 of 38 human units, Metacognition in 25, Knowledge in 12 and Proposal in 3. The human chose the topic, restricted the data to the project\u2019s own sessions, fixed the unit of analysis as one model response and set the research questions. Human Metacognition regulated the process, for instance by requiring every session to be recorded (S01-U001) and originals to be read (S01-U020). Human Knowledge was mostly situated context that only the human held, such as an image service that the AI had reported as unavailable (S13-U006). Human Proposals were rare and shaped core elements of the design (S01-U014, S01-U032, S01-U070).' % TN['dist'])
P.append(('table', T1, [1.3, 1.05, 1.05, 1.05, 1.1, 0.95]))
P.append(('caption', 'Table %d. Units with each type present in both coders\u2019 tags, with the count of each coder in brackets (GPT/Gemini).' % TN['dist']))
p('AI contributions occur in Knowledge, Proposal, Metacognition and Decision. The primary agent supplied Knowledge in 40 of its 187 units, for example an explanation of agreement coefficients (S01-U044). The sub-agents supplied it in 10 of 40 units, almost all of it literature. The primary agent offered Proposals in 22 units, among them candidate taxonomies (S01-U016), research questions (S01-U069) and the figure drafts (S01-U149). Its Metacognition (106 units) consisted of verification results, detected errors and statements about its own limits. Both coders agree on four AI Decision units. Three are task assignments to sub-agents. The fourth is the primary agent\u2019s decision not to repeat the coding after a revision (S01-U185), which the human overturned in the next message (S01-U186). The human therefore remained necessary, and the AI did more than execute.')
p('Mixed contributions exist in the project. We identified seven outputs to which both actors contributed with explicit expression (Table %d), and they show four collaboration modes. In the first, the AI supplies knowledge and the human builds a proposal on it. On the AI\u2019s literature summary, the human built the proposal to treat knowledge as a type (S01-U032). In the second, the human fixes a decision and the AI turns it into an operational proposal grounded in data, as when the unit of analysis was defined. In the third, the human reformulates an AI proposal. Three research questions replaced the AI\u2019s candidate set (S01-U070), and the figures and the framing of the paper followed the same mode. In the fourth, the human regulates how the AI supplies knowledge, for instance by requiring a survey first and the reading of originals. Two short human approvals, S01-U078 and S01-U080, left the proposed outputs as they were.' % TN['mixed'])
P.append(('table', T2, [1.2, 1.9, 2.1, 1.3]))
P.append(('caption', 'Table %d. Outputs with contributions from both actors and their collaboration mode.' % TN['mixed']))
h2('How Contributions Pass Between Parties (RQ2)')
p('Figure 2 groups the transitions between consecutive cognitive units within sessions. The two coders found 165 and 146 transitions, and six interaction modes recur. Direction and drafting (human Decision, then AI Proposal) and proposal and commitment (AI Proposal, then human Decision) form a loop that accounts for 18 and 21 transitions. The human sets or reframes a direction, the AI drafts, and the human commits or redirects. Supply and reframing (AI Knowledge, then human Decision) is rare, with 3 and 4 transitions. Regulation and response (human Decision or Metacognition, then AI Metacognition) accounts for 17 and 17 transitions, and challenge (AI Proposal, then human Metacognition) for 3 and 4. Autonomous work (AI Metacognition continuing or leading to AI Knowledge) is the most frequent mode with 85 and 62 transitions. A report followed by a human Decision occurs 7 and 6 times and lies outside the six modes.')
P.append(('image', os.path.join(FIG, 'fig2_final.png'), 5.3))
P.append(('caption', 'Figure 2. (A) Six interaction modes with the transition counts of Coder A (GPT) and Coder B (Gemini). (B) A worked case with the types both coders tagged. (C) Mixed contribution and bare approval. Bubble texts abridge project messages.'))
p('Five of the seven outputs in Table %d show an AI Proposal, a human Decision and a further AI Proposal in succession. The typology followed a related path in which AI-supplied knowledge preceded a human reframing, an AI draft and a human ruling (S01-U031 to S01-U035). A single pass of proposal and commitment, as in the short approvals of the last rounds, left an output that one actor shaped. The human reaches the AI mainly through direction and regulation, and the AI reaches the human mainly through proposals.' % TN['mixed'])

h1('A Delegation and Commitment Account (RQ3)')
p('The modes show what happens, and the account asks why the work takes this shape. Reading the 38 delegation episodes against the codes suggests a cycle of three parts. The human delegates a scope, the AI generates within it, and the human commits to or reformulates what the AI returns. Figure 3 shows the cycle with one message from the project for each step. Three mechanisms produce it, and Table %d states each as a proposition with its evidence and the evidence that would count against it.' % TN['prop'])
P.append(('image', os.path.join(FIG, 'fig3_final.png'), 6.5))
P.append(('caption', 'Figure 3. The cycle of delegation, generation and commitment, with the three propositions and one message of the project for each step. Message texts abridge the project messages.'))
p('The first mechanism is bounded delegation. Human Decisions and Metacognition open runs of AI work. The median run holds 2.5 AI responses. Eleven of the 38 runs hold 120 of the 177 primary-agent responses, and 113 (GPT) and 110 (Gemini) of these 120 carry Execution or Metacognition as the primary tag. Each long run began with a human message that fixed a multi-step piece of work. The instruction to read originals (S01-U020) opened 11 responses of source retrieval and checking, which ended in a synthesis (S01-U031). The instruction to dispatch the coders and, in our translation, \u201cwrite the complete one\u201d (S01-U045) opened 18 responses. They ended when the human stopped the AI from drafting the paper (S01-U064), because the AI had read the phrase as an instruction to write the paper (S01-U065).')
p('Nine long runs were followed by a human message. Five ended with a report of more than 1,000 characters that the human answered. Four ended while the AI was working in short steps, and in each the human stopped, rejected, corrected or extended the work (S01-U064, S01-U107, S01-U126, S01-U164). A run therefore ends with a hand-back to the human.')
p('The second mechanism is retained commitment. Decision appears in 28 of 38 human units and in 4 of 187 primary-agent units. Three of the four AI Decisions assign tasks to sub-agents inside a delegation. The fourth is the AI\u2019s own decision not to recode after the framing revision (S01-U185), and the human overturned it in the next message. The human message that follows an AI Proposal carries a Decision in 19 (GPT) and 18 (Gemini) of 21 cases, more often than the 74% for human messages in general. Commitment therefore belongs to the human role whatever the AI proposed. All three human Proposals came directly after an AI unit that carried Knowledge or a Proposal, and two reformulated what the AI had returned (S01-U032, S01-U070). The human stated at the start that execution follows a blueprint that the human draws (S01-U005), and the project rules, drawn from the call, state that humans orchestrate and remain accountable. Baird and Maruping (2021) note that agentic artifacts can assume responsibility for tasks. Here responsibility for tasks moved to the AI while accountability for the direction stayed with the human.')
p('The third mechanism is knowledge-induced reframing. AI-supplied knowledge changed a human construct twice. After the synthesis of the readings (S01-U031), the human stated that the content on cognition and its externalised forms had been unknown before and made knowledge a type of contribution (S01-U032). The AI then added a flag for knowledge transfer to the framework (S01-U034). After the AI explained agreement coefficients (S01-U044), the human decided to report several of them (S01-U045). In both cases a decision was pending and the human lacked a piece of knowledge that bore on it. The mirror case also occurs. The AI had reported that image generation was unavailable, the human supplied situated knowledge about an existing configuration (S13-U006, S13-U010), and the AI changed its route. Supply and reframing is rare among the transitions, yet each instance changed the design.')
p('The three mechanisms together produce mixed contributions. A run delivers Knowledge or a Proposal, and the human\u2019s commitment adds content in the form of a reframed construct, a replaced candidate set or a new rule. Each turn builds on the output that the other party left, which resembles the imbrication of human and material agencies that Leonardi (2011) describes. Where the commitment adds nothing, as in the short approvals S01-U078 and S01-U080, the output stays with one party.')
P.append(('table', T_PROP, [2.2, 2.6, 1.7]))
P.append(('caption', 'Table %d. Propositions of the delegation and commitment account with evidence from the case.' % TN['prop']))

h1('Discussion')
h2('Theoretical Contributions')
p('In Gregor\u2019s (2006) taxonomy, the typology is a theory for analysing, of the kind she calls a classification schema. The three propositions are a step toward a theory for explaining, which she describes as accounting for how and why events occur and which can take a process form. The account extends the delegation lens (Baird & Maruping, 2021). Delegation describes what is handed over, and the account adds what thinking comes back and which party holds the commitment. It also locates a different problem from the one that Fügener et al. (2022) study. Their humans misjudge what to delegate to AI, whereas the failures here lay in a wide reading of an ambiguous instruction (S01-U064) and in reports that the human found inaccurate (S01-U126, S01-U134).')
p('Treating Knowledge as a contribution type adds a direction to the human-in-the-loop picture. In the configurations that Gr\u00f8nsund and Aanestad (2020) describe, humans audit and alter the algorithm. Here the AI also changed the human\u2019s constructs, in at least two episodes. The account also raises a question for the performance literature. Combinations lose in decision tasks and gain in content creation (Vaccaro et al., 2024), and in this case the human kept the decisions while the AI produced much of the content. Whether retained commitment explains or counteracts the reported loss is open.')
h2('Implications for Practice and Governance')
p('Journals, conferences and workshops that require disclosure can ask for more than a task list. A disclosure can state who held the commitments, which runs of work proceeded between human messages and what scope bounded them, and which outputs combined contributions from both parties. Organisations that deploy AI agents can treat the scope statement and the closing report as control points, since the overreach in this case followed an ambiguous scope and two reports were inaccurate. The proposition on retained commitment gives accountability a concrete reading, since the human can be asked to answer for every Decision and every adopted Proposal in the record. The recoding of an extended corpus left the agreed presence of actor-type pairs nearly unchanged, so the standard can be applied again at each revision. Any project that keeps its sessions can produce such an account.')
h2('Limitations and Future Research')
p('The coding standard performed unevenly, and the unevenness is informative. Kappa between the two coders ranged from .22 to 1.00 across the actor-type presence variables, and alpha stayed within .04 of it (Appendix Table A8). Human Knowledge (1.00), Metacognition (.92) and Decision (.91) and primary-agent Metacognition (.91) were highest. Primary-agent Decision (.22) and Knowledge (.44) were lowest, because GPT tags Knowledge in 99 of the 187 primary-agent units and Gemini in 42, and Decision in 23 and 8. The coders agreed on the primary type in 226 of 265 units (85%), and the main disagreement lay between Metacognition and Execution (13 units), followed by Metacognition and Proposal (9). On the 146 units that both runs coded, each coder repeated its own primary type in 90% (GPT) and 95% (Gemini) of cases and its full set of types in 79%. Agreed presence of an actor-type pair changed by at most three units, and no pair changed between present and absent. Kappa between the coders rose for eight of 13 variables, stayed equal for two and fell for three, for instance from .57 to .26 for primary-agent Decision (Appendix Table A11). Conclusions therefore rest on agreed presence and not on one coder or one run.')
p('The study has limits that bound its claims. It covers one project with one human orchestrator, and the propositions await tests in projects with several humans, other agent systems and other tasks. The codebook treats an AI draft as a Proposal until a human adopts it, so part of the contrast between AI Proposals and human Decisions follows from the definition. The primary agent, the sub-agents and the author of the typology share a model family that differs from both coders. This reduces but does not remove the self-preference that LLM evaluators show toward their own generations (Panickssery et al., 2024). Two LLM coders are fewer than the three or more that reliability guidance recommends, and their runs are not independent coders in the strict sense (Artstein & Poesio, 2008). An LLM agrees with experts less than experts agree with each other (Xiao et al., 2023), and validation against human labels is recommended (Pangakis et al., 2023, Ziems et al., 2024). The typology was developed on the early part of the corpus, and 129 of the 265 units were produced after the codebook was frozen, although by the same agent.')
p('Cognition that never entered the trace, such as reading, reflection and conversation with the advisor, is invisible to the method. The primary agent drafted the qualitative interpretations, including the mechanisms. The propositions were built from the episodes of one project and remain conjectures until other projects test them. The human has reviewed the definitions, the example cases and the propositions, and not every cited unit. Some sources were read as preprints or third-party copies. Costa et al. (2025) and most IS works in the background were read as abstracts and records, and only Gregor (2006) in full, so claims of novelty rest on a limited literature search. Future work can test the propositions in projects with several human authors, add human coders for a validation subsample and repeat the recoding for each further revision.')

h1('Conclusion')
p('In this project the thinking was shared through a cycle of delegation, generation and commitment. The human delegated scopes and committed to the direction of the work. The AI generated knowledge, proposals and verification inside the scopes, and mixed contributions arose where the human\u2019s commitment added content. The cycle answers the two worries with evidence. The human remained necessary because commitment stayed with the human, and the AI did more than execute because it supplied the knowledge and proposals on which commitments were made. The typology and the three propositions give disclosure and governance a vocabulary beyond task lists and give IS research claims to test. A disclosure that follows the account states who delegated, who committed and what each party added to a shared output. Because this paper is part of the data it analyses, the sequence of its revisions belongs to the method.')

P.append(('h1pb', 'References'))

# ---------- references
def initials(given):
    g = re.sub(r'\(.*?\)', '', given or '').strip(); out = []
    for w in g.split():
        out.append('-'.join(x[0] + '.' for x in w.split('-') if x))
    return ' '.join(out)
refs = json.load(open(os.path.join(ROOT, 'research', 'references_crossref.json'), encoding='utf-8'))
def get_full_authors(doi):
    url = 'https://api.crossref.org/works/' + urllib.parse.quote(doi)
    for a in range(4):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'icis-pdw-research/1.0'})
            m = json.load(urllib.request.urlopen(req, timeout=40))['message']
            return ['%s, %s' % (x.get('family', ''), x.get('given', '')) for x in m.get('author', [])]
        except Exception: time.sleep(3 * (a + 1))
    return None
def authors(key):
    r = refs[key]; au = r['authors']
    if r['n_authors'] > len(au):
        full = get_full_authors(r['doi'])
        if full and len(full) == r['n_authors']: au = full
    names = []
    for a in au:
        fam, giv = (a.split(', ', 1) + [''])[:2]
        names.append('%s, %s' % (fam.strip(), initials(giv)))
    if len(names) > 20: names = names[:19] + ['\u2026 ' + names[-1]]
    if len(names) == 1: return names[0]
    if len(names) == 2: return names[0] + ', & ' + names[1] if False else names[0] + ' & ' + names[1]
    return ', '.join(names[:-1]) + (', & ' if not names[-1].startswith('\u2026') else ', ') + names[-1]
def yr(k): return refs[k]['year']
def doi(k): return 'https://doi.org/' + refs[k]['doi']
R = [
 f"{authors('S062')} ({yr('S062')}). Inter-coder agreement for computational linguistics. *Computational Linguistics, 34*(4), 555-596. {doi('S062')}",
 f"{authors('S075')} ({yr('S075')}). AI as a co-researcher in the qualitative research workflow: Transforming human-AI collaboration. *International Journal of Qualitative Methods, 24*. {doi('S075')}",
 f"{authors('S002')} ({yr('S002')}). Types and qualities of knowledge. *Educational Psychologist, 31*(2), 105-113. {doi('S002')}",
 f"{authors('S074')} ({yr('S074')}). Building theories from case study research. *Academy of Management Review, 14*(4), 532-550. {doi('S074')}",
 f"{authors('S022')} ({yr('S022')}). Metacognition and cognitive monitoring: A new area of cognitive-developmental inquiry. *American Psychologist, 34*(10), 906-911. {doi('S022')}",
 f"{authors('S029')} ({yr('S029')}). Critical thinking, cognitive presence, and computer conferencing in distance education. *American Journal of Distance Education, 15*(1), 7-23. {doi('S029')}",
 f"{authors('S013')} ({yr('S013')}). The situated function-behaviour-structure framework. *Design Studies, 25*(4), 373-391. {doi('S013')}",
 f"{authors('S045')} ({yr('S045')}). Accelerating scientific discovery with Co-Scientist. *Nature, 655*(8122), 487-496. {doi('S045')}",
 "Handa, K., Tamkin, A., McCain, M., Huang, S., Durmus, E., Heck, S., Mueller, J., Hong, J., Ritchie, S., Belonax, T., Troy, K. K., Amodei, D., Kaplan, J., Clark, J., & Ganguli, D. (2025). *Which economic tasks are performed with AI? Evidence from millions of Claude conversations*. arXiv. https://doi.org/10.48550/arXiv.2503.04761",
 f"{authors('S061')} ({yr('S061')}). Answering the call for a standard reliability measure for coding data. *Communication Methods and Measures, 1*(1), 77-89. {doi('S061')}",
 f"{authors('S072')} ({yr('S072')}). Design science in information systems research. *MIS Quarterly, 28*(1), 75-106. {doi('S072')}",
 f"{authors('S014')} ({yr('S014')}). On distinguishing epistemic from pragmatic action. *Cognitive Science, 18*(4), 513-549. {doi('S014')}",
 f"{authors('S001')} ({yr('S001')}). A revision of Bloom\u2019s taxonomy: An overview. *Theory Into Practice, 41*(4), 212-218. {doi('S001')}",
 f"{authors('S076')} ({yr('S076')}). Generalizing generalizability in information systems research. *Information Systems Research, 14*(3), 221-243. {doi('S076')}",
 f"{authors('S047')} ({yr('S047')}). The impact of generative AI on critical thinking: Self-reported reductions in cognitive effort and confidence effects from a survey of knowledge workers. In *Proceedings of the 2025 CHI Conference on Human Factors in Computing Systems* (pp. 1-22). ACM. {doi('S047')}",
 f"{authors('S051')} ({yr('S051')}). CoAuthor: Designing a human-AI collaborative writing dataset for exploring language model capabilities. In *CHI Conference on Human Factors in Computing Systems* (pp. 1-19). ACM. {doi('S051')}",
 f"{authors('S064')} ({yr('S064')}). Codebook development for team-based qualitative analysis. *CAM Journal, 10*(2), 31-36. {doi('S064')}",
 f"{authors('S008')} ({yr('S008')}). The structure of \u201cunstructured\u201d decision processes. *Administrative Science Quarterly, 21*(2), 246-275. {doi('S008')}",
 "Panickssery, A., Bowman, S. R., & Feng, S. (2024). *LLM evaluators recognize and favor their own generations*. arXiv. https://doi.org/10.48550/arXiv.2404.13076",
 f"{authors('S030')} ({yr('S030')}). Artificial intelligence and management: The automation-augmentation paradox. *Academy of Management Review, 46*(1), 192-210. {doi('S030')}",
 "Simon, H. A. (1960). *The new science of management decision*. Harper.",
 f"{authors('S059')} ({yr('S059')}). The metacognitive demands and opportunities of generative AI. In *Proceedings of the CHI Conference on Human Factors in Computing Systems* (pp. 1-24). ACM. {doi('S059')}",
 f"{authors('S035')} ({yr('S035')}). When combinations of humans and AI are useful: A systematic review and meta-analysis. *Nature Human Behaviour, 8*(12), 2293-2303. {doi('S035')}",
 "ICIS 2026 PDW on Autonomous Scholarship. (2026). *Call for papers: ICIS 2026 PDW on Autonomous Scholarship*. https://sites.nd.edu/autonomous-workshop",
 f"{authors('S043')} ({yr('S043')}). *The AI Scientist: Towards fully automated open-ended scientific discovery*. arXiv. {doi('S043')}",
 f"{authors('S017')} ({yr('S017')}). Cognitive offloading. *Trends in Cognitive Sciences, 20*(9), 676-688. {doi('S017')}",
 f"{authors('S065')} ({yr('S065')}). ChatGPT outperforms crowd workers for text-annotation tasks. *Proceedings of the National Academy of Sciences, 120*(30), e2305016120. {doi('S065')}",
 f"{authors('S068')} ({yr('S068')}). Supporting qualitative analysis with large language models: Combining codebook with GPT-3 for deductive coding. In *28th International Conference on Intelligent User Interfaces* (pp. 75-78). ACM. {doi('S068')}",
 f"{authors('S067')} ({yr('S067')}). *Automated annotation with generative AI requires validation*. arXiv. {doi('S067')}",
 f"{authors('S066')} ({yr('S066')}). Can large language models transform computational social science? *Computational Linguistics, 50*(1), 237-291. {doi('S066')}",
 f"{authors('S058')} ({yr('S058')}). Mixed initiative in dialogue: An investigation into discourse segmentation. In *Proceedings of the 28th Annual Meeting of the Association for Computational Linguistics* (pp. 70-78). Association for Computational Linguistics. {doi('S058')}",
]

import html
NEWREF = [
 ('baird2021', 'The next generation of research on IS use: A theoretical framework of delegation to and from agentic IS artifacts'),
 ('benbasat1987', 'The case research strategy in studies of information systems'),
 ('berente2021', 'Managing artificial intelligence'),
 ('fugener2022', 'Cognitive challenges in human-artificial intelligence collaboration: Investigating the path toward productive delegation'),
 ('gregor2006', 'The nature of theory in information systems'),
 ('gronsund2020', 'Augmenting the algorithm: Emerging human-in-the-loop work configurations'),
 ('leonardi2011', 'When flexible routines meet flexible technologies: Affordance, constraint, and the imbrication of human and material agencies'),
 ('seeber2020', 'Machines as teammates: A research agenda on AI in team collaboration'),
 ('susarla2023', 'The Janus effect of generative AI: Charting the path for responsible conduct of scholarly activities in information systems'),
]
def norm(t): return re.sub(r'[^a-z]', '', re.sub(r'1$', '', html.unescape(t).lower()))
for k, title in NEWREF:
    r = RISK[k]
    assert norm(r['title']) == norm(title), (k, r['title'])
    names = ['%s, %s' % (f, initials(g)) for f, g in r['authors']]
    au = names[0] if len(names) == 1 else (names[0] + ' & ' + names[1] if len(names) == 2 else ', '.join(names[:-1]) + ', & ' + names[-1])
    pg = r['page'] if re.search(r'-', r['page'] or '') else r['page']
    R.append('%s (%s). %s. *%s, %s*(%s), %s. https://doi.org/%s' % (au, r['year'], title, html.unescape(r['container']), r['volume'], r['issue'], pg, r['doi']))
R = [re.sub(r'[\u2013\u2014]', '-', s) for s in R]
def key(s): return re.sub(r'[^a-z]', '', s.lower())
R.sort(key=key)
for s in R: P.append(('ref', s))
build(P, os.path.join(OUT, 'ICIS_PDW_paper.docx'))
json.dump({'agree': T3, 'cod': T_COD, 'ex': T_EX, 'runs': N.T_RUNS}, open(os.path.join(OUT, 'tables_for_appendix.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
open(os.path.join(OUT, 'references.txt'), 'w', encoding='utf-8').write('\n'.join(R))
print('built', len(R), 'refs')
