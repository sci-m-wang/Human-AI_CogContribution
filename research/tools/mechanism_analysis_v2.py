"""Mechanism analysis (delegation episodes, fate of AI proposals, report-and-commit transitions) on the extended corpus
with the codes of run 2 (26 October 2026). Writes research/coding/final_v2/mechanism_*.csv and prints a summary."""
import csv, glob, json, os, statistics, sys, io
from collections import Counter, defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"<project>"
CODING = os.path.join(ROOT, "research", "coding"); OUT = os.path.join(CODING, "final_v2"); ARC = os.path.join(OUT, "coder_results")
def load(labels):
    r = {}
    for lab in labels:
        for f in sorted(glob.glob(os.path.join(ARC, lab, "result_*.jsonl"))):
            for line in open(f, encoding="utf-8"):
                line = line.strip()
                if line: o = json.loads(line); r[o["unit_id"]] = o
    return r
C = {"gpt": load(["gpt12a", "gpt12b"]), "gemini": load(["gemini12a", "gemini12b"])}
units = list(csv.DictReader(open(os.path.join(CODING, "units_final.csv"), encoding="utf-8-sig")))
U = {u["unit_id"]: u for u in units}
def kind(u):
    h = u["actor_hint"]; return "human" if h == "human" else ("AI-subagent" if h == "AI-subagent" else "AI-primary")
def na(a):
    a = (a or "").lower(); return "human" if a.startswith("human") else ("AI-subagent" if "sub" in a else "AI-primary")
def tags(c, uid):
    k = kind(U[uid]); return [t for t in C[c].get(uid, {}).get("tags", []) if na(t.get("actor")) == k]
def ty(t): return (t.get("type") or "?").strip().upper()[:1]
def prim(c, uid):
    ts = tags(c, uid); pr = [t for t in ts if t.get("primary")]; t = (pr or ts or [None])[0]; return ty(t) if t else "-"
def present(c, uid): return set(ty(t) for t in tags(c, uid))
def agreed(uid, T): return T in present("gpt", uid) and T in present("gemini", uid)
bysess = defaultdict(list)
for u in sorted(units, key=lambda x: int(x["time"])): bysess[u["session"]].append(u["unit_id"])
def wcsv(name, rows):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

# 1 delegation episodes
ep = []
for s, ids in bysess.items():
    ids = [i for i in ids if kind(U[i]) != "AI-subagent"]
    hum = [k for k, i in enumerate(ids) if kind(U[i]) == "human"]
    for n, k in enumerate(hum):
        end = hum[n + 1] if n + 1 < len(hum) else len(ids)
        run = ids[k + 1:end]; nxt = ids[end] if end < len(ids) else ""
        ep.append(dict(session=s, human_unit=ids[k], gpt=prim("gpt", ids[k]), gemini=prim("gemini", ids[k]), run_len=len(run),
                       run_types_gpt="".join(prim("gpt", i) for i in run), run_types_gemini="".join(prim("gemini", i) for i in run),
                       first_unit=run[0] if run else "", last_unit=run[-1] if run else "",
                       next_human=nxt, next_gpt=prim("gpt", nxt) if nxt else "", next_gemini=prim("gemini", nxt) if nxt else "",
                       ends_session=int(end >= len(ids))))
wcsv("mechanism_episodes.csv", ep)
rl = sorted(e["run_len"] for e in ep)
print("episodes", len(ep), "AI-primary responses inside episodes", sum(rl), "| by session", dict(Counter(e["session"] for e in ep)))
print("run lengths", rl)
print("median", statistics.median(rl), "mean", round(statistics.mean(rl), 2), "n>=5", sum(r >= 5 for r in rl), "n>=10", sum(r >= 10 for r in rl))
LONGMIN = 5
long_eps = [e for e in ep if e["run_len"] >= LONGMIN]
print("long runs (>=%d):" % LONGMIN, len(long_eps), "holding", sum(e["run_len"] for e in long_eps), "of", sum(rl))
for e in sorted(long_eps, key=lambda e: -e["run_len"]):
    print("  ", e["session"], e["human_unit"], "H", e["gpt"] + "/" + e["gemini"], "run", e["run_len"], e["first_unit"], "-", e["last_unit"], "next", e["next_human"], e["next_gpt"] + "/" + e["next_gemini"], "ends_session", e["ends_session"])
for c in ("gpt", "gemini"):
    comp = Counter(); 
    for e in long_eps:
        s = e["session"]; a = int(e["first_unit"].split("-U")[1]); b = int(e["last_unit"].split("-U")[1])
        for n in range(a, b + 1):
            uid = "%s-U%03d" % (s, n)
            if uid in U and kind(U[uid]) != "AI-subagent": comp[prim(c, uid)] += 1
    tot = sum(comp.values()); xm = comp["X"] + comp["M"]
    print(c, "long-run composition", dict(comp), "total", tot, "X or M", xm)
# 2 how episodes end: the next human unit after a run, by tags
nxt_rows = [e for e in ep if e["next_human"]]
print("episodes followed by a human unit", len(nxt_rows))
for c in ("gpt", "gemini"):
    print(c, "next-human primary", dict(Counter(e["next_" + c] for e in nxt_rows)))
# 3 fate of AI proposals
fate = []
for s, ids in bysess.items():
    ids = [i for i in ids if kind(U[i]) != "AI-subagent"]
    for k, i in enumerate(ids):
        if kind(U[i]) == "AI-primary" and agreed(i, "P"):
            nxt = next((j for j in ids[k + 1:] if kind(U[j]) == "human"), "")
            row = dict(proposal=i, next_human=nxt)
            for c in ("gpt", "gemini"):
                row[c] = prim(c, nxt) if nxt else "none"
                for T in "DPM": row["%s_has_%s" % (c, T)] = int(bool(nxt) and T in present(c, nxt))
            fate.append(row)
wcsv("mechanism_proposal_fate.csv", fate)
print("AI proposals (agreed P, primary agent):", len(fate), "| with a later human unit", sum(1 for x in fate if x["next_human"]))
for c in ("gpt", "gemini"):
    print(" ", c, "primary", dict(Counter(x[c] for x in fate)), "D present", sum(x[c + "_has_D"] for x in fate), "P present", sum(x[c + "_has_P"] for x in fate), "M present", sum(x[c + "_has_M"] for x in fate))
print("  ", [(x["proposal"], x["next_human"], x["gpt"], x["gemini"]) for x in fate])
# 4 decisions
for g in ("human", "AI-primary", "AI-subagent"):
    ids = [i for i in U if kind(U[i]) == g]
    print("Decision agreed", g, sum(agreed(i, "D") for i in ids), "of", len(ids), "| either coder", sum(("D" in present("gpt", i)) or ("D" in present("gemini", i)) for i in ids))
print("AI-primary agreed Decision units:", [i for i in U if kind(U[i]) == "AI-primary" and agreed(i, "D")])
print("human units agreed without D:", [i for i in U if kind(U[i]) == "human" and not agreed(i, "D")])
# 5 human K or P units and the unit before
print("human units with agreed K or P and the preceding AI unit (agreed types):")
for s, ids in bysess.items():
    ids = [i for i in ids if kind(U[i]) != "AI-subagent"]
    for k, i in enumerate(ids):
        if kind(U[i]) == "human" and (agreed(i, "K") or agreed(i, "P")):
            pv = next((j for j in reversed(ids[:k]) if kind(U[j]) != "human"), "")
            print("  ", i, "".join(sorted(present("gpt", i) & present("gemini", i))), "<-", pv, "".join(sorted(present("gpt", pv) & present("gemini", pv))) if pv else "")
print("human units with agreed P:", [i for i in U if kind(U[i]) == "human" and agreed(i, "P")])
# 6 report and commit: AI:M then H:D transitions (primary tags, within session)
rep = {"gpt": [], "gemini": []}
for s, ids in bysess.items():
    for c in rep:
        seq = [(u, kind(U[u]), prim(c, u)) for u in ids if prim(c, u) in "KPDM" and prim(c, u) != "-"]
        for a, b in zip(seq, seq[1:]):
            if a[1] == "AI-primary" and a[2] == "M" and b[1] == "human" and b[2] == "D": rep[c].append((a[0], b[0]))
print("AI:M -> H:D transitions", {c: len(v) for c, v in rep.items()}, rep["gpt"][:6])
