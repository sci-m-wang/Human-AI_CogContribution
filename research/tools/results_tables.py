import json, glob, os, csv
from collections import Counter, defaultdict
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
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
def present(res,uid,actor):
    return set(t.get('type','')[:1] for t in res[uid].get('tags',[]) if na(t.get('actor'))==actor)
groups={g:[u for u in U if kind(U[u])==g] for g in ['human','AI-primary','AI-subagent']}
rows=[]
for g,ids in groups.items():
    for ty in 'KPDMX':
        pg=sum(ty in present(C['gpt'],u,g) for u in ids); pm=sum(ty in present(C['gemini'],u,g) for u in ids)
        both=sum((ty in present(C['gpt'],u,g)) and (ty in present(C['gemini'],u,g)) for u in ids)
        rows.append(dict(actor=g,n_units=len(ids),type=ty,gpt=pg,gemini=pm,both=both,gpt_pct=round(100*pg/len(ids)),gemini_pct=round(100*pm/len(ids)),both_pct=round(100*both/len(ids))))
with open(os.path.join(OUT,'presence_by_actor_type.csv'),'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
for r in rows: print(r)
# figure: both-coders presence with whiskers min..max
fig,ax=plt.subplots(figsize=(6.4,2.8))
types='KPDM'; width=0.25; x=range(len(types))
cols={'human':'#1f77b4','AI-primary':'#d62728','AI-subagent':'#ff9896'}
for i,g in enumerate(['human','AI-primary','AI-subagent']):
    vals=[];lo=[];hi=[]
    for ty in types:
        r=[q for q in rows if q['actor']==g and q['type']==ty][0]
        mn=min(r['gpt_pct'],r['gemini_pct']); mx=max(r['gpt_pct'],r['gemini_pct'])
        vals.append(r['both_pct']); lo.append(r['both_pct']-r['both_pct']); hi.append(mx-r['both_pct'])
    ax.bar([k+(i-1)*width for k in x],vals,width,label=f"{g} (n={len(groups[g])})",color=cols[g],yerr=[lo,hi],capsize=2,error_kw={'elinewidth':0.8})
ax.set_xticks(list(x)); ax.set_xticklabels(['K Knowledge','P Proposal','D Decision','M Metacognition'],fontsize=8)
ax.set_ylabel('% of units with type present',fontsize=8); ax.set_ylim(0,105); ax.tick_params(labelsize=8); ax.legend(fontsize=7,frameon=False)
plt.tight_layout(); plt.savefig(os.path.join(OUT,'fig_presence.png'),dpi=200)
# provenance: AI-primary P units (either coder) -> next human unit tags
by_sess=defaultdict(list)
for u in units: by_sess[u['session']].append(u['unit_id'])
print('--- AI P units and next human unit')
for s,ids in by_sess.items():
    for i,uid in enumerate(ids):
        if kind(U[uid])!='AI-primary': continue
        p=[c for c in C if 'P' in present(C[c],uid,'AI-primary')]
        if not p: continue
        nxt=next((x for x in ids[i+1:] if kind(U[x])=='human'),None)
        info={c:sorted(set(f"{t.get('type')}{t.get('subtype') or ''}:{t.get('uptake')}" for t in C[c][nxt].get('tags',[]) if na(t.get('actor'))=='human' and t.get('type') in('D','P','M'))) for c in C} if nxt else None
        print(uid,'P by',p,'->',nxt,info)
# totals
tot=Counter()
for c in C:
    for o in C[c].values():
        for t in o.get('tags',[]): tot[(c,na(t.get('actor')),t.get('type','')[:1])]+=1
print(sorted(tot.items()))
