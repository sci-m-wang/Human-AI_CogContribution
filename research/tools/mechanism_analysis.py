"""Structural statistics behind the explanation section (delegation runs, fate of AI proposals).
Reads the archived coder results and units_all.csv, writes research/coding/final/mechanism_*.csv and prints a summary.
Coder results were archived from %TEMP%\\icis_coders into research/coding/final/coder_results/ (copy step below)."""
import csv, glob, json, os, shutil, statistics, sys, io
from collections import Counter, defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"<project>"
FIN = os.path.join(ROOT, "research", "coding", "final")
ARC = os.path.join(FIN, "coder_results")
TMP = os.path.join(os.environ["TEMP"], "icis_coders")
if not os.path.isdir(ARC):
    for lab in ("gpt11", "gpt11n", "gemini11", "gemini11n"):
        os.makedirs(os.path.join(ARC, lab), exist_ok=True)
        for f in glob.glob(os.path.join(TMP, lab, "result_*.jsonl")):
            shutil.copy2(f, os.path.join(ARC, lab, os.path.basename(f)))
def load(labels):
    r = {}
    for lab in labels:
        for f in sorted(glob.glob(os.path.join(ARC, lab, "result_*.jsonl"))):
            for line in open(f, encoding="utf-8"):
                line = line.strip()
                if line:
                    o = json.loads(line); r[o["unit_id"]] = o
    return r
C = {"gpt": load(["gpt11", "gpt11n"]), "gemini": load(["gemini11", "gemini11n"])}
units = list(csv.DictReader(open(os.path.join(ROOT, "research", "coding", "units_all.csv"), encoding="utf-8-sig")))
U = {u["unit_id"]: u for u in units}
def kind(u):
    h = u["actor_hint"]
    return "human" if h == "human" else ("AI-subagent" if h == "AI-subagent" else "AI-primary")
def na(a):
    a = (a or "").lower(); return "human" if a.startswith("human") else ("AI-subagent" if "sub" in a else "AI-primary")
def tags(cod, uid):
    k = kind(U[uid]); return [t for t in C[cod].get(uid, {}).get("tags", []) if na(t.get("actor")) == k]
def ty(t): return (t.get("type") or "?")[:1].upper()
def prim(cod, uid):
    ts = tags(cod, uid); pr = [t for t in ts if t.get("primary")]; t = (pr or ts or [None])[0]
    return ty(t) if t else "-"
def present(cod, uid): return set(ty(t) for t in tags(cod, uid))
def agreed(uid, T): return T in present("gpt", uid) and T in present("gemini", uid)

bysess = defaultdict(list)
for u in sorted(units, key=lambda x: int(x["time"])): bysess[u["session"]].append(u["unit_id"])

# 1 delegation episodes: a human unit and the AI-primary units that follow until the next human unit
ep = []
for s, ids in bysess.items():
    ids = [i for i in ids if kind(U[i]) != "AI-subagent"]
    hum = [k for k, i in enumerate(ids) if kind(U[i]) == "human"]
    for n, k in enumerate(hum):
        end = hum[n + 1] if n + 1 < len(hum) else len(ids)
        run = ids[k + 1:end]
        nxt = ids[end] if end < len(ids) else ""
        ep.append(dict(session=s, human_unit=ids[k], gpt=prim("gpt", ids[k]), gemini=prim("gemini", ids[k]),
                       run_len=len(run), run_cognitive=sum(1 for i in run if prim("gpt", i) in "KPDM" and prim("gpt", i) != "-"),
                       run_types_gpt="".join(prim("gpt", i) for i in run), run_types_gemini="".join(prim("gemini", i) for i in run),
                       first_unit=run[0] if run else "", last_unit=run[-1] if run else "",
                       next_human=nxt, next_gpt=prim("gpt", nxt) if nxt else "", next_gemini=prim("gemini", nxt) if nxt else "",
                       ends_session=int(end >= len(ids))))
with open(os.path.join(FIN, "mechanism_episodes.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(ep[0].keys())); w.writeheader(); w.writerows(ep)
inner = [e for e in ep if not e["ends_session"] or e["run_len"] > 0]
rl = [e["run_len"] for e in ep]
print("episodes", len(ep), "run lengths", sorted(rl))
print("median run", statistics.median(rl), "mean", round(statistics.mean(rl), 2), "n>=5", sum(r >= 5 for r in rl), "n>=10", sum(r >= 10 for r in rl))
tot_ai = sum(rl); print("AI-primary units in episodes", tot_ai, "in runs >=5:", sum(r for r in rl if r >= 5))
for e in sorted(ep, key=lambda e: -e["run_len"])[:6]:
    print(" ", e["human_unit"], "H", e["gpt"] + "/" + e["gemini"], "run", e["run_len"], e["first_unit"], "-", e["last_unit"], "next", e["next_human"], e["next_gpt"] + "/" + e["next_gemini"], "types", e["run_types_gpt"])
# by human primary type (agreed primary only)
byT = defaultdict(list)
for e in ep:
    if e["gpt"] == e["gemini"]: byT[e["gpt"]].append(e["run_len"])
print("run length by agreed human primary type", {k: (len(v), statistics.median(v), max(v)) for k, v in byT.items()})

# 2 fate of AI proposals: AI-primary units with Proposal agreed by both coders -> next human unit in the same session
fate = []
for s, ids in bysess.items():
    ids = [i for i in ids if kind(U[i]) != "AI-subagent"]
    for k, i in enumerate(ids):
        if kind(U[i]) == "AI-primary" and agreed(i, "P"):
            nxt = next((j for j in ids[k + 1:] if kind(U[j]) == "human"), "")
            fate.append(dict(proposal=i, next_human=nxt, gpt=prim("gpt", nxt) if nxt else "none", gemini=prim("gemini", nxt) if nxt else "none",
                             gpt_has_D=int(bool(nxt) and "D" in present("gpt", nxt)), gemini_has_D=int(bool(nxt) and "D" in present("gemini", nxt)),
                             gpt_has_P=int(bool(nxt) and "P" in present("gpt", nxt)), gemini_has_P=int(bool(nxt) and "P" in present("gemini", nxt)),
                             gpt_has_M=int(bool(nxt) and "M" in present("gpt", nxt)), gemini_has_M=int(bool(nxt) and "M" in present("gemini", nxt))))
with open(os.path.join(FIN, "mechanism_proposal_fate.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(fate[0].keys())); w.writeheader(); w.writerows(fate)
print("\nAI proposals (agreed P, primary agent):", len(fate))
for c in ("gpt", "gemini"):
    n_h = [x for x in fate if x["next_human"]]
    print(" ", c, "next human unit exists", len(n_h), "| primary", Counter(x[c] for x in fate), "| D present", sum(x[c + "_has_D"] for x in fate), "| P present", sum(x[c + "_has_P"] for x in fate), "| M present", sum(x[c + "_has_M"] for x in fate))
print(" ", [(x["proposal"], x["next_human"], x["gpt"], x["gemini"]) for x in fate])

# 3 who holds Decision: human Decision units vs AI Decision units agreed
for g in ("human", "AI-primary", "AI-subagent"):
    ids = [i for i in U if kind(U[i]) == g]
    print("\nDecision agreed", g, sum(agreed(i, "D") for i in ids), "of", len(ids), "| autonomous flag in either coder:",
          sum(1 for i in ids for c in C for t in tags(c, i) if ty(t) == "D" and t.get("autonomous")))
# 4 human K or P units: the preceding AI-primary unit and whether it carried K (agreed)
prevK = []
for s, ids in bysess.items():
    ids = [i for i in ids if kind(U[i]) != "AI-subagent"]
    for k, i in enumerate(ids):
        if kind(U[i]) == "human" and (agreed(i, "K") or agreed(i, "P")):
            pv = next((j for j in reversed(ids[:k]) if kind(U[j]) != "human"), "")
            prevK.append((i, "".join(sorted(present("gpt", i) & present("gemini", i))), pv, "".join(sorted(present("gpt", pv) & present("gemini", pv))) if pv else ""))
print("\nhuman units with agreed K or P and the preceding AI unit (agreed types):")
for x in prevK: print("  ", x)

# 5 composition of the long runs (>= 5 AI units) by primary tag and presence of any tag
long_eps = [e for e in ep if e["run_len"] >= 5]
for c in ("gpt", "gemini"):
    comp = Counter(); pres = Counter()
    for e in long_eps:
        a = int(e["first_unit"].split("-U")[1]); b = int(e["last_unit"].split("-U")[1]); sess = e["first_unit"].split("-")[0]
        for n in range(a, b + 1):
            uid = "%s-U%03d" % (sess, n)
            if uid in U and kind(U[uid]) != "AI-subagent":
                comp[prim(c, uid)] += 1
                for T in present(c, uid): pres[T] += 1
    print("\nlong runs", c, "primary composition", dict(comp), "total", sum(comp.values()), "| units with tag present", dict(pres))
print("long runs", [(e["human_unit"], e["run_len"]) for e in long_eps])
# 6 human Proposal units and the unit before them
for i in [u for u in U if kind(U[u]) == "human" and agreed(u, "P")]:
    s = U[i]["session"]; ids = [j for j in bysess[s] if kind(U[j]) != "AI-subagent"]; k = ids.index(i)
    pv = ids[k - 1] if k > 0 else ""
    print("human P", i, "prev", pv, "prev types gpt", "".join(sorted(present("gpt", pv))) if pv else "", "gemini", "".join(sorted(present("gemini", pv))) if pv else "")
