import csv, collections, os
base = r"records/logs"
for n, col in (("interventions", "intervention_id"), ("events", None), ("verification", "verification_id"), ("artifacts", None)):
    p = os.path.join(base, n + ".csv")
    rows = list(csv.reader(open(p, encoding="utf-8-sig")))
    hdr = rows[0]
    ids = [r[0] for r in rows[1:] if r]
    dup = [k for k, v in collections.Counter(ids).items() if v > 1]
    print(n, "header:", hdr[:4], "rows:", len(ids), "last5:", ids[-5:], "dups:", dup)
    for r in rows[-2:]:
        print("   ", r[0], r[1], (r[7] if len(r) > 7 else "")[:110].replace("\n", " "))
