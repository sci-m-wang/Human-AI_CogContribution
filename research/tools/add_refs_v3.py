"""Fetch and cache Crossref metadata for the IS references added in the v3 framing revision (verification record V045 to V054)."""
import json, urllib.request, time, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"<project>"
DOIS = {
 "baird2021": "10.25300/misq/2021/15882", "benbasat1987": "10.2307/248684", "berente2021": "10.25300/misq/2021/16274",
 "fugener2022": "10.1287/isre.2021.1079", "gregor2006": "10.2307/25148742", "gronsund2020": "10.1016/j.jsis.2020.101614",
 "leonardi2011": "10.2307/23043493", "seeber2020": "10.1016/j.im.2019.103174", "susarla2023": "10.1287/isre.2023.ed.v34.n2",
}
out = {}
for k, d in DOIS.items():
    for a in range(4):
        try:
            req = urllib.request.Request("https://api.crossref.org/works/" + d, headers={"User-Agent": "icis-pdw-research/1.0 (mailto:none)"})
            m = json.load(urllib.request.urlopen(req, timeout=40))["message"]; break
        except Exception as e:
            m = None; time.sleep(3 * (a + 1))
    if not m: print(k, "FAILED"); continue
    out[k] = dict(doi=d, title=(m.get("title") or [""])[0], authors=[[x.get("family", ""), x.get("given", "")] for x in m.get("author", [])],
                  year=(m.get("issued", {}).get("date-parts") or [[None]])[0][0], container=(m.get("container-title") or [""])[0],
                  volume=m.get("volume"), issue=m.get("issue"), page=m.get("page"))
    print(k, out[k]["year"], out[k]["container"], out[k]["volume"], out[k]["issue"], out[k]["page"], len(out[k]["authors"]), "authors |", out[k]["title"][:70])
json.dump(out, open(os.path.join(ROOT, "research", "references_is_v3.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
