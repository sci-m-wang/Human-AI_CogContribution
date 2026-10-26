"""Analysis of the recode (run 2) of 26 October 2026 on the extended corpus, with the comparison to run 1 (frozen 146 units).
Reads archived coder outputs, writes research/coding/final_v2/*.csv and prints a summary.
Run 1 labels: gpt11, gpt11n, gemini11, gemini11n. Run 2 labels: gpt12a, gpt12b, gemini12a, gemini12b."""
import csv, glob, json, math, os, random, shutil, sys, io, statistics
from collections import Counter, defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"<project>"
CODING = os.path.join(ROOT, "research", "coding")
OUT = os.path.join(CODING, "final_v2"); ARC = os.path.join(OUT, "coder_results"); os.makedirs(ARC, exist_ok=True)
TMP = os.path.join(os.environ["TEMP"], "icis_coders")
RUN1 = {"gpt": ["gpt11", "gpt11n"], "gemini": ["gemini11", "gemini11n"]}
RUN2 = {"gpt": ["gpt12a", "gpt12b"], "gemini": ["gemini12a", "gemini12b"]}
RUN1_ARC = os.path.join(CODING, "final", "coder_results")
TYPES = ["K", "P", "D", "M", "X", "C", "Z"]; ACTORS = ["human", "AI-primary", "AI-subagent"]

for labs in RUN2.values():       # archive run 2 outputs before use
    for lab in labs:
        os.makedirs(os.path.join(ARC, lab), exist_ok=True)
        for f in glob.glob(os.path.join(TMP, lab, "result_*.jsonl")):
            shutil.copy2(f, os.path.join(ARC, lab, os.path.basename(f)))
def load(labels, root):
    r = {}; bad = 0
    for lab in labels:
        for f in sorted(glob.glob(os.path.join(root, lab, "result_*.jsonl"))):
            for line in open(f, encoding="utf-8"):
                line = line.strip()
                if not line: continue
                try: o = json.loads(line); r[o["unit_id"]] = o
                except Exception: bad += 1
    return r, bad
R1 = {c: load(RUN1[c], RUN1_ARC)[0] for c in RUN1}
R2 = {}; bad2 = 0
for c in RUN2:
    R2[c], b = load(RUN2[c], ARC); bad2 += b
units = list(csv.DictReader(open(os.path.join(CODING, "units_final.csv"), encoding="utf-8-sig")))
U = {u["unit_id"]: u for u in units}
old146 = [u["unit_id"] for u in csv.DictReader(open(os.path.join(CODING, "units_all_v1_146.csv"), encoding="utf-8-sig"))]
miss2 = {c: [u for u in U if u not in R2[c]] for c in R2}
print("units", len(U), "run2 coded gpt", len(R2["gpt"]), "gemini", len(R2["gemini"]), "missing", {c: len(v) for c, v in miss2.items()}, "bad lines", bad2)
print("run1 coded", {c: len(v) for c, v in R1.items()})

def kind(u):
    h = u["actor_hint"]; return "human" if h == "human" else ("AI-subagent" if h == "AI-subagent" else "AI-primary")
def na(a):
    a = (a or "").lower(); return "human" if a.startswith("human") else ("AI-subagent" if "sub" in a else "AI-primary")
def ty(t): return (t.get("type") or "?").strip().upper()[:1]
def tags(R, c, uid):
    k = kind(U[uid]); return [t for t in R[c].get(uid, {}).get("tags", []) if na(t.get("actor")) == k]
def prim(R, c, uid):
    ts = tags(R, c, uid); pr = [t for t in ts if t.get("primary")]; t = (pr or ts or [None])[0]
    return ty(t) if t else "-"
def present(R, c, uid): return set(ty(t) for t in tags(R, c, uid))
def agreed(R, uid, T): return T in present(R, "gpt", uid) and T in present(R, "gemini", uid)
def pr(R, c): return lambda uid: prim(R, c, uid)
def kappa(a, b):
    n = len(a); po = sum(x == y for x, y in zip(a, b)) / n; pa = sum(a) / n; pb = sum(b) / n; pe = pa * pb + (1 - pa) * (1 - pb)
    return float("nan") if pe == 1 else (po - pe) / (1 - pe)
def alpha_nominal(a, b):
    n = len(a) * 2; o = sum(1 for x, y in zip(a, b) if x != y) * 2; counts = Counter(a + b); de = 0.0
    for c1 in counts:
        for c2 in counts:
            if c1 != c2: de += counts[c1] * counts[c2]
    de = de / (n * (n - 1)); do = o / n
    return float("nan") if de == 0 else 1 - do / de
def boot(fn, a, b, B=2000, seed=1):
    rnd = random.Random(seed); n = len(a); vals = []
    for _ in range(B):
        idx = [rnd.randrange(n) for _ in range(n)]; v = fn([a[i] for i in idx], [b[i] for i in idx])
        if not math.isnan(v): vals.append(v)
    if len(vals) < 50: return (float("nan"), float("nan"))
    vals.sort(); return (vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals))])
def wcsv(name, rows):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

common = [u for u in U if u in R2["gpt"] and u in R2["gemini"]]
ids_by = {g: [u for u in common if kind(U[u]) == g] for g in ACTORS}
print("common units", len(common), {g: len(v) for g, v in ids_by.items()})

# 1 agreement between the coders in run 2 (all units) and in run 1 (146 units) for the same actor-type variables
def agreement(R, ids, fname):
    rows = []
    for ac in ACTORS:
        for T in TYPES:
            sub = [u for u in ids if kind(U[u]) == ac]
            a = [1 if T in present(R, "gpt", u) else 0 for u in ids if kind(U[u]) == ac]
            b = [1 if T in present(R, "gemini", u) else 0 for u in ids if kind(U[u]) == ac]
            if sum(a) + sum(b) == 0: continue
            # the earlier analysis (agreement.py) used every unit and an actor-type pair; keep that definition
            a = [1 if (ac, T) in {(na(t.get("actor")), ty(t)) for t in R["gpt"].get(u, {}).get("tags", [])} else 0 for u in ids]
            b = [1 if (ac, T) in {(na(t.get("actor")), ty(t)) for t in R["gemini"].get(u, {}).get("tags", [])} else 0 for u in ids]
            pa = sum(x == y for x, y in zip(a, b)) / len(a); k = kappa(a, b); al = alpha_nominal(a, b); kl, kh = boot(kappa, a, b); all_, alh = boot(alpha_nominal, a, b)
            rows.append(dict(actor=ac, type=T, n=len(a), A_present=sum(a), B_present=sum(b), both=sum(x & y for x, y in zip(a, b)), pct_agree=round(pa, 3), kappa=round(k, 3), kappa_lo=round(kl, 3), kappa_hi=round(kh, 3), alpha=round(al, 3), alpha_lo=round(all_, 3), alpha_hi=round(alh, 3)))
    wcsv(fname, rows); return rows
ag2 = agreement(R2, common, "agreement_run2_all.csv")
ids146 = [u for u in old146 if u in common]
agr1 = agreement(R1, [u for u in old146 if u in R1["gpt"] and u in R1["gemini"]], "agreement_run1_146.csv")
agr2_146 = agreement(R2, ids146, "agreement_run2_on146.csv")
prim_ag2 = sum(prim(R2, "gpt", u) == prim(R2, "gemini", u) for u in common)
prim_ag1 = sum(prim(R1, "gpt", u) == prim(R1, "gemini", u) for u in old146)
prim_ag2_146 = sum(prim(R2, "gpt", u) == prim(R2, "gemini", u) for u in old146)
print("primary-type agreement between coders: run2 all", prim_ag2, "/", len(common), "| run1 146:", prim_ag1, "| run2 on the same 146:", prim_ag2_146)
conf = Counter((prim(R2, "gpt", u), prim(R2, "gemini", u)) for u in common)
wcsv("confusion_primary_run2.csv", [dict(gpt_primary=k[0], gemini_primary=k[1], count=v) for k, v in sorted(conf.items(), key=lambda x: -x[1])])
print("top confusions run2:", [(k, v) for k, v in sorted(conf.items(), key=lambda x: -x[1]) if k[0] != k[1]][:6])
print("kappa range run2 all:", min(r["kappa"] for r in ag2), max(r["kappa"] for r in ag2), "| run1:", min(r["kappa"] for r in agr1), max(r["kappa"] for r in agr1))

# 2 test-retest: each coder, run 1 versus run 2, on the 146 frozen units
rt = []
for c in ("gpt", "gemini"):
    same_primary = sum(prim(R1, c, u) == prim(R2, c, u) for u in old146)
    same_any = sum(present(R1, c, u) == present(R2, c, u) for u in old146)
    row = dict(coder=c, units=len(old146), same_primary=same_primary, pct_primary=round(same_primary / len(old146), 3), same_type_set=same_any, pct_type_set=round(same_any / len(old146), 3))
    ks = []
    for ac in ACTORS:
        for T in "KPDM":
            a = [1 if T in present(R1, c, u) else 0 for u in old146 if kind(U[u]) == ac]; b = [1 if T in present(R2, c, u) else 0 for u in old146 if kind(U[u]) == ac]
            if sum(a) + sum(b) == 0: continue
            ks.append((ac, T, round(kappa(a, b), 2)))
    row["kappa_by_actor_type"] = ks
    rt.append(row); print("retest", c, {k: v for k, v in row.items() if k != "kappa_by_actor_type"}); print("   kappa by actor-type:", ks)
wcsv("retest.csv", [{k: (json.dumps(v) if isinstance(v, list) else v) for k, v in r.items()} for r in rt])

# 3 existence (agreed presence in run 2 on all units) and the same table for run 1, to report which headline cells changed
def existence(R, ids):
    rows = []
    for g in ACTORS:
        for T in "KPDMX":
            sel = [u for u in ids if kind(U[u]) == g]
            rows.append(dict(actor=g, type=T, units=len(sel), gpt=sum(T in present(R, "gpt", u) for u in sel), gemini=sum(T in present(R, "gemini", u) for u in sel),
                             agreed=sum(agreed(R, u, T) for u in sel), either=sum((T in present(R, "gpt", u)) or (T in present(R, "gemini", u)) for u in sel)))
    return rows
ex2 = existence(R2, common); wcsv("existence.csv", ex2)
ex1_on146 = existence(R2, ids146); ex_run1 = existence(R1, old146); wcsv("existence_run1_146.csv", ex_run1); wcsv("existence_run2_on146.csv", ex1_on146)
print("existence run2 (all units):")
for r in ex2: print("  ", r)
print("existence agreed, run1 vs run2 on the 146:", [(a["actor"], a["type"], a["agreed"], b["agreed"]) for a, b in zip(ex_run1, ex1_on146) if a["agreed"] != b["agreed"]])

# 4 stage distribution
st = Counter()
for g in ACTORS:
    for u in ids_by[g]:
        for T in "KPDM":
            if agreed(R2, u, T):
                s = [t.get("stage") for t in tags(R2, "gpt", u) if ty(t) == T and t.get("stage")]; st[(g, T, s[0] if s else "NA")] += 1
with open(os.path.join(OUT, "stage_dist.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["actor", "type", "stage", "units_agreed"])
    for k, v in sorted(st.items()): w.writerow(list(k) + [v])
tot = Counter()
for (g, T, s), v in st.items(): tot[(g, s)] += v
print("stage totals per actor:")
for g in ACTORS: print("  ", g, sum(v for (gg, s), v in tot.items() if gg == g), sorted([(s, v) for (gg, s), v in tot.items() if gg == g], key=lambda x: -x[1])[:6])

# 5 transitions within sessions on primary tags of cognitive units
bysess = defaultdict(list)
for u in sorted(units, key=lambda x: int(x["time"])): bysess[u["session"]].append(u["unit_id"])
trans = {"gpt": Counter(), "gemini": Counter()}; ex_tr = defaultdict(list)
for s, ids in bysess.items():
    for c in trans:
        seq = [(u, kind(U[u]), prim(R2, c, u)) for u in ids if prim(R2, c, u) in "KPDM" and prim(R2, c, u) != "-"]
        for a, b in zip(seq, seq[1:]):
            key = (("H" if a[1] == "human" else "AI") + ":" + a[2], ("H" if b[1] == "human" else "AI") + ":" + b[2]); trans[c][key] += 1; ex_tr[(c, key)].append((a[0], b[0]))
keys = sorted(set(trans["gpt"]) | set(trans["gemini"]), key=lambda k: -(trans["gpt"][k] + trans["gemini"][k]))
with open(os.path.join(OUT, "transitions.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["from", "to", "gpt", "gemini", "example_gpt"])
    for k in keys: w.writerow([k[0], k[1], trans["gpt"][k], trans["gemini"][k], "; ".join("%s>%s" % e for e in ex_tr.get(("gpt", k), [])[:3])])
print("transitions gpt", sum(trans["gpt"].values()), "gemini", sum(trans["gemini"].values()))
for k in keys[:14]: print("  ", k, trans["gpt"][k], trans["gemini"][k])
