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
U={u['unit_id']:u for u in csv.DictReader(open(os.path.join(R,'units_all.csv'),encoding='utf-8-sig'))}
out=[]
def dq(C,uid,actor_prefix):
    r=[]
    for t in C[uid].get('tags',[]):
        if (t.get('type') or '')[0]=='D' and str(t.get('actor','')).startswith(actor_prefix):
            ev=t.get('evidence'); q=ev.get('quote') if isinstance(ev,dict) else ev
            r.append(f"{t.get('subtype')} auto={t.get('autonomous')} q={str(q)[:110]}")
    return r
for uid,u in U.items():
    if u['actor_hint'].startswith('AI-primary'):
        g=dq(G,uid,'AI'); m=dq(M,uid,'AI')
        if g or m:
            out.append(f"{uid} [{u['actor_hint']}] GPT:{g} | GEM:{m}")
open(os.path.join(R,'final','_aiD.txt'),'w',encoding='utf-8').write('\n'.join(out))
