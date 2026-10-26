import json, glob, os, csv
from collections import Counter
TMP=os.environ['TEMP']; OUT=r'<project>\research\coding'
def load(label):
    r={}
    for f in sorted(glob.glob(os.path.join(TMP,'icis_coders',label,'result_*.jsonl'))):
        for line in open(f,encoding='utf-8'):
            line=line.strip()
            if line: o=json.loads(line); r[o['unit_id']]=o
    return r
C={'gpt':load('gpt'),'gemini':load('gemini')}
units=list(csv.DictReader(open(os.path.join(OUT,'units_all.csv'),encoding='utf-8-sig')))
U={u['unit_id']:u for u in units}
def na(a):
    a=(a or '').lower(); return 'human' if a.startswith('human') else ('AI-subagent' if 'sub' in a else 'AI-primary')
def kind(u):
    h=u['actor_hint']; return 'human' if h=='human' else ('AI-subagent' if h=='AI-subagent' else 'AI-primary')
def primary(cod,uid):
    k=kind(U[uid]); tags=[t for t in C[cod][uid].get('tags',[]) if na(t.get('actor'))==k]
    pr=[t for t in tags if t.get('primary')]
    t=(pr or tags or [None])[0]
    return f"{t.get('type','?')[:1]}{(t.get('subtype') or '')[1:]}" if t else '-'
# main timeline: origin session (S02) then main (S01), human + AI-primary units that are ai_response or user_message by human
seq=[u for u in units if u['session'] in('S02','S01') and kind(u) in('human','AI-primary') and not u['actor_hint'].endswith('sub-agent)')]
seq.sort(key=lambda u:int(u['time']))
def short(t,n=110): return (t or '').replace('\n',' ').replace('\r',' ')[:n]
L=[]
L.append('# Examples v0: transitions and mixed-contribution candidates (development set, exploratory)\n')
L.append('Source: codebook v1.0 coding by GPT-6.1-sol and Gemini-4-argon (two independent LLM coders), 106 units. Human messages are in Chinese in the raw data; shown here as raw text. Primary tag per unit = the unit actor\'s tag marked primary (first tag if none). `g:` GPT, `m:` Gemini. Bare approval = a human message whose only tag is D2/C and which is short; excluded from mixed candidates per I019.\n')
L.append('## 1. Main-line sequence (human and primary-AI units, time order)\n')
L.append('| # | unit | actor | g | m | text (first 110 chars) |\n|---|---|---|---|---|---|')
rows=[]
for i,u in enumerate(seq,1):
    g=primary('gpt',u['unit_id']); m=primary('gemini',u['unit_id'])
    rows.append((u['unit_id'],kind(u),g,m))
    if kind(u)=='AI-primary' and not (u['text'] or '').strip() and u['spawned']: tx='[spawns: '+short(u['spawned'],90)+']'
    else: tx=short(u['text'])
    L.append(f"| {i} | {u['unit_id']} | {'H' if kind(u)=='human' else 'AI'} | {g} | {m} | {tx.replace('|','/')} |")
# transitions
def trans(idx):
    c=Counter()
    for a,b in zip(rows,rows[1:]):
        c[(f"{'H' if a[1]=='human' else 'AI'}:{a[idx][0]}",f"{'H' if b[1]=='human' else 'AI'}:{b[idx][0]}")]+=1
    return c
for name,idx in [('GPT',2),('Gemini',3)]:
    L.append(f'\n## 2. Transition counts, {name} primary tags (adjacent units, reference only)\n')
    L.append('| from | to | n |\n|---|---|---|')
    for (a,b),n in sorted(trans(idx).items(), key=lambda x:-x[1])[:14]: L.append(f'| {a} | {b} | {n} |')
# mixed candidates: human unit that follows an AI unit, human has substantive tag (K/P/D1/M1/M2 or D2 with len>40) per both coders
L.append('\n## 3. Mixed-contribution candidates (human unit responding to an AI unit; human text is not a bare approval)\n')
n=0
for a,b in zip(seq,seq[1:]):
    if kind(a)!='AI-primary' or kind(b)!='human': continue
    htxt=(b['text'] or '').strip()
    htags={cod:[(t.get('type','')[:1]+(t.get('subtype') or '')[1:]) for t in C[cod][b['unit_id']].get('tags',[]) if na(t.get('actor'))=='human'] for cod in C}
    both_sub = all(any(x[0] in 'KPM' or x=='D1' for x in htags[c]) for c in C)
    if len(htxt)<40 or not both_sub: continue
    atags={cod:[(t.get('type','')[:1]+(t.get('subtype') or '')[1:]) for t in C[cod][a['unit_id']].get('tags',[]) if na(t.get('actor'))=='AI-primary'] for cod in C}
    n+=1
    L.append(f"### Candidate {n}: {a['unit_id']} -> {b['unit_id']}")
    L.append(f"- AI unit tags g:{atags['gpt']} m:{atags['gemini']}")
    L.append(f"- AI text: {short(a['text'],360)}")
    L.append(f"- Human tags g:{htags['gpt']} m:{htags['gemini']}")
    L.append(f"- Human text: {short(htxt,520)}\n")
# rubber-stamp / short approvals
L.append('## 4. Human units excluded as bare approval or too thin\n')
for a,b in zip(seq,seq[1:]):
    if kind(b)!='human' or kind(a)!='AI-primary': continue
    htxt=(b['text'] or '').strip()
    htags={cod:[(t.get('type','')[:1]+(t.get('subtype') or '')[1:]) for t in C[cod][b['unit_id']].get('tags',[]) if na(t.get('actor'))=='human'] for cod in C}
    both_sub = all(any(x[0] in 'KPM' or x=='D1' for x in htags[c]) for c in C)
    if len(htxt)<40 or not both_sub:
        L.append(f"- {b['unit_id']} g:{htags['gpt']} m:{htags['gemini']}: {short(htxt,160)}")
open(os.path.join(OUT,'examples_v0.md'),'w',encoding='utf-8').write('\n'.join(L))
print('candidates',n,'seq',len(seq))
