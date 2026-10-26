import json, csv, os, re, sys, time, urllib.request, urllib.parse
sys.path.insert(0, r'<project>\research\tools')
from docx_builder import build
ROOT = r'<project>'
CODING = os.path.join(ROOT, 'research', 'coding', 'final')
FIG = os.path.join(ROOT, 'paper', 'figures')
OUT = os.path.join(ROOT, 'paper')

# ---------- numbers from analysis outputs
ex = list(csv.DictReader(open(os.path.join(CODING, 'existence.csv'), encoding='utf-8')))
def E(actor, ty): return [r for r in ex if r['actor'] == actor and r['type'] == ty][0]
def cell(actor, ty):
    r = E(actor, ty); n = int(r['units']); a = int(r['agreed'])
    return '%d (%d%%) [%s/%s]' % (a, int(100 * a / n + 0.5), r['gpt'], r['gemini'])
assert E('human', 'D')['agreed'] == '18' and E('human', 'M')['agreed'] == '14' and E('human', 'K')['agreed'] == '9' and E('human', 'P')['agreed'] == '3'
assert E('AI-primary', 'K')['agreed'] == '28' and E('AI-primary', 'P')['agreed'] == '15' and E('AI-primary', 'D')['agreed'] == '6' and E('AI-primary', 'M')['agreed'] == '46'
assert E('AI-subagent', 'K')['agreed'] == '10' and E('AI-subagent', 'D')['agreed'] == '0'
n_h, n_p, n_s = E('human', 'K')['units'], E('AI-primary', 'K')['units'], E('AI-subagent', 'K')['units']
assert (n_h, n_p, n_s) == ('21', '85', '40')
T1 = [['Actor (units)', 'Knowledge', 'Proposal', 'Decision', 'Metacognition', 'Execution']]
for lab, a in [('Human (%s)' % n_h, 'human'), ('Primary agent (%s)' % n_p, 'AI-primary'), ('Sub-agents (%s)' % n_s, 'AI-subagent')]:
    T1.append([lab] + [cell(a, t) for t in 'KPDMX'])
T2 = [['Output', 'AI contribution', 'Human contribution', 'Mode'],
      ['Four-type typology', 'Literature synthesis (S01-U031) and framework draft (S01-U034)', 'Knowledge as a type and Proposal replacing expression or design (S01-U032)', 'AI Knowledge, human Proposal'],
      ['Unit of analysis', 'Draft rule (S01-U039) and data-based operational rule (S01-U042)', 'One model response as the unit (S01-U040)', 'Human Decision, AI Proposal'],
      ['Research questions', 'Candidate questions (S01-U069) and refinement (S01-U072)', 'Three questions with reasons (S01-U070)', 'Human reformulation of an AI Proposal'],
      ['Mixed contribution criterion', 'Draft criterion (S01-U072)', 'Same-output rule and exclusion of bare approvals (S01-U073)', 'Human reformulation of an AI Proposal'],
      ['Literature base', 'Surveys and reading notes (S01-U019, S01-U031)', 'Survey first (S01-U017), originals (S01-U020), skip closed sources (S01-U032)', 'Human Metacognition, AI Knowledge']]

P = []
T_EX = [['Actor', 'Type', 'Exemplar unit'],
        ['Human', 'Knowledge', 'Execution carries little cognition because it follows a prepared blueprint (S01-U005)'],
        ['Human', 'Proposal', 'A split of cognitive contribution into decision, knowledge and expression or design (S01-U014)'],
        ['Human', 'Decision', 'Only the project\u2019s own sessions serve as data (S01-U005)'],
        ['Human', 'Metacognition', 'Survey the related research before designing the scheme (S01-U017)'],
        ['Primary agent', 'Knowledge', 'Reading of the call for papers, including the page limit (S01-U004)'],
        ['Primary agent', 'Proposal', 'A process model linking Knowledge, Proposal, Decision and Metacognition (S01-U066)'],
        ['Primary agent', 'Decision', 'Assignment of full-text reading to a sub-agent with rules for its output (S06-U001)'],
        ['Primary agent', 'Metacognition', 'Report that only abstracts could be read for 12 sources (S01-U031)'],
        ['Primary agent', 'Execution', 'Launching both coders as instructed (S01-U051)'],
        ['Sub-agents', 'Knowledge', 'Reading note that a revised taxonomy is a two-dimensional table (S06-U005)'],
        ['Sub-agents', 'Metacognition', 'Statement that only the main text of one source was read in full (S08-U003)']]
agr = list(csv.DictReader(open(os.path.join(CODING, 'agreement_v1.1_all146.csv'), encoding='utf-8')))
def f2(x): return ('%.2f' % float(x)).replace('0.', '.', 1) if abs(float(x)) < 1 else '%.2f' % float(x)
T3 = [['Actor and type', 'GPT / Gemini', 'Agree %', 'Kappa [95% CI]', 'Alpha [95% CI]']]
names = {'human': 'Human', 'AI-primary': 'Primary agent', 'AI-subagent': 'Sub-agents'}
tn = {'K': 'Knowledge', 'P': 'Proposal', 'D': 'Decision', 'M': 'Metacognition', 'X': 'Execution'}
for r in agr:
    T3.append(['%s, %s' % (names[r['actor']], tn[r['type']]), '%s / %s' % (r['A_present'], r['B_present']), str(int(float(r['pct_agree']) * 100 + 0.5)),
               '%s [%s, %s]' % (f2(r['kappa']), f2(r['kappa_lo']), f2(r['kappa_hi'])), '%s [%s, %s]' % (f2(r['alpha']), f2(r['alpha_lo']), f2(r['alpha_hi']))])
assert len(T3) == 14
T_COD = [['Unit', 'Actor', 'Content (abridged)', 'Coder A', 'Coder B'],
    ['S01-U031', 'Primary agent', 'Reports 25 sources read in full and that sub-agent notes were not all re-checked.', 'M (K, P)', 'K (M)'],
    ['S01-U032', 'Human', 'Argues that agents now give experts new knowledge, so knowledge should count as a contribution.', 'D (K, M, P)', 'K (D, M, P)'],
    ['S01-U033', 'Primary agent', 'Announces that it will log the instruction and write the framework to file.', 'X', 'X'],
    ['S01-U034', 'Primary agent', 'Delivers framework and codebook v0.1 with knowledge as a type and four primary types.', 'P (K, M)', 'P (K, M)'],
    ['S01-U035', 'Human', 'Accepts that evaluation and choice are hard to separate and sets the coding unit to one round.', 'D (K, M)', 'D (K, M)']]
def p(t): P.append(('p', t))
def h1(t): P.append(('h1', t))
def h2(t): P.append(('h2', t))

P.append(('title', 'Who Contributes What in Human-AI Research? A Qualitative Case Study of a Project That Analyses Itself'))

h1('Introduction')
p('Generative AI now takes part in every stage of research, from the formulation of questions to the writing of manuscripts. The call for this workshop asks every submission for a human-AI contribution account. The account covers nine research functions, namely problem formulation, literature identification, theory development, research design, analysis, interpretation, writing, verification and revision (ICIS 2026 PDW on Autonomous Scholarship, 2026). Current disclosure practice answers such a request with a list of tasks. The AI searched, summarised and drafted, and the human supervised. Such a list shows activity and hides the kind of thinking behind it. A draft written by the AI may rest on a scope that the human fixed, and an approval by the human may follow a framing that only the AI had proposed.')
p('Two worries make this hidden layer important. One holds that humans become unnecessary once AI can execute a research workflow. The other holds that AI is an execution tool with no ideas of its own. Both are claims about cognitive contributions, and counting tasks cannot settle them. Research on human-AI work compares the performance of human-AI combinations with that of either party alone (Vaccaro et al., 2024) and classifies conversations into automative and augmentative patterns (Handa et al., 2025). Both characterise collaboration by outcome or by delegation style, and the cognitive kind of each party\u2019s contribution remains untyped.')
p('A vocabulary for this layer serves three audiences. Reviewers and editors need to know what an author is accountable for when an AI proposes the argument. Organisations that deploy AI agents need to decide which decisions stay with people. Researchers need to test claims about complementarity against what each party contributes, beyond measured outcomes. Any project that leaves a trace can be studied in this way, and a project carried out by AI agents under human direction leaves a complete one.')
p('This paper types cognitive contributions from the trace of a collaboration and applies the typology to the project that produced the paper. A human orchestrator and AI agents carried out the project, and every session was recorded as it happened. The recorded sessions are therefore both the data and the history of the manuscript\u2019s own production. We pose three research questions. RQ1 asks whether human, AI and mixed human-AI cognitive contributions exist in the project and which collaboration modes the mixed ones show. RQ2 asks in which categories human and AI contributions fall. RQ3 asks which transitions between human and AI contributions occur and which interaction modes they form.')
p('We answer with a qualitative case analysis in which counts serve as reference. Two LLM coders from different model families coded 146 units from 12 recorded sessions with a frozen codebook. Human, AI and mixed contributions all exist in the project. The human held every project-level decision and regulated the process, the AI supplied knowledge, proposals and verification, and five outputs carry explicit contributions from both parties. Transitions between contributions form six interaction modes, among them a loop in which the human sets a direction, the AI drafts and the human commits.')
p('The paper makes three contributions. It offers a typology of observable cognitive contributions that treats knowledge as something an AI can supply. It provides a trace-based coding standard. It gives a qualitative account of how contributions were distributed and exchanged in an AI-led project. Together they give disclosure and governance a vocabulary beyond task lists.')

h1('A Typology of Observable Cognitive Contributions')
h2('Contributions in Human-AI Work')
p('Information systems and management research frames the division of labour between humans and AI mainly at the level of tasks. Raisch and Krakowski (2021) argue that automation and augmentation are intertwined rather than alternative. A meta-analysis of 106 experiments finds that human-AI combinations on average perform worse than the better of human or AI alone. The losses occur in decision tasks and the gains in content creation (Vaccaro et al., 2024).')
p('Trace-based studies are fewer in number. Handa et al. (2025) label conversations as automative or augmentative, and CoAuthor records keystroke-level co-writing in which writers produced 72.6% of the final text (Lee et al., 2022). Survey evidence suggests that effort shifts toward verification, integration and stewardship when workers use generative AI (Lee et al., 2025). In scientific discovery, the AI Co-Scientist assigns generation, critique and refinement to agents while scientists set goals and review results (Gottweis et al., 2026). Costa et al. (2025) describe a qualitative research workflow in which the AI acts as analytical partner and the human as reflexive agent. Fully automated pipelines for machine learning research generate ideas, run experiments, write papers and review them, and leave the human share unmeasured (Lu et al., 2024). These works describe contributions by task, outcome or role. A typing of the cognitive kind of each party\u2019s contribution across a whole project is missing.')
p('Existing coding schemes address related but different objects. Cognitive presence codes four phases of inquiry at message level in text conferences among human participants (Garrison et al., 2001). Initiative coding records who holds control through assertions, commands, questions and prompts and leaves cognitive content aside (Walker & Whittaker, 1990). The conversation-level patterns of Handa et al. (2025) describe how work is delegated and not which thinking each party supplies. The present typology borrows the indicator logic of the first, the observable stance of the second and the LLM classification of interaction logs of the third. It adds an actor to every tag and applies the scheme to the whole course of one project.')
h2('From Cognition Research to Four Types')
p('Cognitive taxonomies separate cognitive processes from knowledge types (Krathwohl, 2002) and distinguish situational, conceptual, procedural and strategic knowledge (de Jong & Ferguson-Hessler, 1996). Decision research describes choice as intelligence, design and choice (Simon, 1960). Mintzberg et al. (1976) elaborate this into twelve elements with pervasive recycling and report that evaluation and choice could be separated in only 18 of 83 evaluation-choice instances. Design research treats externalised structure as part of thinking, since synthesis includes making structure explicit (Gero & Kannengiesser, 2004) and epistemic actions reduce the burden of mental computation (Kirsh & Maglio, 1994). Metacognition spans knowledge, experiences, goals and strategies (Flavell, 1979), and generative AI adds the demands of prompt formulation, iteration, output evaluation and automation strategy (Tankelevitch et al., 2024). People hand cognitive demands to external resources according to a metacognitive evaluation of those demands (Risko & Gilbert, 2016).')
p('Two properties of these sources shape our typology. First, they place knowledge in the thinker, so that evaluation, choice and design operate on what the thinker already knows. When an AI agent supplies knowledge that a human expert did not hold, knowledge also becomes something that is contributed. We therefore treat Knowledge as a type of contribution. Second, cognition is inferred from what is observable. Garrison et al. (2001) addressed this by deriving manifest indicators for each latent phase of inquiry, and we adopt the same stance. The typology classifies what a move does in the shared record.')
p('A cognitive contribution is an externalised move by an actor that adds to or changes the shared research state and can be identified from the trace. Figure 1 shows the types and the pipeline in which they are used. Knowledge introduces a fact, concept, method or situational context into the record. Proposal offers a candidate, such as a frame, a structure, a text or a revision, that is not yet committed to. Decision commits the project by setting a goal, scope or constraint, or by selecting, rejecting or stopping an option. Metacognition checks or steers how the work is done and how reliable it is. Execution carries out a specified step without new content and is recorded for coverage.')
p('Evaluation and choice form one type, since evaluation usually carries preference. One rule separates object from process. If removing a move would change the product, the move is Knowledge, Proposal or Decision. If it would change only how the product was made or checked, the move is Metacognition. The rule applies to every unit regardless of actor.')
p('Each type has subtypes that the codebook defines with examples. Knowledge divides into fact or source, concept or explanation, method or procedure, and situated context. Proposal divides into frame, structure or plan, content, and alternative or revision. Decision divides into setting a goal, scope or constraint and selecting, accepting, rejecting or stopping an option. Metacognition divides into monitoring, regulating and calibrating, where calibrating covers statements about the limits, confidence or provenance of one\u2019s own output. Further boundary rules govern mixed cases. Proposals offer and decisions commit, so a draft by the AI is a Proposal until a human adopts it, and the adoption is a separate Decision. A fact found by a check is Knowledge, and the check itself is Metacognition.')
P.append(('image', os.path.join(FIG, 'fig1_final.png'), 6.0))
P.append(('caption', 'Figure 1. From recorded sessions (A) through units (B) and tags (C) to three analyses (D to F). Bubble texts abridge project messages.'))

h1('Method')
h2('Case and Data')
p('The case is the project that produced this manuscript. One human orchestrator directed a primary AI agent (claude-sonnet-5.5), which dispatched sub-agents running the same model to survey and read literature. The recorded period covers the choice of the topic, the design of the typology, the reading of sources and the coding itself. Every session was exported with message-level provenance together with its model, agent name and parent session. The corpus at the time of analysis comprises 12 sessions, namely the ideation session in which the topic was chosen, the main working session and ten sub-agent sessions. These yield 146 units, of which 21 are human messages, 75 are primary-agent responses, 10 are primary-agent prompts to sub-agents and 40 are sub-agent responses. Each revision of the manuscript extends the corpus, and the analysis is repeated on the extended corpus.')
h2('Units and Coding')
p('A unit is one model response. A human unit is one human message. An AI unit is an assistant message that contains visible text or dispatches a sub-agent, together with the tool-only steps that precede it. Of 499 assistant messages in the export, 424 (85%) contained tool calls only, so these steps serve as evidence for the unit that follows. In a sub-agent session the single user message is the primary agent\u2019s prompt, and its actor is the primary agent. A unit may carry several tags, each with an actor and a type, and at most one primary tag per actor. Each tag carries a stage label drawn from the functions of the workshop\u2019s contribution account plus governance and tooling, and an evidence quotation. The codebook gives each code a brief and a full definition, rules for use and non-use, and examples (MacQueen et al., 1998). Table 1 shows five consecutive units from the project with the tags of both coders.')
P.append(('table', T_COD, [0.75, 0.85, 3.0, 0.95, 0.95]))
P.append(('caption', 'Table 1. Five consecutive units with the tags of both coders, primary tag first (K Knowledge, P Proposal, D Decision, M Metacognition, X Execution).'))
p('Two independent coders, GPT-6.1-sol and Gemini-4-argon, coded every unit with the frozen codebook (version 1.1) as their instruction, as in the LLM annotation studies of Gilardi et al. (2023) and Xiao et al. (2023). Each ran in an isolated session that held only the codebook and the units, in chunks of up to 20 units. Each coder received the unit text and an actor hint with model names masked. The primary agent designed the codebook and coordinated the coding, and the analysis uses the codes of the two coders alone. The human approved each codebook version and ruled on boundary cases. Version 1.1 revised version 1.0 after a first run on 106 units. The revision treats narration of a next step as Execution. It also narrows Metacognition to moves that change the shared state about process or reliability.')
h2('Analysis')
p('The analysis is qualitative and descriptive. For RQ1, an actor-type pair counts as present when both coders assign it to at least one unit, and exemplar units are read in context. A mixed contribution is one output to which both actors contribute with explicit expression that adds, changes or reasons about content. For example, the AI supplies knowledge and the human proposes a scheme built on it. We identified outputs by reading the units and the project log, and the human ruled on the definition and on example cases.')
p('For RQ2, we tabulate presence by actor, type and stage as reference. For RQ3, we order cognitive units within each session and skip units coded only as Execution, Coordination or unclassifiable. We write each transition as actor and primary type and group recurring transitions by content into interaction modes. The study follows a single-case design and generalises analytically to the typology, following Eisenhardt (1989) and Lee and Baskerville (2003). The coding standard is a method artifact in the design-science sense (Hevner et al., 2004). We report percent agreement, Cohen\u2019s kappa and Krippendorff\u2019s alpha with bootstrap confidence intervals for each actor-type presence variable, following Artstein and Poesio (2008) and Hayes and Krippendorff (2007).')

h1('Findings')
h2('RQ1: Human, AI and Mixed Contributions Exist')
p('Human contributions occur in all four types (Table 2). Decision appears in 18 of 21 human units, Metacognition in 14, Knowledge in 9 and Proposal in 3. The decisions set the direction of the project. The human chose the topic and restricted the data to the project\u2019s own sessions. The human required anonymised release, fixed the unit of analysis as one model response and wrote the three research questions of this paper.')
p('Human Metacognition regulated the process. The human required that every session be recorded (S01-U001), that originals be read wherever accessible (S01-U020) and that manuscript writing wait until the framework was complete (S01-U064). Human Knowledge was mostly situated context that only the human held, such as the choice of coder models and the location of a drawing method. It also included the claim that evaluation usually carries preference (S01-U035). Human Proposals were comparatively rare. Three units contain them, namely the first three-way split of contributions (S01-U014), its revision to Proposal (S01-U032) and the formulation of the research questions (S01-U070). Each shaped a core element of the design.')
P.append(('table', T1, [1.3, 1.05, 1.05, 1.05, 1.1, 0.95]))
P.append(('caption', 'Table 2. Units with each type present in both coders\u2019 tags, with the count of each coder in brackets (GPT/Gemini).'))
p('AI contributions occur in Knowledge, Proposal, Metacognition and Decision. The primary agent supplied Knowledge in 28 of its 85 units, for example an explanation of agreement coefficients (S01-U044). The sub-agents supplied it in 10 of 40 units, almost all of it literature. The primary agent offered Proposals in 15 units, among them candidate taxonomies (S01-U016, S01-U019), candidate research questions (S01-U069) and the operational rule for coding units (S01-U042). Its Metacognition appeared in 46 units and consisted of verification results, detected errors and statements about the limits of its own output.')
p('Decisions by the AI were few. Both coders agree on six Decision units, and all are task assignments from the primary agent to sub-agents. One coder tags four further units in which the AI changed its tooling approach after a failure, and the other tags three in which it accepted a human redirection or formulation. Decisions about the direction of the research product came from the human.')
P.append(('table', T_EX, [1.0, 1.1, 4.4]))
P.append(('caption', 'Table 3. One exemplar unit for each actor-type pair that both coders tag.'))
p('These patterns bear on the two worries stated earlier. The human remained necessary, since every project-level decision came from the human, and the human also contributed knowledge and proposals that changed the design. The AI did more than execute. It contributed Proposals and Knowledge that shaped the typology, the unit of analysis and the research questions, and it carried the verification work. Execution accounts for 32 of the 85 primary-agent units and coexists with the other types.')
p('Mixed contributions also exist in the project. We identified five outputs to which both actors contributed with explicit expression (Table 4), and they show four collaboration modes. In the first, the AI supplies knowledge and the human builds a proposal on it. The reframing of Knowledge as a type of contribution followed this mode. The human wrote that the AI\u2019s literature summary had supplied what they did not previously know. The human then proposed to treat knowledge as a type and to rename expression or design as Proposal (S01-U032). In the second, the human fixes a decision and the AI turns it into an operational proposal grounded in data, as when the unit of analysis was defined. In the third, the human reformulates an AI proposal. Three research questions replaced the AI\u2019s candidate set (S01-U070), and the criterion for mixed contributions received its exclusion of bare approvals (S01-U073). In the fourth, the human regulates how the AI supplies knowledge, for instance by requiring a survey first and the reading of originals. Two human units, S01-U078 and S01-U080, were short approvals that left the proposed outputs as they were.')
P.append(('table', T2, [1.15, 1.75, 2.0, 1.6]))
P.append(('caption', 'Table 4. Outputs with contributions from both actors and their collaboration mode.'))
h2('RQ2: Where Contributions Fall')
p('Table 2 summarises the distribution for reference. Human units concentrate in Decision (86%) and Metacognition (67%), with Knowledge in 43% and Proposal in 14%. The primary agent shows Metacognition in 54% of its units, Knowledge in 33%, Proposal in 18% and Decision in 7%, with Execution in 38%. Sub-agents show Knowledge in 25% and Execution in 43%, with Proposal in one unit and Decision in none. By stage, human contributions fall mostly in design (14 of 44), followed by problem formulation, governance and theory (6 each). Primary-agent contributions fall in verification (19 of 95), literature (18), design (16) and tooling (15), and sub-agent contributions fall almost entirely in literature (19 of 20).')
h2('RQ3: Transitions and Interaction Modes')
p('Figure 2 groups the transitions between consecutive cognitive units within sessions. The two coders found 85 and 67 transitions, and six interaction modes recur. Direction and drafting (human Decision, then AI Proposal) and proposal and commitment (AI Proposal, then human Decision) form a loop that accounts for 15 and 12 transitions. In the loop the human sets or reframes a direction, the AI drafts, and the human commits or redirects. One run began with the human\u2019s rulings on evaluation and the coding unit (S01-U035), continued with the second framework draft (S01-U039) and ended with the human\u2019s definition of the unit (S01-U040). Supply and reframing (AI Knowledge, then human Decision) is rare. An example is the explanation of agreement coefficients (S01-U044) followed by the human\u2019s decision to report several statistics (S01-U045).')
p('Regulation and response (human Decision or Metacognition, then AI Metacognition) accounts for 8 and 9 transitions. The instruction to survey the literature first (S01-U017) led the AI to dispatch three sub-agents (S01-U018) and later to return a synthesis (S01-U019). The human answered with the instruction to read originals (S01-U020). Challenge (AI Proposal, then human Metacognition) accounts for 2 and 4 transitions. The AI\u2019s proposal of two orthogonal dimensions (S01-U016) met the human\u2019s demand to survey the research before designing (S01-U017). Autonomous work (AI Metacognition continuing or leading to AI Knowledge) is the most frequent mode with 39 and 22 transitions. It consists of runs of verification and reporting between human messages, such as the checks of sub-agent notes (S01-U027 to S01-U030).')
P.append(('image', os.path.join(FIG, 'fig2_final.png'), 6.0))
P.append(('caption', 'Figure 2. (A) Six interaction modes with the transition counts of Coder A (GPT) and Coder B (Gemini). (B) A worked case with the types both coders tagged. (C) Mixed contribution and bare approval.'))
p('Mixed contributions arise from the loop of the first two modes. Three outputs in Table 4 show an AI Proposal, a human Decision and a further AI Proposal in succession. They are the unit of analysis, the research questions and the criterion for mixed contributions. The typology followed a related path in which AI-supplied knowledge preceded a human reframing, an AI draft and a human ruling (S01-U031 to S01-U035). A single pass of proposal and commitment, as in the short approvals of the last rounds, ended with an output that only one actor shaped. The six modes suggest a division of exchange. Humans reach AI mainly through direction and regulation, the AI reaches the human mainly through proposals, and knowledge enters through supply that the human then reframes.')

h1('Discussion and Limitations')
p('The typology adds to task-based disclosure in three ways. First, it shows that AI contribution and human decision authority sit together in one project. The AI contributed in all types except project-level Decision, while the human held every project-level Decision and also supplied knowledge and proposals that changed the design. Second, it shows that cognition moved in cycles. Mixed contributions arose when direction and drafting alternated with proposal and commitment. The reframing of Knowledge as a contribution type is the clearest case in which AI-supplied knowledge changed a human\u2019s construct. Third, it sharpens what governance can ask. A disclosure that says who wrote a section leaves open who decided what the section should claim, and the types allow both to be answered from the record.')
p('The coding standard performed unevenly, and the unevenness is informative. Across the actor-type presence variables, kappa between the two coders ranged from .57 to 1.00, and alpha took nearly identical values (Table 5). Human Decision (kappa .97), AI Metacognition (.91) and AI Proposal (.84) were highest, and AI Decision was lowest (.57, CI .25 to .81). The coders agreed on the primary type in 112 of 146 units (77%). The main disagreement lay between Metacognition and Execution, which the coders separated differently in 14 units, followed by Metacognition and Knowledge in 6. Version 1.0 left the boundary between narrating a next step and regulating the process open. Tightening it in version 1.1 raised kappa for primary-agent Execution from .35 to .87 on the same 106 units. Sub-agent Metacognition remains unsettled at kappa .61, because the coders disagree on whether a sub-agent\u2019s report of its own checks regulates the work or only describes it. Intervals are wide for types that occur in few units, such as human Proposal.')
P.append(('table', T3, [1.7, 1.0, 0.7, 1.6, 1.6]))
P.append(('caption', 'Table 5. Agreement between the coders on actor-type presence (146 units).'))
p('The study has limits that bound its claims. It covers one project with one human orchestrator. The primary agent, the sub-agents and the author of the typology share a model family that differs from both coders. This reduces but does not remove the self-preference that LLM evaluators show toward their own generations (Panickssery et al., 2024). Two LLM coders are fewer than the three or more that reliability guidance recommends, and their runs are not independent coders in the strict sense (Artstein & Poesio, 2008). Annotation studies find that an LLM agrees with experts less than experts agree with each other (Xiao et al., 2023). Pangakis et al. (2023) and Ziems et al. (2024) recommend validation against human labels. The coders saw actor hints and unit text truncated at 2,500 characters. The typology was developed on the corpus it describes, and only ten units, produced after the freeze of version 1.1, were unseen by its designer.')
p('Cognition that never entered the trace, such as reading, reflection and conversation with the advisor, is invisible to the method. The primary agent drafted the qualitative interpretations, and the human has so far reviewed definitions and example cases and not every cited unit. Some sources were read as preprints or third-party copies. One near neighbour (Costa et al., 2025) was available to us only as an abstract, so claims of novelty rest on a literature search of limited coverage. Generalisation is analytic, and the typology and the interaction modes are offered for testing in other projects.')

h1('Conclusion')
p('Cognitive contributions can be typed from the trace of a collaboration. In this AI-led research project the human held every project-level decision and regulated the process. The AI supplied knowledge, offered proposals and verified work, and the two produced mixed contributions through cycles of drafting and commitment. These patterns answer the two worries with evidence. The human remained necessary, and the AI did more than execute. The typology and the interaction modes give disclosure a vocabulary beyond task lists. Because this paper is part of the data it analyses, the sequence of its revisions belongs to the method. Further work can apply the typology to projects with several human authors, add human coders for a validation subsample and compare the recoding of each revision of this manuscript.')

h1('Use of Generative AI')
p('Generative AI produced this manuscript, the coding standard, the analysis pipeline, the figures and the workflow appendix under the direction of one human orchestrator, who is responsible for the final version. The primary agent was claude-sonnet-5.5 with sub-agents on the same model, and the coders were GPT-6.1-sol and Gemini-4-argon. An Azure OpenAI image model drew the figure drafts and icons, and a further model (big-pickle) built an intermediate version of the figures. The workflow appendix documents prompts, interventions, errors and verification.')

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
R = [re.sub(r'[\u2013\u2014]', '-', s) for s in R]
def key(s): return re.sub(r'[^a-z]', '', s.lower())
R.sort(key=key)
for s in R: P.append(('ref', s))
build(P, os.path.join(OUT, 'ICIS_PDW_paper.docx'))
open(os.path.join(OUT, 'references.txt'), 'w', encoding='utf-8').write('\n'.join(R))
print('built', len(R), 'refs')
