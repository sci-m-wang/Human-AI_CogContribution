import json
r=json.load(open(r'<project>\research\references_crossref.json',encoding='utf-8'))
out=[]
for k in ['S001','S002','S008','S013','S014','S022','S029','S030','S035','S045','S047','S051','S058','S059','S061','S062','S064','S068','S072','S074','S075','S076']:
    v=r[k]; out.append(f"{k} | {v['year']} | n={v['n_authors']} | {'; '.join(v['authors'])} | {v['title']} | {v['container']} | {v.get('volume')} | {v.get('issue')} | {v.get('page')}")
open(r'<project>\research\_refs_view.txt','w',encoding='utf-8').write('\n'.join(out))
