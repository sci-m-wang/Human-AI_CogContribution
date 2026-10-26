"""Add verified references to research/references_crossref.json (Crossref for journal DOIs, DataCite for arXiv DOIs)."""
import json, os, sys, time, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(ROOT, "research", "references_crossref.json")
refs = json.load(open(P, encoding="utf-8"))
H = {"User-Agent": "icis-pdw-research/1.0 (mailto:none)"}
NEW = {
    "S017": ("crossref", "10.1016/j.tics.2016.07.002"),
    "S065": ("crossref", "10.1073/pnas.2305016120"),
    "S068": ("crossref", "10.1145/3581754.3584136"),
    "S066": ("crossref", "10.1162/coli_a_00502"),
    "S067": ("datacite", "10.48550/arXiv.2306.00176"),
    "S070": ("datacite", "10.48550/arXiv.2306.05685"),
    "S043": ("datacite", "10.48550/arXiv.2408.06292"),
}
def get(u):
    for k in range(4):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=40))
        except Exception as e:
            print("retry", u[:70], e); time.sleep(3 * (k + 1))
for key, (svc, doi) in NEW.items():
    if key in refs: print("have", key); continue
    if svc == "crossref":
        m = get("https://api.crossref.org/works/" + urllib.parse.quote(doi))["message"]
        au = ["%s, %s" % (a.get("family", ""), a.get("given", "")) for a in m.get("author", [])]
        yr = (m.get("issued") or m.get("published") or {}).get("date-parts", [[None]])[0][0]
        refs[key] = {"doi": doi, "title": m["title"][0], "authors": au, "n_authors": len(au), "year": yr,
                     "container": (m.get("container-title") or [""])[0], "volume": m.get("volume", ""), "issue": m.get("issue", ""),
                     "page": m.get("page", ""), "type": m.get("type", "")}
    else:
        m = get("https://api.datacite.org/dois/" + urllib.parse.quote(doi.lower()))["data"]["attributes"]
        au = ["%s, %s" % (a.get("familyName", ""), a.get("givenName", "")) for a in m.get("creators", [])]
        refs[key] = {"doi": doi, "title": m["titles"][0]["title"], "authors": au, "n_authors": len(au), "year": m.get("publicationYear"),
                     "container": "arXiv", "volume": "", "issue": "", "page": "", "type": "posted-content"}
    r = refs[key]
    print(key, "|", r["year"], "|", r["title"][:80], "|", r["container"], r["volume"], r["issue"], r["page"], "|", "; ".join(r["authors"][:4]), "| n=", r["n_authors"])
json.dump(refs, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("total", len(refs))
