import json, glob, os, csv
from collections import Counter, defaultdict
TMP=os.environ['TEMP']; OUT=r'<project>\research\coding'
def load(label):
    r={}
    for f in sorted(glob.glob(os.path.join(TMP,'icis_coders',label,'result_*.jsonl'))):
        for line in open(f,encoding='utf-8'):
            line=line.strip()
            if line:
                o=json.loads(line); r[o['unit_id']]=o
    return r
C={'gpt':load('gpt'),'gemini':load('gemini')}
units={u['unit_id']:u for u in csv.DictReader(open(os.path.join(OUT,'units_all.csv'),encoding='utf-8-sig'))}
def na(a):
    a=(a or '').lower()
    return 'human' if a.startswith('human') else ('AI-subagent' if 'sub' in a else 'AI-primary')
# 1 unit-kind composition
print('units by actor_hint:',Counter(u['actor_hint'] for u in units.values()))
# 2 actor attribution mismatches: tag actor != actor_hint
mm=Counter()
for cod,res in C.items():
    for uid,o in res.items():
        hint=units[uid]['actor_hint']; hint_n='human' if hint=='human' else ('AI-subagent' if 'subagent' in hint and 'prompt' not in hint else 'AI-primary')
        for t in o.get('tags',[]):
            if na(t.get('actor'))!=hint_n: mm[(cod,hint_n,na(t.get('actor')))]+=1
print('tags whose actor != unit actor_hint:',dict(mm))
# 3 presence shares per coder: share of units of that actor kind with type present
for cod,res in C.items():
    print('==',cod)
    for hint_n,sel in [('human',lambda h:h=='human'),('AI-primary',lambda h:h.startswith('AI-primary')),('AI-subagent',lambda h:h=='AI-subagent')]:
        ids=[u for u,x in units.items() if sel(x['actor_hint'])]
        c=Counter()
        for uid in ids:
            seen=set(t.get('type','')[:1] for t in res[uid].get('tags',[]) if na(t.get('actor'))==hint_n)
            for s in seen: c[s]+=1
        print(hint_n,'units',len(ids),{k:f'{v} ({v/len(ids):.0%})' for k,v in sorted(c.items())})
# 4 primary type distribution per coder per actor
for cod,res in C.items():
    print('== primary',cod)
    for hint_n in ['human','AI-primary','AI-subagent']:
        c=Counter()
        for uid,o in res.items():
            for t in o.get('tags',[]):
                if t.get('primary') and na(t.get('actor'))==hint_n: c[t.get('type','')[:1]]+=1
        print(hint_n,dict(c))
# 5 subtype counts
for cod,res in C.items():
    c=Counter()
    for o in res.values():
        for t in o.get('tags',[]): c[(na(t.get('actor')),str(t.get('subtype')))]+=1
    print('== subtypes',cod,sorted(c.items(),key=lambda x:-x[1])[:25])
# 6 stage by actor (tags)
for cod,res in C.items():
    c=Counter()
    for o in res.values():
        for t in o.get('tags',[]): c[(na(t.get('actor')),t.get('stage'))]+=1
    print('== stage',cod,sorted(c.items(),key=lambda x:-x[1])[:20])
# 7 uptake, epistemic transfer, autonomous, manual_change
for cod,res in C.items():
    up=Counter(); ep=Counter(); au=Counter(); mc=0
    for o in res.values():
        for t in o.get('tags',[]):
            up[(na(t.get('actor')),str(t.get('uptake')))]+=1
            if t.get('type','')[:1]=='K': ep[(na(t.get('actor')),str(t.get('epistemic_transfer')))]+=1
            if t.get('type','')[:1]=='D' and t.get('autonomous'): au[na(t.get('actor'))]+=1
            if t.get('manual_change'): mc+=1
    print('== uptake',cod,dict(up)); print('   epistemic',dict(ep)); print('   autonomous D',dict(au),'manual_change',mc)
# 8 human-tag text anchors for D/M/K/P for inspection
for uid,u in units.items():
    if u['actor_hint']=='human':
        tg={}
        for cod,res in C.items():
            tg[cod]=sorted(set(f"{t.get('type')}{t.get('subtype') or ''}{'*' if t.get('primary') else ''}" for t in res[uid].get('tags',[]) if na(t.get('actor'))=='human'))
        print(uid,u['time'],(u['text'] or '')[:70].replace('\n',' '),tg)
