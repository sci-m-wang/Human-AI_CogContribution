import json, urllib.request, sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
H = {"User-Agent": "icis-pdw-research/1.0 (mailto:none)"}
def get(u):
    for a in range(3):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=40))
        except Exception as e: err = e; time.sleep(2)
    return {"error": str(err)}
for d in ["10.5465/amr.1994.9410210748", "10.5465/amr.1994.9410210748 "]:
    o = get("https://api.crossref.org/works/" + d.strip())
    m = o.get("message", {})
    print(d, "|", (m.get("title") or [""])[0], "|", m.get("page"), "|", m.get("volume"), m.get("issue"), "|", (m.get("container-title") or [""])[0])
o = get("https://api.crossref.org/works?rows=3&select=DOI,title,page,volume,issue,issued,container-title&query.bibliographic=Doty+Glick+Typologies+as+a+unique+form+of+theory+building+1994")
for it in o.get("message", {}).get("items", []):
    print(it.get("DOI"), "|", (it.get("title") or [""])[0][:70], "|", it.get("page"), it.get("volume"), it.get("issue"))
o = get("https://api.semanticscholar.org/graph/v1/paper/DOI:10.2307/258704?fields=title,venue,year,journal,authors")
print(o)
# Gregor 2006 full text access check
try:
    r = urllib.request.urlopen(urllib.request.Request("https://misq.umn.edu/misq/article-pdf/30/3/611/1652/3_gregor.pdf", headers=H), timeout=40)
    print("gregor pdf", r.status, r.headers.get("Content-Type"), len(r.read()))
except Exception as e:
    print("gregor pdf fail", e)
