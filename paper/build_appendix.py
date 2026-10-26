import csv, json, os, re, sys
sys.path.insert(0, r'<project>\research\tools')
import docx_builder
docx_builder.HEADER_TITLE = 'Workflow Appendix'
from docx_builder import build
ROOT = r'<project>'
LOG = os.path.join(ROOT, 'records', 'logs')
def rd(n): return list(csv.DictReader(open(os.path.join(LOG, n), encoding='utf-8-sig')))
def clean(s, n=240):
    s = s or ''
    s = re.sub(r'[A-Za-z]:\\[^\s",;)]+', '[local path]', s)
    s = s.replace('<user>', 'human').replace('an organiser', 'an organiser')
    # identifying resource names and credential variable names are masked. Chinese originals stay.
    s = re.sub(r'https://github\.com/[github-user][^\s",;)]*', '[repository URL]', s)
    s = s.replace('[github-user]', '[github-user]')
    s = re.sub(r'\bming-[A-Za-z0-9.\-]*', '[resource]', s)
    s = s.replace('AZURE_OPENAI_ / OPENAI_API_KEY', 'the image service variables').replace('OPENAI_API_KEY', 'the image service key variable').replace('AZURE_OPENAI_', 'the image service variables')
    s = re.sub(r'\s{2,}', ' ', s)
    s = re.sub(r'[\u2013\u2014]', '-', s).replace(';', ',')
    s = s.replace('\n', ' ').strip()
    return s if len(s) <= n else s[:n].rsplit(' ', 1)[0] + ' ...'
P = []
def p(t): P.append(('p', t))
def h1(t): P.append(('h1', t))
def h2(t): P.append(('h2', t))
P.append(('title', 'Workflow Appendix: How a Human Orchestrator and AI Agents Produced This Paper'))
p('This appendix documents the research workflow of the submission. It follows the items required by the call, namely a chronological map, models and tools, representative prompts, errors and abandoned approaches, material human interventions, verification steps, artifact availability and a contribution account. The complete logs, codebooks, scripts and figure assets are in the artifact bundle. The raw session exports are withheld for the reasons given in Section G. Identifying names, credentials and local paths are removed in this document. All text of the paper and of this appendix and every figure was produced by AI agents. The human typed no manuscript text and gave instructions in conversation.')

h1('A. Chronological Workflow Map')
P.append(('table', [['Stage', 'What happened', 'Main actors'],
    ['1 Ideation', 'The human forwarded the workshop call, proposed the topic of cognitive contribution distribution and asked for an assessment. The AI judged fit, listed risks and suggested a process-log method. The human decided to open a dedicated project (I004, I005).', 'Human, AI'],
    ['2 Task framing and recording', 'The AI read the call files and summarised duties and tensions. The human fixed scope, self-reference, project-level recording of every session, verified references and page limits. The AI built the recording mechanism, project rules and a project skill (I002, I003, I007).', 'Human, AI'],
    ['3 Literature survey', 'The human rejected the AI\u2019s memory-based taxonomy and demanded a survey (I010). Three sub-agents surveyed cognition, human-AI contribution and coding methods, and returned 75 candidate sources with bibliographic verification.', 'Human, AI, sub-agents'],
    ['4 Full-text reading', 'The human asked for original texts (I011). Seven sub-agents read open versions and wrote notes with access levels. Two crashed on a PDF error and were rerun. Unreachable closed sources were skipped by human decision (I012).', 'Human, AI, sub-agents'],
    ['5 Framework and codebook', 'The human corrected the AI\u2019s treatment of knowledge as a dimension and set four types (I012). The AI drafted framework v0.1 and v0.2, then codebook v1.0 with a response-level unit and multi-label tags. The human ruled on boundary cases and fixed the unit (I013, I014, I015).', 'Human, AI'],
    ['6 First coding run', 'The AI built coding packets, and GPT-6.1-sol and Gemini-4-argon coded 106 units independently under codebook v1.0. Agreement was computed with several statistics.', 'AI, coders'],
    ['7 Research questions and v1.1', 'The human set qualitative research questions and the definition of mixed contributions, and ruled on example cases (I017 to I021). The AI drafted codebook v1.1, which the human approved (I022). The same units were recoded and compared.', 'Human, AI, coders'],
    ['8 Full coding and analysis', 'The corpus was extended and coded under v1.1 (146 units). The AI carried out the qualitative analysis of existence, distribution and transitions.', 'AI, coders'],
    ['9 Figures and manuscript', 'The AI drew flat figures that the human rejected (I024) and then redrew them with the Sivia workflow. The human approved whole-figure drafts (I029) and asked for concrete examples in the speech bubbles (I030). A second agent session on another model redrew both figures and the human rated the result as poor (I034 to I036). That session finished Figure 2 after a model change, and Figure 1 was completed in the main session (I037, I038). The AI drafted the manuscript under the human-style writing constraints, and this appendix.', 'Human, AI, image model'],
    ['10 Audit and repair of the record', 'While auditing the second session, the primary agent found that its own run of the sync script had replaced 29 raw session files with help text. It rebuilt every session file from the OpenCode database and rewrote the script (E057, E058). The account is in Section E.', 'Human, AI'],
    ['11 Structure and layout review', 'The human noticed that the paper had no abstract, that the Introduction was short and that some pages ended in white space (I040). The AI measured the section proportions of 16 ICIS papers and found that the template keeps the abstract out of the paper file. It rewrote the Introduction with concrete content, added eight verified sources and a coding excerpt, repaired a citation that was missing from the reference list and removed the gaps (E063 to E067).', 'Human, AI'],
    ['12 Framing revision', 'On 26 October a co-author judged that the paper did not read as an information systems paper, and the human added three problems with the research questions (I041, I042). The human chose to restructure it as a conceptual paper positioned in IS theory. The AI set off plain research questions, added an IS background from nine verified sources, derived delegation episodes and the fate of AI proposals from the coded units, and wrote three propositions. The human then rejected the shaded question box and the grid tables, asked for the original title and wording to be kept, and asked for the figures to fill the pages (I043 to I045, E075). While editing one label of Figure 1 the AI overwrote the final figures with an earlier design and restored them (E073).', 'Human, AI'],
    ['13 Recode and layout', 'Following the human rule and request, both coders recoded the 146 earlier units and 119 later ones under codebook v1.1 (run 2, E076). Run 2 replaced run 1 in all counts, and Table A11 compares the runs. The AI rebuilt the mechanism analysis on the extended corpus, built Figure 3, rebuilt Figure 2 after finding that it still showed the counts of run 1 (E080), cut about 600 words to bring the body back to 8 pages, moved Figure 1 into Research Design and compacted the tables. The human dropped the Use of Generative AI section because the submission form has the item, after the AI had checked the call for papers (I045, I046, E078, E079).', 'Human, AI, coders'],
    ['14 Submission package', 'The AI assembled the single PDF, drafted the text of every form field and built a redacted artifact bundle (I047). A scan of the appendix found garbled rows, resource names that contain the author\u2019s first name and a prompt description in the imperative, and these were repaired. The human asked that the verbatim originals be kept, and the Chinese wording of seven messages was restored from the raw sessions (I048, E082, E083). The raw session exports are withheld because a pattern-based redaction cannot make them safe with certainty (E084).', 'Human, AI']],
    [1.35, 4.2, 0.95]))
P.append(('caption', 'Table A1. Chronological map of the project.'))

h1('B. Models, Agents, Tools and Environment')
P.append(('table', [['Role', 'System', 'Notes'],
    ['Primary agent', 'claude-sonnet-5.5 (agent name openwork)', 'Run in OpenCode 1.18.30 through OpenWork 0.18.59. Sampling settings are not exposed to the agent. Model, agent name and system prompt of every message are in the raw sessions.'],
    ['Sub-agents', 'claude-sonnet-5.5 (general sub-agent type)', 'Literature survey and full-text reading. Each is a child session of the main session. Prompts required compliance with the project rules.'],
    ['Independent coders', 'GPT-6.1-sol, Gemini-4-argon', 'Run through the same agent framework in isolated directories that held only the codebook and unit packets. Chunks of up to 20 units. Run 2 used four parallel jobs of 136 units, two per model.'],
    ['Image model', 'Azure OpenAI image deployment (gpt-image-2.5 family)', 'Three icon sheets at 1536 by 1024, high quality. Each call is recorded with prompt and hash.'],
    ['Bibliographic services', 'Crossref, OpenAlex, DataCite, arXiv, OpenLibrary', 'Used for existence checks and open-access location. Access was limited to legal sources.'],
    ['Local tools', 'Python 3.11 (pypdf, Pillow, numpy, matplotlib, python-docx), draw.io desktop, Microsoft Word, Windows PowerShell 5.1', 'Windows 10.0.26300. Word was used only to count pages.'],
    ['Figure model', 'opencode big-pickle and claude-sonnet-5.5', 'A second agent session redrew the figures. The first part of it (intermediate versions of Figures 1 and 2) ran on big-pickle. After the human rated the aesthetics as poor (I036) the session continued on claude-sonnet-5.5, which redrew Figure 2. Figure 1 was redrawn in the main session with the same drawing library. Some log rows call big-pickle MiniMax-Flash, which the session records do not confirm.'],
    ['Figure method', 'Sivia workflow: full prompts checked against the template length, whole-figure raster drafts from an Azure OpenAI image model and human approval, then 30 icon assets with key-colour cut-out and quality checks. The final figures are drawn through the live draw.io tools and checked by the live audit, a geometry check, a blank-area check, and renders viewed in colour, in grey and at print size. Figure 3 was built the same way and audited with 0 hard failures and 0 warnings (V061).', 'The first editable figures were generated as XML files by a Python script because the live tools were not available, and an earlier statement that the Sivia workflow had been used for them was wrong. The human rejected those figures and two later versions. The image call was ported to Python because the original script needs Node.']],
    [1.2, 2.2, 3.1]))
P.append(('caption', 'Table A2. Models, agents and tools.'))

h1('C. Representative Prompts and Instructions')
p('Human instructions were given in Chinese and are paraphrased here. The first project instruction asked the AI to read the call and to set the deliverables, namely a paper, a theory-grounded coding standard, a provenance-tracing method and skills. It also asked for a full record of the collaboration sessions. A decisive redirect asked that the externalised forms of cognition be modelled from existing research and not guessed in conversation. Later instructions fixed the coding unit as one model response and named the two coder models. They defined mixed contributions by explicit expression from both actors and required that writing and figures follow human-style constraints. The last redirects asked that the research questions stand out and read plainly, that they gain theoretical abstraction, and that the findings explain mechanisms and not only count (I042). Later instructions asked for a plain bullet list instead of a shaded box, three-line tables, a recode, and figures arranged so that no page keeps a large blank area (I043, I044).')
p('Prompts that the AI wrote to sub-agents began with the project rules and a research brief. The literature prompts asked for verified sources only and told the agent to mark unverified items. The reading prompts required notes with an access level for each source and short quotations with locators. They also required a statement that a source was not accessed instead of filling gaps from memory. The coder prompt told each coder to read the coding manual and apply it to every unit of the packet. It also told each coder to code only what is observable and to take the actor hint as the actor of the tags. Each coder was to write one JSON line per unit in the schema of the manual and to read no other files.')

h1('D. Material Human Interventions')
inter = rd('interventions.csv')
rows = [['ID', 'Stage', 'Type', 'Intervention and reason']]
VERB = json.load(open(os.path.join(ROOT, 'submission', 'verbatim_map.json'), encoding='utf-8'))
def with_verbatim(iid, summ):
    """Replace garbled or mixed Chinese in a log summary by the verbatim original from the raw session. The English paraphrase stays."""
    v = VERB.get(iid)
    if not v: return summ
    if iid == 'I022': return re.sub(r"\('[^)]*?'\)", '(\u201c' + v + '\u201d)', summ, count=1)
    m = re.match(r'^(.*?:\s*)(.*?)\s*(\([A-Za-z].*\))\s*$', summ, re.S)
    if not m: return summ
    return m.group(1) + '\u201c' + v + '\u201d ' + m.group(3)
for r in inter:
    n_ = 700 if r['intervention_id'] in VERB else 330
    rows.append([r['intervention_id'], r['stage'], r['type'], clean(with_verbatim(r['intervention_id'], r['summary']), n_)])
P.append(('table', rows, [0.45, 0.9, 1.2, 3.95]))
P.append(('caption', 'Table A3. Human interventions recorded during the project.'))

h1('E. Errors, Abandoned Approaches and Responses')
ev = rd('events.csv')
rows = [['ID', 'Type', 'Event and response']]
for r in ev:
    txt = clean(r['description'], 280)
    resp = clean(r['response'], 150)
    rows.append([r['event_id'], r['event_type'], txt + (' Response: ' + resp if resp and resp.lower() != 'n/a' else '')])
P.append(('table', rows, [0.5, 1.2, 4.8]))
P.append(('caption', 'Table A4. Events, errors and responses.'))

h2('The Record Incident of 22 October')
p('One error damaged the record itself and is told in full here. The recording script exported each session with the command opencode export and wrote the output to the raw archive without checking it. The command line tool was upgraded after the previous run of the script and before the audit, and the same command then printed its help text. The primary agent ran the script at the start of its audit of the figure redraw session on 22 October, and the help text replaced the raw files of 29 sessions (E057). The agent saw that every session showed zero messages and an identical file size, and it stopped to investigate.')
p('The first repair used the new export command. It restored the 29 files in a format that omits messages removed by context compaction, and the agent ran the script again before comparing the restored files with the earlier snapshots. That second run wrote the same format over 11 further files, among them the main session. The comparison then showed that the figure redraw session had kept 1.3 thousand characters of assistant text where the earlier export held 68.9 thousand.')
p('The OpenCode database still held every message. The agent opened it read-only and rebuilt every session in the earlier format and in the new format, which holds all messages written since the upgrade. It rewrote the script so that it reads the database, writes both formats and refuses to replace a file with a version that has fewer messages. For the figure redraw session the rebuilt file matched the surviving snapshot in all 323 messages. For the other 40 sessions only the message counts could be compared with the counts logged before the incident (E058). The superseded files are kept in the repository, and the coding corpus of 146 units had been built before the incident.')
p('The incident also bears on the argument of the paper. The error arose in work that the AI performed, the AI found it while carrying out a human request to check another session (I037), and the AI made the first repair mistake. The human then decided that the incident should be disclosed in this appendix (I039). The case shows detection and repair by the agent, and it shows the human holding the decision about what the record says.')
P.append(('table', [['Time on 22 Oct', 'Step', 'Result'],
    ['17:11', 'Last successful run of the script before the upgrade', 'All sessions exported in the earlier format.'],
    ['20:37', 'Run of the script by the primary agent at the start of the audit', '29 raw files replaced by help text, zero messages (E057).'],
    ['20:39', 'First repair with the new export command', '29 files restored in a format without compacted messages.'],
    ['20:40', 'Second run of the script', '11 further files, among them the main session, written in that format.'],
    ['20:49', 'Comparison of the two formats and rebuild from the database', 'Earlier format rebuilt for 41 sessions, identity checked on one session (V023, V024).'],
    ['20:51', 'Script rewritten and run again', 'Both formats written, no file replaced by a shorter one.']],
    [0.9, 2.8, 2.8]))
P.append(('caption', 'Table A5. Timeline of the record incident.'))

h1('F. Verification and Validation')
ver = rd('verification.csv')
rows = [['ID', 'Target', 'Method', 'Result and detail']]
for r in ver:
    rows.append([r['verification_id'], clean(r['target'], 90), clean(r['method'], 40), clean(r['result'] + '. ' + r['details'], 260)])
rows.append(['V009', 'Manuscript text', 'Style checklist', 'Searched for dashes, semicolons, multiple colons, short and long sentences and defensive phrases. Findings were fixed and the check was rerun until clean.'])
rows.append(['V010', 'Manuscript layout', 'Page count', 'Rendered to PDF with a word processor. Main text fills 8 pages, references start on page 9.'])
rows.append(['V011', 'Reference list', 'Bibliographic match', '23 references matched in Crossref, DataCite or OpenLibrary. Author lists were taken from the records. End pages of three entries (Mintzberg et al., Eisenhardt, Hevner et al.) are missing or differ in the Crossref record and need human confirmation. The list now holds 40 references, and the entries added later are verified in their own rows (V042 to V054).'])
rows.append(['V012', 'Coding agreement', 'Statistics', 'Percent agreement, Cohen kappa and Krippendorff alpha with 2,000-resample bootstrap intervals for each actor-type presence variable. Cross-model coding with two model families.'])
P.append(('table', rows, [0.5, 1.7, 1.2, 3.1]))
P.append(('caption', 'Table A6. Verification steps. Human re-verification of references with other tools is planned before submission.'))

h1('G. Data, Code and Artifact Availability')
p('The artifact bundle holds the unit tables with the full text of every coded unit and the redacted verbatim human messages. It also holds the four structured logs, the session registry and the coder outputs of every run. It further holds codebook versions 1.0 and 1.1 with SHA-256 hashes, the analysis and build scripts and the figure sources with generation prompts and quality reports. It holds the structure review against ICIS papers and the project rules and logging skill. Codebook v1.0 has hash d9fc917f6a6c9b520b92f51d8250465d836d5af4f883a07cb340e6e3785e7d9a and v1.1 has hash 2ccb4592396328910b92fc43ff6b6ae6a2df410a45f36c4dedadedab8a8fc266. The stable link is given in the artifact availability statement of the submission form. The raw session exports (69 sessions, about 130 MB) are withheld. Their tool outputs contain local paths, user and resource names and forwarded third-party email text, and a pattern-based redaction cannot make them safe with certainty. They can be provided to reviewers on request. Copyrighted source copies read during the project, among them the repository copy of Gregor (2006), are not redistributed. In the released copies, user names, local paths, email addresses, an organiser\u2019s name and cloud resource names are masked, and the Chinese wording of the human messages is kept. The unmasked verbatim record is held privately with SHA-256 sums.')

h1('H. Human-AI Contribution Account')
P.append(('table', [['Function', 'Human', 'AI'],
    ['Problem formulation', 'Proposed the topic, restricted the data to the project, formulated the first research questions in conversation and, after a co-author\u2019s comment, redirected them toward plain wording and theoretical abstraction.', 'Assessed fit and risks, offered candidate questions, refined definitions and rewrote the question block.'],
    ['Literature identification', 'Required a survey first, demanded original texts and skipped closed sources.', 'Ran the surveys, verified bibliographic records, read open texts and wrote notes.'],
    ['Theory development', 'Proposed the first three-way split, reframed knowledge as a type and renamed expression or design as Proposal.', 'Synthesised the cognition and decision literature, drafted the typology and boundary rules, searched and verified the IS background and drafted the delegation and commitment propositions.'],
    ['Research design', 'Fixed the unit as one model response, the qualitative design, the coder models and the criterion for mixed contributions.', 'Operationalised the unit, built the coding pipeline and the version-freeze procedure.'],
    ['Analysis', 'Ruled on example cases and boundary cases.', 'Ran the coders, computed agreement and carried out the qualitative analysis.'],
    ['Interpretation', 'Adjudicated definitions and examples and judged the three propositions reasonable. The mechanisms have not been reviewed unit by unit.', 'Drafted all interpretations of existence, distribution, transitions and mechanisms.'],
    ['Writing', 'Set structure, style constraints and the page target and rejected several versions. Typed no text of the manuscript or this appendix (I049).', 'Wrote all text of the manuscript and this appendix and produced every figure and table.'],
    ['Verification', 'Halted premature drafting and will re-check references with other tools.', 'Checked references and sub-agent notes and ran the style and layout checks.'],
    ['Revision', 'Rejected several figure versions and the page layout, decided that the record incident be disclosed, relayed the co-author\u2019s comment, chose the conceptual restructuring, rejected the box and grid tables, required a recode and full pages, and dropped the AI-use section.', 'Rebuilt the figures, repaired the record, extended the corpus and revised every version.']],
    [1.35, 2.6, 2.55]))
P.append(('caption', 'Table A7. Contribution account by research function.'))

h1('I. Coding Agreement and Coded Examples')
p('This section holds the tables that were moved out of the main text. Table A8 gives agreement between the two coders on actor-type presence for all 265 units of run 2. Table A9 shows five consecutive units with the tags of both coders, primary tag first. Table A10 gives one exemplar unit for every actor-type pair that both coders tag. Table A11 compares the two runs on the 146 units that both coded.')
TA = json.load(open(os.path.join(ROOT, 'paper', 'tables_for_appendix.json'), encoding='utf-8'))
P.append(('table', TA['agree'], [1.7, 1.0, 0.7, 1.6, 1.6]))
P.append(('caption', 'Table A8. Agreement between the coders on actor-type presence (265 units, run 2).'))
P.append(('table', TA['cod'], [0.75, 0.85, 3.0, 0.95, 0.95]))
P.append(('caption', 'Table A9. Five consecutive units with the tags of both coders, primary tag first (K Knowledge, P Proposal, D Decision, M Metacognition, X Execution).'))
P.append(('table', TA['ex'], [1.0, 1.1, 4.4]))
P.append(('caption', 'Table A10. One exemplar unit for each actor-type pair that both coders tag.'))
P.append(('table', TA['runs'], [2.6, 1.3, 1.3, 1.3]))
P.append(('caption', 'Table A11. Run 1 and run 2 on the 146 units that both coded: kappa between the coders for each actor-type presence variable, and the repeat rate of each coder against its own run 1.'))
APP = os.path.join(ROOT, 'paper', 'ICIS_PDW_workflow_appendix.docx')
build(P, APP)
# continuous page numbers after the 10 pages of main paper and references (the single submission PDF)
import docx as _docx
from docx.oxml import OxmlElement as _OE
from docx.oxml.ns import qn as _qn
_d = _docx.Document(APP)
for _s in _d.sections:
    _pg = _s._sectPr.find(_qn('w:pgNumType'))
    if _pg is None:
        _pg = _OE('w:pgNumType'); _s._sectPr.append(_pg)
    _pg.set(_qn('w:start'), '11')
_d.save(APP)
print('appendix built', len(inter), len(ev), len(ver))
