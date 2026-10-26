import json, urllib.request, urllib.parse, sys, io, re, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
Q = [
 "Baird Maruping The Next Generation of Research on IS Use: A Theoretical Framework of Delegation to and from Agentic IS Artifacts",
 "Fugener Grahl Gregory Kuhl Cognitive Challenges in Human-Artificial Intelligence Collaboration: Investigating the Path Toward Productive Delegation",
 "Berente Gu Recker Santhanam Managing Artificial Intelligence",
 "Susarla Gopal Thatcher Sarker The Janus Effect of Generative AI: Charting the Path for Responsible Conduct of Scholarly Activities in Information Systems",
 "Leonardi When Flexible Routines Meet Flexible Technologies: Affordance, Constraint, and the Imbrication of Human and Material Agencies",
 "Seeber Bittner Briggs de Vreede Machines as teammates: A research agenda on AI in team collaboration",
 "Doty Glick Typologies as a Unique Form of Theory Building: Toward Improved Understanding and Modeling",
 "Benbasat Goldstein Mead The Case Research Strategy in Studies of Information Systems",
 "Dellermann Ebel Sollner Leimeister Hybrid Intelligence",
 "Gronsund Aanestad Augmenting the algorithm: Emerging human-in-the-loop work configurations",
 "Fugener Grahl Gregory Kuhl Will Humans-in-the-Loop Become Borgs? Merits and Pitfalls of Working with AI",
 "Schuetz Venkatesh The Rise of Human Machines: How Cognitive Computing Systems Challenge Assumptions of User-System Interaction",
]
FIELDS = "DOI,title,author,issued,container-title,volume,issue,page,type,abstract"
for q in Q:
    url = "https://api.crossref.org/works?rows=2&select=" + FIELDS + "&query.bibliographic=" + urllib.parse.quote(q)
    for a in range(3):
        try:
            m = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "icis-pdw-research/1.0 (mailto:none)"}), timeout=40))["message"]["items"]
            break
        except Exception as e:
            m = []; time.sleep(3)
    print("\nQ:", q[:90])
    for it in m:
        au = "; ".join("%s %s" % (x.get("family", ""), (x.get("given", "") or "")[:1]) for x in it.get("author", [])[:5])
        ab = re.sub(r"<[^>]+>", "", it.get("abstract", ""))[:60]
        print("  ", it.get("DOI"), "|", (it.get("title") or [""])[0][:100], "|", au, "|", it.get("issued", {}).get("date-parts", [[None]])[0][0], "|", (it.get("container-title") or [""])[0][:40], it.get("volume"), it.get("issue"), it.get("page"), "| abs:", bool(it.get("abstract")))
