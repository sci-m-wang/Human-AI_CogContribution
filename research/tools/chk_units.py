import json,csv,os,glob,sys
TMP=os.environ['TEMP']; R=r'<project>\research\coding'
def load(labs):
    r={}
    for lab in labs:
        for f in sorted(glob.glob(os.path.join(TMP,'icis_coders',lab,'result_*.jsonl'))):
            for l in open(f,encoding='utf-8'):
                l=l.strip()
                if l: o=json.loads(l); r[o['unit_id']]=o
    return r
G=load(['gpt11','gpt11n']); M=load(['gemini11','gemini11n'])
U={u['unit_id']:u for u in csv.DictReader(open(os.path.join(R,'units_all.csv'),encoding='utf-8-sig'))}
def na(a):
    a=(a or '').lower(); return 'human' if a.startswith('human') else ('AI-subagent' if 'sub' in a else 'AI-primary')
def kind(u):
    h=u['actor_hint']; return 'human' if h=='human' else ('AI-subagent' if h=='AI-subagent' else 'AI-primary')
def info(C,uid):
    k=kind(U[uid]); ts=[t for t in C[uid].get('tags',[]) if na(t.get('actor'))==k]
    pr=[t for t in ts if t.get('primary')]; p=(pr or ts or [None])[0]
    allt=''.join(sorted(set((t.get('type') or '?')[0] for t in ts)))
    return ((p.get('type') or '?')[0]+(p.get('subtype') or '')[1:] if p else '-')+'('+allt+')'
ids=sys.argv[1:]
out=[f"{u} {kind(U[u])[:2]} g:{info(G,u)} m:{info(M,u)}" for u in ids]
open(os.path.join(R,'final','_chk.txt'),'w',encoding='utf-8').write('\n'.join(out))
