"""Measure the section structure of ICIS papers whose author versions are on arXiv.

Usage: python icis_structure.py
Downloads the PDFs to research/icis_refs/pdf (not for redistribution), detects headings by font, counts words per section,
writes research/icis_refs/structure_raw.json and prints a table plus the heading list of every paper for manual checking.
"""
import json, os, re, sys, time, urllib.request, collections
import pymupdf as fitz
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = os.path.join(ROOT, "research", "icis_refs"); os.makedirs(os.path.join(D, "pdf"), exist_ok=True)
IDS = ["2609.33754v2", "2606.17839v1", "2606.17831v1", "2602.11707v1", "2510.08104v1", "2510.00555v1", "2510.00552v1", "2412.13528v1",
       "2408.04317v1", "2405.01881v3", "2310.02568v1", "2210.02123v1", "2201.05945v1", "2109.15067v1", "2108.04766v2", "2002.08777v1"]

def fetch(i):
    p = os.path.join(D, "pdf", i + ".pdf")
    if os.path.exists(p) and os.path.getsize(p) > 20000: return p
    for k in range(3):
        try:
            r = urllib.request.urlopen(urllib.request.Request("https://arxiv.org/pdf/" + i, headers={"User-Agent": "icis-pdw-research/1.0"}), timeout=60)
            open(p, "wb").write(r.read()); time.sleep(3); return p
        except Exception as e:
            print("retry", i, e); time.sleep(5)
    return None

def lines_of(doc):
    sizes = collections.Counter(); L = []
    for pn, pg in enumerate(doc):
        for b in pg.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                spans = [s for s in ln["spans"] if s["text"].strip()]
                if not spans: continue
                t = "".join(s["text"] for s in spans).strip()
                size = max(s["size"] for s in spans)
                bold = all(("bold" in s["font"].lower() or "black" in s["font"].lower() or (s["flags"] & 16)) for s in spans)
                for s in spans: sizes[round(s["size"], 1)] += len(s["text"])
                L.append({"p": pn + 1, "t": t, "size": size, "bold": bold, "y": ln["bbox"][1]})
    body = sizes.most_common(1)[0][0]
    return L, body

SEC = re.compile(r"^(\d+(\.\d+)*\.?|[IVX]+\.)?\s*(abstract|introduction|background|related work|related literature|literature review|theoretical|theory|conceptual|research (design|method|model|question)|method|methodology|data|case|findings|results|analysis|discussion|implications|conclusion|limitations|future|references|appendix|acknowledg)", re.I)

def analyse(pdf):
    doc = fitz.open(pdf); L, body = lines_of(doc)
    heads = []
    for i, l in enumerate(L):
        t = l["t"]
        if len(t.split()) > 14 or len(t) < 3 or re.match(r"^(figure|table|fig\.)\s*\d", t, re.I): continue
        big = l["size"] >= body + 0.9
        numbered = bool(re.match(r"^\d+(\.\d+)*\.?\s+[A-Z]", t))
        if (l["bold"] and (numbered or SEC.match(t) or big)) or (big and (numbered or SEC.match(t))):
            heads.append(i)
    # merge consecutive heading lines that belong together
    sections = []
    for k, i in enumerate(heads):
        j = heads[k + 1] if k + 1 < len(heads) else len(L)
        txt = " ".join(x["t"] for x in L[i + 1:j])
        sections.append({"h": L[i]["t"], "p": L[i]["p"], "words": len(txt.split())})
    return {"pages": len(doc), "body_font": body, "sections": sections, "words_all": sum(len(l["t"].split()) for l in L)}

res = {}
for i in IDS:
    p = fetch(i)
    if not p: print("FAILED", i); continue
    try: res[i] = analyse(p)
    except Exception as e: print("ERR", i, e)
json.dump(res, open(os.path.join(D, "structure_raw.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
for i, r in res.items():
    print("\n=== %s pages=%d body_font=%.1f words_all=%d" % (i, r["pages"], r["body_font"], r["words_all"]))
    for s in r["sections"][:40]:
        print("   p%-2d %-70s %5d" % (s["p"], s["h"][:70], s["words"]))
