import json,sys,csv,os
R=r'<project>\research\coding'
U={u['unit_id']:u for u in csv.DictReader(open(os.path.join(R,'units_all.csv'),encoding='utf-8-sig'))}
ex=json.load(open(os.path.join(R,'final','exemplars.json'),encoding='utf-8'))
out=[]
for key in sys.argv[1:]:
    out.append('===== '+key)
    for u,s,q in ex.get(key,[]):
        t=(U[u]['text'] or '').replace('\n',' ')
        out.append(f"{u} [{s}] quote: {(q or '')[:140]}")
open(os.path.join(R,'final','_ex_view.txt'),'w',encoding='utf-8').write('\n'.join(out))
