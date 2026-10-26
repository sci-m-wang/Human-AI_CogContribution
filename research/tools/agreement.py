import json, glob, os, sys, random, csv, math
from collections import Counter, defaultdict
TMP = os.environ.get('TEMP')
OUT = r'<project>\research\coding'
coders = {'gpt': 'github-copilot/gpt-6.1-sol', 'gemini': 'github-copilot/gemini-4-argon'}
TYPES = ['K','P','D','M','X','C','Z']
ACTORS = ['human','AI-primary','AI-subagent']

def load(label):
    res = {}; bad = 0
    for lab in label.split(','):
        for f in sorted(glob.glob(os.path.join(TMP,'icis_coders',lab,'result_*.jsonl'))):
            for line in open(f, encoding='utf-8'):
                line=line.strip()
                if not line: continue
                try:
                    o = json.loads(line)
                    res[o['unit_id']] = o
                except Exception:
                    bad += 1
    return res, bad

def norm_actor(a):
    a = (a or '').lower()
    if a.startswith('human'): return 'human'
    if 'sub' in a: return 'AI-subagent'
    return 'AI-primary'

def tagset(o):
    s=set()
    for t in o.get('tags',[]):
        ty = str(t.get('type','')).strip().upper()[:1]
        if ty in TYPES: s.add((norm_actor(t.get('actor')), ty))
    return s

def kappa(a,b):
    n=len(a); po=sum(x==y for x,y in zip(a,b))/n
    pa=sum(a)/n; pb=sum(b)/n
    pe=pa*pb+(1-pa)*(1-pb)
    return float('nan') if pe==1 else (po-pe)/(1-pe)

def alpha_nominal(a,b):
    # two coders, no missing, nominal binary
    n=len(a)*2
    o=sum(1 for x,y in zip(a,b) if x!=y)*2   # disagreeing ordered pairs
    counts=Counter(a+b)
    de=0.0
    for c1 in counts:
        for c2 in counts:
            if c1!=c2: de+=counts[c1]*counts[c2]
    de = de/(n*(n-1))
    do = o/n
    return float('nan') if de==0 else 1-do/de

def boot(fn,a,b,B=2000,seed=1):
    rnd=random.Random(seed); n=len(a); vals=[]
    for _ in range(B):
        idx=[rnd.randrange(n) for _ in range(n)]
        v=fn([a[i] for i in idx],[b[i] for i in idx])
        if not math.isnan(v): vals.append(v)
    if len(vals)<50: return (float('nan'),float('nan'))
    vals.sort(); return (vals[int(0.025*len(vals))], vals[int(0.975*len(vals))])

SUF = sys.argv[1] if len(sys.argv) > 1 else ''
A,badA = load('gpt11,gpt11n'); B,badB = load('gemini11,gemini11n')
units = list(csv.DictReader(open(os.path.join(OUT,'units_all.csv'),encoding='utf-8-sig')))
uid = [u['unit_id'] for u in units]
common = [u for u in uid if u in A and u in B]
print('units total',len(uid),'coded A',len(A),'coded B',len(B),'common',len(common),'bad lines',badA,badB)
rows=[]
for ac in ACTORS:
    for ty in TYPES:
        a=[1 if (ac,ty) in tagset(A[u]) else 0 for u in common]
        b=[1 if (ac,ty) in tagset(B[u]) else 0 for u in common]
        if sum(a)+sum(b)==0: continue
        pa=sum(x==y for x,y in zip(a,b))/len(a)
        k=kappa(a,b); al=alpha_nominal(a,b)
        kl,kh=boot(kappa,a,b); al_l,al_h=boot(alpha_nominal,a,b)
        rows.append(dict(actor=ac,type=ty,n=len(a),A_present=sum(a),B_present=sum(b),both=sum(x&y for x,y in zip(a,b)),pct_agree=round(pa,3),kappa=round(k,3),kappa_lo=round(kl,3),kappa_hi=round(kh,3),alpha=round(al,3),alpha_lo=round(al_l,3),alpha_hi=round(al_h,3)))
with open(os.path.join(OUT,'final/agreement_v1.1_all146.csv'),'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())) if rows else None
    if w: w.writeheader(); w.writerows(rows)
for r in rows: print(r)
# type-only (ignoring actor)
print('--- type only')
for ty in TYPES:
    a=[1 if any(t==ty for _,t in tagset(A[u])) else 0 for u in common]
    b=[1 if any(t==ty for _,t in tagset(B[u])) else 0 for u in common]
    if sum(a)+sum(b)==0: continue
    print(ty,'pct',round(sum(x==y for x,y in zip(a,b))/len(a),3),'kappa',round(kappa(a,b),3),'alpha',round(alpha_nominal(a,b),3),'A',sum(a),'B',sum(b))
# primary-type confusion (unit level, primary tag per unit by first actor-hint)
conf=Counter()
for u in common:
    pa=[t for t in A[u].get('tags',[]) if t.get('primary')]; pb=[t for t in B[u].get('tags',[]) if t.get('primary')]
    ta=pa[0].get('type','-')[:1] if pa else '-'; tb=pb[0].get('type','-')[:1] if pb else '-'
    conf[(ta,tb)]+=1
print('--- primary-type confusion (A=gpt rows, B=gemini cols)')
for k,v in sorted(conf.items(), key=lambda x:-x[1])[:20]: print(k,v)
with open(os.path.join(OUT,'final/confusion_primary_v1.1_all146.csv'),'w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['gpt_primary','gemini_primary','count'])
    for k,v in sorted(conf.items(), key=lambda x:-x[1]): w.writerow([k[0],k[1],v])
