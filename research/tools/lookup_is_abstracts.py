import json, urllib.request, sys, io, re, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
H = {"User-Agent": "icis-pdw-research/1.0 (mailto:none)"}
def get(url):
    for a in range(3):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=40))
        except Exception as e:
            err = e; time.sleep(3)
    return {"error": str(err)}
DOIS = ["10.25300/misq/2021/15882", "10.1287/isre.2021.1079", "10.25300/misq/2021/16274", "10.1287/isre.2023.ed.v34.n2",
        "10.2307/23043493", "10.2307/248684", "10.1016/j.im.2019.103174", "10.1016/j.jsis.2020.101614", "10.1007/s12599-019-00595-2",
        "10.2307/258704", "10.25300/misq/2021/16553", "10.17705/1jais.00608"]
for d in DOIS:
    o = get("https://api.openalex.org/works/doi:" + d)
    if "error" in o:
        print(d, "ERR", o["error"]); continue
    bib = o.get("biblio", {})
    inv = o.get("abstract_inverted_index") or {}
    words = {}
    for w, pos in inv.items():
        for p in pos: words[p] = w
    ab = " ".join(words[k] for k in sorted(words))
    au = "; ".join(a["author"]["display_name"] for a in o.get("authorships", [])[:6])
    print("\n", d, "|", o.get("display_name"), "|", o.get("publication_year"), "|", au)
    print("   biblio:", bib.get("volume"), bib.get("issue"), bib.get("first_page"), bib.get("last_page"), "| venue:", (o.get("primary_location", {}) or {}).get("source", {}) and o["primary_location"]["source"].get("display_name"))
    print("   ABS:", ab[:1100])
