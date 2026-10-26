"""Section shares of the sampled ICIS papers (author versions on arXiv) against the manuscript.
Categories: INT introduction, BG background/related work/theory, MTH method or design or approach, RES results/findings/framework,
DIS discussion/implications, CON conclusion/limitations/future work. Front matter, references, acknowledgements and appendices are excluded.
The mapping of headings to categories was made by reading the heading lists printed by icis_structure.py.
"""
import json, os, re, statistics as st, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
raw = json.load(open(os.path.join(ROOT, "research", "icis_refs", "structure_raw.json"), encoding="utf-8"))
M = {  # heading prefix -> category, applied in order, category carries forward until the next mapped heading
 "2609.33754v2": [("Abstract","ABS"),("Introduction","INT"),("Background","BG"),("Privacy-Preserving Collaborative","MTH"),("Results","RES"),("Datasets","RES"),("Discussion","DIS"),("Limitations","CON"),("Conclusion","CON"),("References","END")],
 "2606.17839v1": [("Abstract","ABS"),("Introduction","INT"),("Related Work","BG"),("Methodology","MTH"),("Results","RES"),("Discussion","DIS"),("Conclusion","CON"),("Acknowledgment","END"),("References","END")],
 "2606.17831v1": [("Abstract","ABS"),("Introduction","INT"),("Related Work","BG"),("Methods","MTH"),("Results","RES"),("Discussion","DIS"),("Conclusion","CON"),("Limitations","CON"),("Acknowledgment","END"),("References","END")],
 "2602.11707v1": [("Abstract","ABS"),("Introduction","INT"),("Fragmentation","BG"),("Discussion","DIS"),("Limitations","CON"),("Conclusion","CON"),("References","END")],
 "2510.08104v1": [("Abstract","ABS"),("Introduction","INT"),("Foundations","BG"),("Methodology","MTH"),("Conceptualizing","RES"),("Theoretical","DIS"),("Conclusion","CON"),("References","END")],
 "2510.00555v1": [("Abstract","ABS"),("Introduction","INT"),("Related Work","BG"),("Method","MTH"),("Results","RES"),("Discussion","DIS"),("Limitations","CON"),("Conclusion","CON"),("References","END")],
 "2510.00552v1": [("Abstract","ABS"),("Introduction","INT"),("Foundation","BG"),("Methodology","MTH"),("Results","RES"),("Discussion","DIS"),("Limitations","CON"),("Conclusion","CON"),("References","END")],
 "2412.13528v1": [("Abstract","ABS"),("Introduction","INT"),("Related Literature","BG"),("Our Proposed","MTH"),("Technical Evaluation","RES"),("Results and Discussion","DIS"),("Limitations","CON"),("Conclusion","CON"),("Acknowledgements","END"),("References","END")],
 "2408.04317v1": [("Abstract","ABS"),("Introduction","INT"),("Related Work","BG"),("Method","MTH"),("Findings","RES"),("Discussion","DIS"),("Conclusion","CON"),("Acknowledgement","END"),("References","END")],
 "2405.01881v3": [("Abstract","ABS"),("Introduction","INT"),("Related Work","BG"),("Problem Formulation","MTH"),("Explanation by","RES"),("Discussion of","DIS"),("Conclusion","CON"),("References","END")],
 "2310.02568v1": [("Abstract","ABS"),("Introduction","INT"),("Theory","BG"),("Method","MTH"),("Results","RES"),("Discussion","DIS"),("Conclusion","CON"),("References","END")],
 "2210.02123v1": [("Abstract","ABS"),("Introduction","INT"),("Background","BG"),("Research Methodology","MTH"),("Pre-Test","RES"),("Conclusion","CON"),("References","END")],
 "2201.05945v1": [("Abstract","ABS"),("Introduction","INT"),("Methodology","MTH"),("Synthesize","RES"),("Future Research","DIS"),("Discussion","DIS"),("Conclusion","CON"),("References","END")],
 "2109.15067v1": [("Abstract","ABS"),("Introduction","INT"),("Theoretical","BG"),("Data and Methods","MTH"),("Preliminary Results","RES"),("Conclusion","CON"),("Current Work","CON"),("Acknowledgements","END"),("References","END")],
 "2108.04766v2": [("Abstract","ABS"),("Introduction","INT"),("Related work","BG"),("Methodology","MTH"),("Study findings","RES"),("Discussion","DIS"),("Limitations","CON"),("References","END")],
 "2002.08777v1": [("Abstract","ABS"),("Introduction","INT"),("Theoretical","BG"),("Data and Methodology","MTH"),("Preliminary Study","RES"),("Conclusion","CON"),("Acknowledgements","END"),("References","END")],
}
KIND = {  # reading of the abstract and method sections
 "2609.33754v2": "technical design", "2606.17839v1": "design and pattern", "2606.17831v1": "qualitative field study", "2602.11707v1": "conceptual",
 "2510.08104v1": "conceptual", "2510.00555v1": "design science", "2510.00552v1": "literature-based taxonomy", "2412.13528v1": "technical design",
 "2408.04317v1": "qualitative multi-case", "2405.01881v3": "technical design", "2310.02568v1": "technical design", "2210.02123v1": "experiment (short)",
 "2201.05945v1": "literature review", "2109.15067v1": "experiment (short)", "2108.04766v2": "qualitative think-aloud", "2002.08777v1": "experiment (short)"}
CATS = ["INT", "BG", "MTH", "RES", "DIS", "CON"]
rows = []
for pid, r in raw.items():
    cat = None; w = {c: 0 for c in CATS + ["ABS", "END"]}; rules = M[pid]
    for s in r["sections"]:
        for pre, c in rules:
            hh = s["h"].lower()
            if (hh == "abstract") if pre == "Abstract" else hh.startswith(pre.lower()): cat = c; break
        if cat in w: w[cat] += s["words"]
    body = sum(w[c] for c in CATS)
    import pymupdf as fitz
    txt = "".join(pg.get_text() for pg in fitz.open(os.path.join(ROOT, "research", "icis_refs", "pdf", pid + ".pdf")))
    tail = txt[txt.rfind("References"):] if "References" in txt else ""
    nref = len(re.findall(r"\(?(?:19|20)\d\d[a-z]?\)?[.,]", tail[:60000]))
    rows.append({"id": pid, "refs": nref, "pages": r["pages"], "kind": KIND[pid], "abs": w["ABS"], "body": body, **{c: w[c] for c in CATS}, **{c + "%": 100 * w[c] / body for c in CATS}})
print("%-13s %5s %-26s %4s %6s | %5s %5s %5s %5s %5s %5s | intro words, refs" % ("paper", "pages", "kind", "abs", "body", "INT%", "BG%", "MTH%", "RES%", "DIS%", "CON%"))
for r in sorted(rows, key=lambda x: x["pages"]):
    print("%-13s %5d %-26s %4d %6d | %5.1f %5.1f %5.1f %5.1f %5.1f %5.1f | %d, %d" % (r["id"][:12], r["pages"], r["kind"], r["abs"], r["body"], r["INT%"], r["BG%"], r["MTH%"], r["RES%"], r["DIS%"], r["CON%"], r["INT"], r["refs"]))
def med(sub, k): return st.median([x[k] for x in sub])
groups = {"all 16": rows, "short (6 to 11 pages)": [r for r in rows if r["pages"] <= 11], "full (17 to 18 pages)": [r for r in rows if r["pages"] >= 17],
          "non-technical (conceptual, qualitative, review, taxonomy)": [r for r in rows if r["kind"] in ("conceptual", "qualitative field study", "qualitative multi-case", "qualitative think-aloud", "literature review", "literature-based taxonomy")]}
print()
for g, sub in groups.items():
    print("%-58s n=%2d | median refs %3d | median abstract %3d | body words %5d | INT %4.1f%% (%4d w) BG %4.1f%% MTH %4.1f%% RES %4.1f%% DIS %4.1f%% CON %4.1f%%" % (
        g, len(sub), med(sub, "refs"), med(sub, "abs"), med(sub, "body"), med(sub, "INT%"), med(sub, "INT"), med(sub, "BG%"), med(sub, "MTH%"), med(sub, "RES%"), med(sub, "DIS%"), med(sub, "CON%")))
json.dump(rows, open(os.path.join(ROOT, "research", "icis_refs", "structure_shares.json"), "w", encoding="utf-8"), indent=1)
ours = {"INT": 364, "BG": 310 + 552, "MTH": 138 + 268 + 201, "RES": 686 + 137 + 379 + 59 + 158 + 112, "DIS": 518 + 175, "CON": 108}
tot = sum(ours.values())
print("\nmanuscript (prose and tables, without references, GenAI statement, captions): body words", tot)
print("  " + "  ".join("%s %.1f%% (%d w)" % (k, 100 * v / tot, v) for k, v in ours.items()))
