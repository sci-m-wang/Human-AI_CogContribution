import json, time, urllib.request, urllib.parse, os, sys
dois = {
 'S001':'10.1207/s15430421tip4104_2','S002':'10.1207/s15326985ep3102_2','S008':'10.2307/2392045',
 'S013':'10.1016/j.destud.2003.10.010','S014':'10.1207/s15516709cog1804_1','S022':'10.1037/0003-066x.34.10.906',
 'S029':'10.1080/08923640109527071','S035':'10.1038/s41562-024-02024-1','S047':'10.1145/3706598.3713778',
 'S051':'10.1145/3491102.3502030','S058':'10.3115/981823.981833','S059':'10.1145/3613904.3642902',
 'S061':'10.1080/19312450709336664','S062':'10.1162/coli.07-034-r2','S064':'10.1177/1525822x980100020301',
 'S065':'10.1073/pnas.2305016120','S068':'10.1145/3581754.3584136','S069':'10.1145/3617362',
 'S072':'10.2307/25148625','S074':'10.2307/258557','S075':'10.1177/16094069251383739','S076':'10.1287/isre.14.3.221.16560',
 'S016':'10.1093/analys/58.1.7','S017':'10.1016/j.tics.2016.07.002','S030':'10.5465/amr.2018.0072','S045':'10.1038/s41586-026-10644-y',
}
out = {}
for k,d in dois.items():
    url = 'https://api.crossref.org/works/'+urllib.parse.quote(d)
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={'User-Agent':'icis-pdw-research/1.0 (mailto:[email])'})
            m = json.load(urllib.request.urlopen(req, timeout=40))['message']
            au = m.get('author',[])
            out[k] = dict(doi=d, title=(m.get('title') or [''])[0], authors=['%s, %s'%(a.get('family',''),a.get('given','')) for a in au][:12], n_authors=len(au),
                          year=(m.get('issued',{}).get('date-parts',[[None]])[0][0]), container=(m.get('container-title') or [''])[0],
                          volume=m.get('volume'), issue=m.get('issue'), page=m.get('page'), type=m.get('type'))
            break
        except Exception as e:
            out[k] = dict(doi=d, error=str(e)); time.sleep(3*(attempt+1))
    time.sleep(1.2)
json.dump(out, open(r'<project>\research\references_crossref.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
for k,v in out.items(): print(k, v.get('year'), '|', (v.get('authors') or ['?'])[0], '|', (v.get('title') or v.get('error'))[:70], '|', v.get('container'), v.get('volume'), v.get('issue'), v.get('page'))
