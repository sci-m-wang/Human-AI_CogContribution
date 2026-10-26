import sys, urllib.request, io, os, re
try:
    import pypdf
except ImportError:
    print("NO_PYPDF"); sys.exit(1)
def get(url, ua="Mozilla/5.0 (research fetch)"):
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept": "application/pdf,*/*"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()
def pdf_text(b):
    rd = pypdf.PdfReader(io.BytesIO(b))
    out = []
    for i, p in enumerate(rd.pages, 1):
        out.append(f"\n[[PAGE {i}]]\n" + (p.extract_text() or ""))
    return "".join(out), len(rd.pages)
if __name__ == "__main__":
    url, outp = sys.argv[1], sys.argv[2]
    try:
        b = get(url)
    except Exception as e:
        print("FETCH_FAIL", e); sys.exit(2)
    print("bytes", len(b), "head", b[:8])
    if not b.startswith(b"%PDF"):
        print("NOT_PDF"); sys.exit(3)
    t, n = pdf_text(b)
    os.makedirs(os.path.dirname(outp), exist_ok=True)
    open(outp, "w", encoding="utf-8").write(t)
    print("pages", n, "chars", len(t))
