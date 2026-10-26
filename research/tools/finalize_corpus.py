"""Post-coding exclusion of harness-generated context summaries that the first filter (rule R3) missed.
Reads units_ext.csv (the corpus the coders saw), writes units_final.csv and exclusions_post_coding.csv. The coders' outputs for the
excluded units stay in the archive and are not used by any table."""
import csv, io, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
R = r"research/coding/"
rows = list(csv.DictReader(open(R + "units_ext.csv", encoding="utf-8-sig")))
oldids = {u["unit_id"] for u in csv.DictReader(open(R + "units_all_v1_146.csv", encoding="utf-8-sig"))}
pat = re.compile(r"^\s*##\s*Objective|##\s*Important Details|##\s*Work State|##\s*Next Move|##\s*Relevant Files")
cand = []
for u in rows:
    t = u["text"]
    hits = len(pat.findall(t)) if u["actor_hint"].startswith("AI-primary") else 0
    if hits >= 2: cand.append(u["unit_id"])
print("candidates (>=2 summary headings):", cand)
for u in rows:
    if u["unit_id"] in cand: print(u["unit_id"], u["actor_hint"], len(u["text"]), "frozen146" if u["unit_id"] in oldids else "new", "|", u["text"][:80].replace("\n", " "))
assert not any(i in oldids for i in cand), "a frozen unit would be removed"
keep = [u for u in rows if u["unit_id"] not in cand]
with open(R + "units_final.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(keep)
with open(R + "exclusions_post_coding.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["unit_id", "rule", "note"])
    for i in cand: w.writerow([i, "R3b context-compaction summary missed by R3", "found after coding, outputs archived and not used"])
print("units_final", len(keep), "of", len(rows))
