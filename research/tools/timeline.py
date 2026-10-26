import json,csv,os,glob
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
U=list(csv.DictReader(open(os.path.join(R,'units_all.csv'),encoding='utf-8-sig')))
def na(a):
    a=(a or '').lower(); return 'human' if a.startswith('human') else ('AI-subagent' if 'sub' in a else 'AI-primary')
def kind(u):
    h=u['actor_hint']; return 'human' if h=='human' else ('AI-subagent' if h=='AI-subagent' else 'AI-primary')
def tg(C,u):
    k=kind(u); ts=[t for t in C[u['unit_id']].get('tags',[]) if na(t.get('actor'))==k]
    pr=[t for t in ts if t.get('primary')]; p=(pr or ts or [None])[0]
    return ((p.get('type') or '?')[0]+(p.get('subtype') or '')[1:]) if p else '-', ''.join(sorted(set((t.get('type') or '?')[0] for t in ts)))
out=[]
for u in sorted([x for x in U if x['session']=='S01'],key=lambda x:int(x['time'])):
    g=tg(G,u); m=tg(M,u)
    out.append(f"{u['unit_id']} {'H' if kind(u)=='human' else 'AI'} g:{g[0]}({g[1]}) m:{m[0]}({m[1]}) | {(u['text'] or u['spawned'] or '')[:90]!r}".replace('\n',' '))
open(os.path.join(R,'final','_s01_timeline.txt'),'w',encoding='utf-8').write('\n'.join(out))
