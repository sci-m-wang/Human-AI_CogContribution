import json, csv, os, re, sys
sys.path.insert(0, r'<project>\research\tools')
from docx_builder import build
ROOT = r'<project>'
CODING = os.path.join(ROOT, 'research', 'coding')
OUT = os.path.join(ROOT, 'paper'); os.makedirs(OUT, exist_ok=True)
agr = list(csv.DictReader(open(os.path.join(CODING, 'agreement_by_actor_type.csv'), encoding='utf-8')))
def A(actor, ty): return [r for r in agr if r['actor'] == actor and r['type'] == ty][0]
def ci(lo, hi): return '[%s, %s]' % (lo, hi)
def f2(x): return ('%.2f' % float(x)).replace('0.', '.', 1) if abs(float(x)) < 1 else '%.2f' % float(x)
rows2 = [['Actor', 'Type', 'GPT n', 'Gemini n', 'Agree %', 'Cohen kappa [95% CI]', 'Krippendorff alpha [95% CI]']]
spec = [('human', 'K'), ('human', 'P'), ('human', 'D'), ('human', 'M'), ('AI-primary', 'K'), ('AI-primary', 'P'), ('AI-primary', 'D'),
        ('AI-primary', 'M'), ('AI-primary', 'X'), ('AI-subagent', 'K'), ('AI-subagent', 'M'), ('AI-subagent', 'X')]
for a, t in spec:
    r = A(a, t)
    rows2.append([a, t, r['A_present'], r['B_present'], str(round(float(r['pct_agree']) * 100)),
                  '%s %s' % (f2(r['kappa']), ci(f2(r['kappa_lo']), f2(r['kappa_hi']))),
                  '%s %s' % (f2(r['alpha']), ci(f2(r['alpha_lo']), f2(r['alpha_hi'])))])

T1 = [['Type', 'Observable criterion (what the move does in the shared record)', 'Subtypes', 'Theoretical anchor'],
      ['K Knowledge', 'Introduces a fact, concept, method or situational fact as input to the work', 'K1 fact/source; K2 concept/explanation; K3 method/procedure; K4 situated context', 'Knowledge types (Krathwohl, 2002; de Jong & Ferguson-Hessler, 1996)'],
      ['P Proposal', 'Offers a candidate (frame, structure, content, revision) that is not yet committed to', 'P1 frame; P2 structure/plan; P3 content; P4 alternative/revision', 'Synthesis and externalisation of structure (Gero & Kannengiesser, 2004); design as development (Mintzberg et al., 1976)'],
      ['D Decision', 'Commits the project: sets goal, scope or constraint; selects, accepts, rejects or stops (evaluation and choice are not split)', 'D1 set; D2 select', 'Intelligence-design-choice (Simon, 1960); evaluation-choice (Mintzberg et al., 1976)'],
      ['M Metacognition', 'Monitors or regulates how the work is done or how reliable it is', 'M1 monitor; M2 regulate; M3 calibrate', 'Metacognitive knowledge, experiences, goals, actions (Flavell, 1979); GenAI metacognitive demands (Tankelevitch et al., 2024); decision control (Mintzberg et al., 1976)']]

P = []
def p(t): P.append(('p', t))
def h1(t): P.append(('h1', t))
def h2(t): P.append(('h2', t))

P.append(('title', 'Who Thinks What? Typing Cognitive Contributions in Human\u2013AI Research Collaboration from Interaction Traces, Applied to Its Own Production'))
p('*Submission type: PDW (Autonomous Scholarship).*')

h1('Introduction')
p('The ICIS 2026 PDW on Autonomous Scholarship asks authors to push research workflows toward AI execution while documenting the human\u2013AI division of labor. Such documentation usually enumerates tasks: who searched, who wrote, who ran the analysis. Tasks say little about what kind of thinking each party contributed. An AI may \u201cwrite\u201d a section whose scope and acceptance were fixed by a human, and a human may \u201conly\u201d approve a draft whose decisive framing came from the AI. If autonomous scholarship is to be assessed by reviewers, editors and the field, we need a vocabulary of cognitive contributions that can be applied to the trace of a collaboration rather than to the participants\u2019 recollection of it.')
p('This paper offers such a vocabulary and applies it reflexively. The project that produced this manuscript was run by one human orchestrator and AI agents, and every session was recorded. We (i) derive a four-type typology of observable cognitive contributions (Knowledge, Proposal, Decision, Metacognition) from cognition and decision research and adapt it to a paradigm in which an AI agent can supply new knowledge to a human expert; (ii) specify a trace-based coding standard with a unit of analysis, boundary rules and provenance attributes; (iii) apply it to the project\u2019s own sessions with two independent LLM coders; and (iv) report what the resulting distribution does and does not show. Our research questions are: **RQ1** Can cognitive contributions be typed from interaction traces with substantial agreement between independent coders? **RQ2** How are the types distributed between the human, the primary AI agent and sub-agents, and who proposes and who commits? **RQ3** (exploratory) Where does the scheme fail, and what does revising and re-coding it reveal?')

h1('Background and Gap')
h2('Division of Labor Between Humans and AI')
p('Management and IS research frames human\u2013AI work mainly at the level of tasks. Raisch and Krakowski (2021) argue that automation and augmentation are interdependent rather than alternatives. A meta-analysis of 106 experiments finds that human\u2013AI combinations on average perform worse than the better of human or AI alone, with losses in decision tasks and gains in content-creation tasks (Vaccaro et al., 2024), which suggests that the type of cognitive work matters. Trace-based studies are rarer. Handa et al. (2025) classify conversations with an AI assistant into automative and augmentative collaboration patterns (43% vs. 57%), but their unit is a single conversation and their axis is delegation style rather than what each party contributes cognitively. CoAuthor logs keystroke-level human\u2013AI writing sessions and reports that writers produced 72.6% of the final text (Lee et al., 2022), which attributes text but not thinking. A survey study suggests that with generative AI the worker\u2019s effort shifts toward verification, integration and stewardship (Lee et al., 2025). In research settings, AI Co-Scientist describes generate\u2013critique\u2013refine agents, with human effort devoted to setting goals and reviewing (Gottweis et al., 2026), and Costa et al. (2025) propose, in an abstract we could read, an abductive human\u2013AI workflow in which the human is the reflexive agent. To our knowledge, and within the limits of our literature access, no study types the cognitive kind of each party\u2019s contribution across a whole research project from its interaction trace.')
h2('Cognition and Its Externalized Forms')
p('Cognitive taxonomies separate what is processed from how. The revised Bloom taxonomy is a two-dimensional table of cognitive processes crossed with knowledge types (factual, conceptual, procedural, metacognitive), and it classifies intended objectives rather than observed behavior (Krathwohl, 2002). De Jong and Ferguson-Hessler (1996) distinguish situational, conceptual, procedural and strategic knowledge. Both treat knowledge as something the thinker already holds. Decision research describes choice as a process of intelligence, design and choice (Simon, 1960), elaborated by Mintzberg et al. (1976) into twelve elements with pervasive recycling, in which evaluation and choice could be separated in only 18 of 83 observed instances. Design research treats externalization as part of thinking: in the function\u2013behavior\u2013structure framework, synthesis includes externalizing structure (Gero & Kannengiesser, 2004), and epistemic actions change the world to reduce mental computation (Kirsh & Maglio, 1994). Metacognition comprises knowledge, experiences, goals and strategies (Flavell, 1979), and generative AI adds metacognitive demands of prompt formulation, iteration, output evaluation and automation strategy (Tankelevitch et al., 2024).')
p('Two points matter for traces. First, latent processes are inferred, not observed; Garrison et al. (2001) therefore derived manifest indicators for each phase of cognitive presence and reported kappa values of .35, .49 and .74 over three coding rounds. Second, the classical assumption that decisions and designs rest on the decider\u2019s own prior knowledge weakens when an AI agent can supply knowledge the human expert did not have. We therefore treat knowledge as a contribution that can be made, not only as a resource that is held.')

h1('A Typology of Observable Cognitive Contributions')
p('A *cognitive contribution* is an externalized move by an actor that adds to or changes the shared research state and can be identified from the trace alone. We code manifest content and make no claim about internal cognition. Table 1 gives the four types and the residual codes X (execution without new content, e.g., running a specified command), C (coordination) and Z (unclassifiable). Each code has a codebook entry with a brief and full definition, when to use, when not to use, and examples, following MacQueen et al. (1998).')
P.append(('caption', 'Table 1. Contribution types and their anchors'))
P.append(('table', T1, [0.9, 2.2, 1.7, 1.7]))
p('**Boundary rules.** R1 separates object from process: if the move were removed, would the product (paper, data, codebook) differ, or only the way it was produced and checked? The former is K, P or D; the latter is M. Proposals offer and decisions commit, so an AI draft is a P until a human adopts it, and the adoption is a separate D. A move that reports what a source says is K; organizing the literature leans M with some D. Because evaluation usually carries preference, evaluative statements that express acceptability are D, and checks of correctness without preference are M.')
p('**Unit of analysis.** A unit is one model response, not a complete interaction. A human unit is one human message. An AI unit is an assistant message with visible text or a sub-agent dispatch, together with the tool-only steps since the previous unit; in the exported sessions 424 of 499 assistant messages (85%) contained only tool calls and serve as evidence rather than units. A unit may carry several tags and tags of both actors; at most one tag per actor is marked primary. Attributes recorded per tag are: actor, derived from session lineage and not from message role (in a sub-agent session the \u201cuser\u201d message is the primary agent\u2019s prompt); stage (the CFP\u2019s functions plus governance and tooling); evidence quote; *responds-to*; *uptake* (adopted, adopted-modified, rejected, questioned, no response); *epistemic transfer* (the receiver states that content was new or visibly acts on it); *autonomous* (an AI decision without a preceding human instruction); and *manual change* (a human edit not mediated by AI). The tracing of origin and uptake is our own design; the initiative literature supports only the narrower idea that control can be read from utterance types (Walker & Whittaker, 1990).')

h1('Method')
h2('Design')
p('The study is a single, self-referential case with analytic rather than statistical generalization: claims are made to the typology and its application conditions, not to a population of projects (Eisenhardt, 1989; Lee & Baskerville, 2003). The coding standard is a method artifact in the design-science sense (Hevner et al., 2004), evaluated by observation and by agreement between independent coders.')
h2('Data')
p('We exported all sessions of the project on the day of coding: the human\u2019s ideation session, the main working session, and 10 sub-agent sessions (literature surveys and full-text reading). The export yields 106 units: 13 human, 53 primary-AI (43 responses and 10 prompts to sub-agents) and 40 sub-agent responses. Tool outputs are omitted and unit text is truncated at 2,500 characters. The primary agent was claude-sonnet-5.5 (OpenCode 1.18.30 via OpenWork 0.18.59); sub-agents ran on the same model. Because the codebook was revised during the project, all units existing at the time of codebook freeze (v1.0, SHA-256 recorded) form a *development set* and are reported as exploratory; units produced afterwards form an *evaluation set* (see Appendix). The present results are therefore development-set results.')
h2('Coders and Agreement')
p('Two LLM coders worked independently: GPT-6.1-sol and Gemini-4-argon, both run through the same agent framework in a neutral directory with no project instructions, in chunks of 18 units, with the coding manual (codebook sections on construct, unit, types, rules, attributes and output schema) and a packet from which model names had been removed. Actor hints were retained, so actors were not blind. The designer of the scheme (the primary agent) is not an independent coder: it authored the codebook and most AI content. Coders from other model families partially address self-preference bias, which has been documented for LLM evaluation of summary quality (Panickssery et al., 2024); we apply this evidence only by analogy. Following the human decision, we report several statistics rather than one: percent agreement, Cohen\u2019s kappa and Krippendorff\u2019s alpha with a 2,000-resample bootstrap 95% confidence interval (Hayes & Krippendorff, 2007), for each binary variable \u201cactor \u00d7 type present in unit\u201d. No acceptance threshold was set, because the sample is small and the analysis mainly qualitative; interpretation follows the results. A human-coded reference subsample is planned and not yet available.')

h1('Results')
h2('Agreement (RQ1)')
p('Both coders coded all 106 units. Agreement was high for the types that carry the main distinctions (Table 2): for the primary AI, kappa was .71 for K, .77 for P, .60 for D and .87 for M; for sub-agents, .87 for K and .94 for M. Human D and M tags were agreed in every unit, but with 11\u201312 positive units the intervals for human K and P are wide. Execution was unreliable (kappa .35 for the primary agent and .13 for sub-agents): Gemini coded 20 primary-agent and 32 sub-agent units as containing execution against 5 and 3 for GPT. Pooled over actors, kappa was .66 for K, .75 for P, .78 for D, .56 for M and .16 for X. Disagreement in primary tags clustered around M: M versus X in 11 units, M versus K in 8, and M versus P and M versus D in 4 each. P and D for sub-agents were too rare (one or two units) to evaluate.')
P.append(('caption', 'Table 2. Agreement between the two LLM coders (n = 106 units; presence of each actor\u00d7type tag)'))
P.append(('table', rows2, [0.9, 0.4, 0.5, 0.6, 0.5, 1.6, 1.8]))
h2('Distribution Between Human and AI (RQ2)')
p('Figure 1 shows the share of units in which each actor\u2019s tag is present (bars: both coders agree; whiskers: the higher coder). The human contribution was concentrated in Decision and Metacognition: D was present in 11 of 13 human messages (85%) and M in 12 (92%), according to both coders. Human Knowledge was present in 5 messages (38%, 46\u201354% by either coder) and was mostly situated context (K4: constraints, deadlines, intentions, the advisor\u2019s role). Human Proposals were rare: P was present in 2 of 13 messages by both coders (15%; 23% by GPT). The primary AI agent showed K in 42% of its 53 units, P in 19% and D in 13%, with M in 77% (91% by GPT). Sub-agents mostly supplied knowledge (K in 30% of 40 units) and almost never proposed or decided (P and D in one unit each). Sub-agent work lay almost entirely in the literature stage (50 or 85 stage tags, by coder), whereas human tags spread over design, governance, theory, problem formulation and literature.')
P.append(('image', os.path.join(CODING, 'fig_presence.png'), 5.3))
P.append(('caption', 'Figure 1. Share of units in which each actor has a tag of each type (bars: both coders; whiskers: higher coder)'))
p('Two cautions apply. First, M is present in about nine of ten AI units under the current definition, which counts any statement of planning, checking or uncertainty. It therefore has little discriminating power for AI units, and the unresolved M/X boundary shows in the divergent execution counts. Second, the AI made decisions without a preceding human instruction: of the primary agent\u2019s D tags, 8 of 12 (GPT) and 10 of 10 (Gemini) were flagged autonomous. We have not yet characterized their content.')
h2('Who Proposes and Who Commits')
p('Both coders tagged 10 primary-agent units as containing a proposal. In 8 of these, the next human message carried a D tag (set, accept or modify); in the other 2 the human replied with a question. Combined with the rarity of human P, this gives a clear pattern in this project: structural and textual proposals came mainly from the AI, and commitment from the human, who also regulated the process. Uptake labels, however, were not reliable: for human tags the coders assigned \u201cadopted\u201d 21 versus 37 times and \u201cadopted-modified\u201d 7 versus 1 time, so we use only the presence of a human D after an AI P.')
h2('Knowledge Transfer')
p('Explicit evidence that AI-supplied knowledge was new to the human was rare: 2 (GPT) and 3 (Gemini) AI K tags carried the explicit-new flag. The clearest instance is the human remarking that the cognition taxonomies summarized by the AI were unknown to them before the summary; this observation led to the revision of the typology itself, from knowledge as a dimension to knowledge as a contribution type. The flag was applied inconsistently to human tags by one coder (5 times), which indicates a definitional problem.')
h2('Revision Candidates (RQ3)')
p('The disagreements point to four revisions for codebook v1.1: restrict M2 to explicit regulation and treat routine tool use as X; define when a statement of intent counts as M versus D; replace the uptake scale with a rule anchored in the next human message; and state that the epistemic-transfer flag attaches only to knowledge received by a different actor. Under the freeze rule, these changes create v1.1 and the corpus will be re-coded; differences between versions are reported in the Appendix.')

h1('Discussion')
p('**What the types add to task-based disclosure.** A task list would say that the AI searched, summarized and drafted. The type account adds that the human in this project rarely authored proposals, but committed and regulated in almost every message, and supplied situated knowledge that the AI could not have. This fits the PDW\u2019s \u201chuman-orchestrated, AI-performed\u201d principle, and it also shows that orchestration is cognitively substantive. It does not show that the human\u2019s contribution was small: unit presence says nothing about weight, and a single decision can determine a whole direction.')
p('**Knowledge as a type.** Treating knowledge as a contribution produced a measurable but sparse signal. Half of the AI units supplied knowledge, yet explicit evidence of transfer was found in a handful of tags. In traces, novelty to the receiver is rarely stated, so an observable-trace design will under-detect epistemic transfer; stated limits are therefore part of the finding.')
p('**Accountability.** If the AI makes autonomous decisions, the reported dichotomy of human decides and AI executes is incomplete. The autonomous flag provides a first measure of AI-led execution that can be compared across projects and revisions.')
p('**Method.** LLM coders from other families reached substantial agreement on K, P and D and weak agreement on the catch-all M and on execution. This echoes the expectation, from earlier work on LLM-assisted deductive coding, that agreement on multi-category schemes can lag behind agreement between human experts (Xiao et al., 2023), and it underlines the need for human reference coding.')

h1('Limitations')
p('This is one project with 13 human units, so all figures are descriptive. The designer, most AI content and the sub-agents share a model family, the coders saw actor hints and truncated text, and no human reference coding exists yet. The typology was developed on the same project it was applied to; only coding after freeze counts as evaluation. Human thinking that never entered the trace is invisible. Several works that would ground origin and uptake tracing (for example on grounding and linkography) were not accessible to us, and some sources were read in preprint or third-party copies; claims about them are limited accordingly.')

h1('Conclusion')
p('Cognitive contributions can be typed from interaction traces: independent coders from two other model families agreed substantially on Knowledge, Proposal and Decision, and the first distribution of a real project suggests that the human committed and regulated while the AI supplied knowledge and proposals, with autonomous AI decisions as a further layer. Metacognition and execution need sharper definitions. Because this paper is part of the data it analyses, each revision changes the evidence; we treat that iteration as a feature of the method and document it in the workflow appendix.')

h1('Acknowledgements and Use of Generative AI')
p('This manuscript, the coding standard, the analysis pipeline and the workflow appendix were produced by AI agents (primary agent claude-sonnet-5.5; sub-agents; coders GPT-6.1-sol and Gemini-4-argon) under the direction, review and decisions of the human orchestrator, who is responsible for the content. Authors, affiliations and acknowledgements are withheld for anonymous review. The complete process is documented in the workflow appendix.')

h1('References')
refs = json.load(open(os.path.join(ROOT, 'research', 'references_crossref.json'), encoding='utf-8'))
def initials(given):
    g = re.sub(r'\(.*?\)', '', given or '').strip()
    out = []
    for w in g.split():
        out.append('-'.join(x[0] + '.' for x in w.split('-') if x))
    return ' '.join(out)
def authors(key):
    r = refs[key]; names = []
    for a in r['authors']:
        fam, giv = a.split(', ', 1) if ', ' in a else (a, '')
        names.append('%s, %s' % (fam, initials(giv)))
    if r['n_authors'] > len(names): names = names[:19] + ['\u2026'] + ['et al.']
    if len(names) == 1: return names[0]
    if len(names) == 2: return ' & '.join(names)
    return ', '.join(names[:-1]) + ', & ' + names[-1]
def article(key, italic_container=True):
    r = refs[key]; vol = r.get('volume'); iss = r.get('issue'); pg = (r.get('page') or '').replace('-', '\u2013')
    s = '%s (%s). %s. *%s*' % (authors(key), r['year'], r['title'].rstrip('.'), r['container'])
    if vol: s += ', *%s*' % vol
    if iss: s += '(%s)' % iss
    if pg: s += ', %s' % pg
    return s + '. https://doi.org/' + r['doi']
R = []
R.append(article('S075').replace('*24*', '*24*'))
R.append(article('S002'))
R.append(article('S074').replace(', 532.', ', 532\u2013550.'))
R.append(article('S022').replace('Metacognition and cognitive monitoring: A new area of cognitive\u2013developmental inquiry', 'Metacognition and cognitive monitoring: A new area of cognitive\u2013developmental inquiry'))
R.append(article('S029'))
R.append(article('S013'))
R.append(article('S045'))
R.append('Handa, K., Tamkin, A., McCain, M., Huang, S., Durmus, E., Heck, S., Mueller, J., Hong, J., Ritchie, S., Belonax, T., Troy, K. K., Amodei, D., Kaplan, J., Clark, J., & Ganguli, D. (2025). *Which economic tasks are performed with AI? Evidence from millions of Claude conversations*. arXiv. https://doi.org/10.48550/arXiv.2503.04761')
R.append(article('S061'))
R.append(article('S072'))
R.append(article('S014'))
R.append(article('S001'))
R.append(article('S076'))
R.append(article('S047'))
R.append(article('S051'))
R.append(article('S064'))
R.append(article('S008').replace(', 246.', ', 246\u2013275.'))
R.append('Panickssery, A., Bowman, S. R., & Feng, S. (2024). *LLM evaluators recognize and favor their own generations*. arXiv. https://doi.org/10.48550/arXiv.2404.13076')
R.append(article('S030'))
R.append('Simon, H. A. (1960). *The new science of management decision*. Harper.')
R.append(article('S059'))
R.append(article('S035'))
R.append(article('S058'))
R.append(article('S068'))
R = sorted(R, key=lambda s: re.sub(r'[^a-z]', '', s.lower()))
for s in R: P.append(('ref', s))
build(P, os.path.join(OUT, 'ICIS_PDW_paper_v1.docx'))
open(os.path.join(OUT, 'references_v1.txt'), 'w', encoding='utf-8').write('\n'.join(R))
print('built', len(P), 'blocks;', len(R), 'refs')
words = sum(len(b[1].split()) for b in P if b[0] in ('p', 'h1', 'h2') )
print('words (excluding refs/tables):', words)
