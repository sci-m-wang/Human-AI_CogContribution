import json, glob, os, csv, sys
from collections import Counter, defaultdict
TMP=os.environ['TEMP']
ROOT=r'<project>'
OUT=os.path.join(ROOT,'research','coding','final'); os.makedirs(OUT,exist_ok=True)
def load(labels):
    r={}
    for lab in labels:
        for f in sorted(glob.glob(os.path.join(TMP,'icis_coders',lab,'result_*.jsonl'))):
            for line in open(f,encoding='utf-8'):
                line=line.strip()
                if line:
                    o=json.loads(line); r[o['unit_id']]=o
    return r
C={'gpt':load(['gpt11','gpt11n']),'gemini':load(['gemini11','gemini11n'])}
units=list(csv.DictReader(open(os.path.join(ROOT,'research','coding','units_all.csv'),encoding='utf-8-sig')))
new_ids={u['unit_id'] for u in csv.DictReader(open(os.path.join(ROOT,'research','coding','units_new_40.csv'),encoding='utf-8-sig'))}
FREEZE_MS=int(sys.argv[1]) if len(sys.argv)>1 else 0
U={u['unit_id']:u for u in units}
miss=[u for u in U if u not in C['gpt'] or u not in C['gemini']]
print('units',len(U),'coded gpt',len(C['gpt']),'gemini',len(C['gemini']),'missing',len(miss))
def na(a):
    a=(a or '').lower(); return 'human' if a.startswith('human') else ('AI-subagent' if 'sub' in a else 'AI-primary')
def kind(u):
    h=u['actor_hint']; return 'human' if h=='human' else ('AI-subagent' if h=='AI-subagent' else 'AI-primary')
def tags(cod,uid):
    k=kind(U[uid]); return [t for t in C[cod].get(uid,{}).get('tags',[]) if na(t.get('actor'))==k]
def ty(t): return (t.get('type') or '?')[:1].upper()
def sub(t): return t.get('subtype') or ''
def prim(cod,uid):
    ts=tags(cod,uid); pr=[t for t in ts if t.get('primary')]; t=(pr or ts or [None])[0]
    return ty(t) if t else '-'
def present(cod,uid): return set(ty(t) for t in tags(cod,uid))
G=['human','AI-primary','AI-subagent']
ids_by={g:[u for u in U if kind(U[u])==g] for g in G}
# set label
def setlab(u):
    return 'after_v1.1_freeze' if (FREEZE_MS and int(U[u]['time'])>FREEZE_MS) else 'dev'
# 1 existence + exemplars
rows=[]; ex=defaultdict(list)
for g in G:
    for T in 'KPDMX':
        agreed=[u for u in ids_by[g] if T in present('gpt',u) and T in present('gemini',u)]
        either=[u for u in ids_by[g] if T in present('gpt',u) or T in present('gemini',u)]
        rows.append(dict(actor=g,type=T,units=len(ids_by[g]),gpt=sum(T in present('gpt',u) for u in ids_by[g]),gemini=sum(T in present('gemini',u) for u in ids_by[g]),agreed=len(agreed),either=len(either)))
        for u in agreed[:40]:
            q=''
            for t in tags('gpt',u):
                if ty(t)==T: q=(t.get('evidence') or {}).get('quote','') if isinstance(t.get('evidence'),dict) else str(t.get('evidence')); break
            ex[(g,T)].append((u,sub(next((t for t in tags('gpt',u) if ty(t)==T),{})),q))
with open(os.path.join(OUT,'existence.csv'),'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
json.dump({f'{k[0]}|{k[1]}':v for k,v in ex.items()},open(os.path.join(OUT,'exemplars.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
for r in rows: print(r)
# 2 stage distribution (tags agreed in presence by both coders: stage taken from gpt tag)
st=Counter()
for g in G:
    for u in ids_by[g]:
        for T in 'KPDM':
            if T in present('gpt',u) and T in present('gemini',u):
                s=[t.get('stage') for t in tags('gpt',u) if ty(t)==T and t.get('stage')]
                st[(g,T,s[0] if s else 'NA')]+=1
with open(os.path.join(OUT,'stage_dist.csv'),'w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['actor','type','stage','units_agreed'])
    for k,v in sorted(st.items()): w.writerow(list(k)+[v])
tot=Counter()
for (g,T,s),v in st.items(): tot[(g,s)]+=v
print('stage totals', sorted(tot.items(), key=lambda x:(x[0][0],-x[1])))
# 3 transitions: within session, cognitive units only (skip X/C/Z/-), primary tag
bysess=defaultdict(list)
for u in sorted(units,key=lambda x:int(x['time'])): bysess[u['session']].append(u['unit_id'])
trans={'gpt':Counter(),'gemini':Counter()}; ex_tr=defaultdict(list); agree_tr=Counter()
for s,ids in bysess.items():
    seqs={}
    for cod in C:
        seqs[cod]=[(u,kind(U[u]),prim(cod,u)) for u in ids if prim(cod,u) in 'KPDM' and prim(cod,u)!='-']
        for a,b in zip(seqs[cod],seqs[cod][1:]):
            key=(('H' if a[1]=='human' else 'AI')+':'+a[2],('H' if b[1]=='human' else 'AI')+':'+b[2])
            trans[cod][key]+=1
            ex_tr[(cod,key)].append((a[0],b[0]))
for cod in C: print(cod,'transitions',sum(trans[cod].values()))
keys=sorted(set(trans['gpt'])|set(trans['gemini']),key=lambda k:-(trans['gpt'][k]+trans['gemini'][k]))
with open(os.path.join(OUT,'transitions.csv'),'w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['from','to','gpt','gemini','example_gpt'])
    for k in keys: 
        e=ex_tr.get(('gpt',k),[]); w.writerow([k[0],k[1],trans['gpt'][k],trans['gemini'][k],'; '.join(f'{a}>{b}' for a,b in e[:3])])
for k in keys[:20]: print(k,trans['gpt'][k],trans['gemini'][k])
# 4 primary agreement and autonomous D
pa=sum(prim('gpt',u)==prim('gemini',u) for u in U); print('primary type agreement',pa,'/',len(U))
au={c:Counter() for c in C}
for c in C:
    for u in U:
        for t in tags(c,u):
            if ty(t)=='D' and t.get('autonomous'): au[c][kind(U[u])]+=1
print('autonomous D',au)
