"""All numbers that the manuscript states about the coded corpus, computed from the run 2 outputs (final_v2) and checked.
Imported by paper/build_paper.py and paper/build_appendix.py. Run directly to print a report."""
import csv, glob, json, os, statistics, sys, io
from collections import Counter, defaultdict
ROOT = r"<project>"
CODING = os.path.join(ROOT, "research", "coding"); V2 = os.path.join(CODING, "final_v2"); V1 = os.path.join(CODING, "final")
def rd(path): return list(csv.DictReader(open(path, encoding="utf-8")))
units = list(csv.DictReader(open(os.path.join(CODING, "units_final.csv"), encoding="utf-8-sig")))
U = {u["unit_id"]: u for u in units}
def kind(u):
    h = u["actor_hint"]; return "human" if h == "human" else ("AI-subagent" if h == "AI-subagent" else "AI-primary")
def load(labels):
    r = {}
    for lab in labels:
        for f in sorted(glob.glob(os.path.join(V2, "coder_results", lab, "result_*.jsonl"))):
            for line in open(f, encoding="utf-8"):
                line = line.strip()
                if line: o = json.loads(line); r[o["unit_id"]] = o
    return r
C = {"gpt": load(["gpt12a", "gpt12b"]), "gemini": load(["gemini12a", "gemini12b"])}
def na(a):
    a = (a or "").lower(); return "human" if a.startswith("human") else ("AI-subagent" if "sub" in a else "AI-primary")
def ty(t): return (t.get("type") or "?").strip().upper()[:1]
def tags(c, uid):
    k = kind(U[uid]); return [t for t in C[c].get(uid, {}).get("tags", []) if na(t.get("actor")) == k]
def prim(c, uid):
    ts = tags(c, uid); pr = [t for t in ts if t.get("primary")]; t = (pr or ts or [None])[0]; return ty(t) if t else "-"
def present(c, uid): return set(ty(t) for t in tags(c, uid))
def agreed(uid, T): return T in present("gpt", uid) and T in present("gemini", uid)

# corpus
N_UNITS = len(units)
N_BY = Counter(kind(u) for u in units)
N_PROMPT = sum(u["actor_hint"].startswith("AI-primary (prompt") for u in units)
N_SESSIONS = len({u["session"] for u in units})
N_PRIMARY_RESP = N_BY["AI-primary"] - N_PROMPT
N_NEW = N_UNITS - 146

# existence
ex = rd(os.path.join(V2, "existence.csv"))
def E(actor, t): return [r for r in ex if r["actor"] == actor and r["type"] == t][0]
def A(actor, t): return int(E(actor, t)["agreed"])
def pct(actor, t): return int(100 * A(actor, t) / int(E(actor, t)["units"]) + 0.5)
def cell(actor, t):
    r = E(actor, t); n = int(r["units"]); a = int(r["agreed"])
    return "%d (%d%%) [%s/%s]" % (a, int(100 * a / n + 0.5), r["gpt"], r["gemini"])
n_h, n_p, n_s = int(E("human", "K")["units"]), int(E("AI-primary", "K")["units"]), int(E("AI-subagent", "K")["units"])
T1 = [["Actor (units)", "Knowledge", "Proposal", "Decision", "Metacognition", "Execution"]]
for lab, a in [("Human (%d)" % n_h, "human"), ("Primary agent (%d)" % n_p, "AI-primary"), ("Sub-agents (%d)" % n_s, "AI-subagent")]:
    T1.append([lab] + [cell(a, t) for t in "KPDMX"])
# agreement
def f2(x): return ("%.2f" % float(x)).replace("0.", ".", 1) if abs(float(x)) < 1 else "%.2f" % float(x)
agr = rd(os.path.join(V2, "agreement_run2_all.csv")); agr1 = rd(os.path.join(V2, "agreement_run1_146.csv")); agr_146 = rd(os.path.join(V2, "agreement_run2_on146.csv"))
names = {"human": "Human", "AI-primary": "Primary agent", "AI-subagent": "Sub-agents"}
tn = {"K": "Knowledge", "P": "Proposal", "D": "Decision", "M": "Metacognition", "X": "Execution", "C": "Coordination"}
def ag_row(r): return [r["actor"], r["type"], r["A_present"], r["B_present"], int(float(r["pct_agree"]) * 100 + 0.5), float(r["kappa"]), float(r["alpha"]), r]
AGMAIN = [r for r in agr if r["type"] in "KPDMX"]
T3 = [["Actor and type", "GPT / Gemini", "Agree %", "Kappa [95% CI]", "Alpha [95% CI]"]]
for r in AGMAIN:
    T3.append(["%s, %s" % (names[r["actor"]], tn[r["type"]]), "%s / %s" % (r["A_present"], r["B_present"]), str(int(float(r["pct_agree"]) * 100 + 0.5)),
               "%s [%s, %s]" % (f2(r["kappa"]), f2(r["kappa_lo"]), f2(r["kappa_hi"])), "%s [%s, %s]" % (f2(r["alpha"]), f2(r["alpha_lo"]), f2(r["alpha_hi"]))])
def kap(actor, t, rows=None):
    return [float(r["kappa"]) for r in (rows or agr) if r["actor"] == actor and r["type"] == t][0]
# run 1 versus run 2 on the same 146 units
K1 = {(r["actor"], r["type"]): float(r["kappa"]) for r in agr1}; K2 = {(r["actor"], r["type"]): float(r["kappa"]) for r in agr_146}
common_pairs = sorted(set(K1) & set(K2) - {("human", "C")})
retest = {r["coder"]: r for r in rd(os.path.join(V2, "retest.csv"))}
RT = {c: (int(100 * int(r["same_primary"]) / int(r["units"]) + 0.5), int(100 * int(r["same_type_set"]) / int(r["units"]) + 0.5)) for c, r in retest.items()}
old146 = [u["unit_id"] for u in csv.DictReader(open(os.path.join(CODING, "units_all_v1_146.csv"), encoding="utf-8-sig"))]
PRIM_ALL = sum(prim("gpt", u) == prim("gemini", u) for u in U)
PRIM_146_R2 = sum(prim("gpt", u) == prim("gemini", u) for u in old146)
# run 1 primary agreement is stored in the earlier analysis (112 of 146)
PRIM_146_R1 = 112
conf = Counter((prim("gpt", u), prim("gemini", u)) for u in U)
# transitions
tr = rd(os.path.join(V2, "transitions.csv"))
def TR(a, b):
    r = [x for x in tr if x["from"] == a and x["to"] == b]; return (int(r[0]["gpt"]), int(r[0]["gemini"])) if r else (0, 0)
def add(*pairs): return (sum(p[0] for p in pairs), sum(p[1] for p in pairs))
MODES = {1: TR("H:D", "AI:P"), 2: TR("AI:P", "H:D"), 3: TR("AI:K", "H:D"), 4: add(TR("H:D", "AI:M"), TR("H:M", "AI:M")), 5: TR("AI:P", "H:M"), 6: add(TR("AI:M", "AI:M"), TR("AI:M", "AI:K"))}
REPORT_COMMIT = TR("AI:M", "H:D")
TRANS_TOTAL = (sum(int(x["gpt"]) for x in tr), sum(int(x["gemini"]) for x in tr))
# stage
st = rd(os.path.join(V2, "stage_dist.csv"))
def stage_tot(actor):
    c = Counter()
    for r in st:
        if r["actor"] == actor: c[r["stage"]] += int(r["units_agreed"])
    return sum(c.values()), c
# mechanism
EP = rd(os.path.join(V2, "mechanism_episodes.csv")); FATE = rd(os.path.join(V2, "mechanism_proposal_fate.csv"))
RL = sorted(int(e["run_len"]) for e in EP); LONG = [e for e in EP if int(e["run_len"]) >= 5]
N_EP = len(EP); N_LONG = len(LONG); LONG_UNITS = sum(int(e["run_len"]) for e in LONG); EP_UNITS = sum(RL); MEDIAN_RUN = statistics.median(RL)
def long_xm(c):
    n = 0; tot = 0
    for e in LONG:
        s = e["session"]; a = int(e["first_unit"].split("-U")[1]); b = int(e["last_unit"].split("-U")[1])
        for k in range(a, b + 1):
            uid = "%s-U%03d" % (s, k)
            if uid in U and kind(U[uid]) != "AI-subagent":
                tot += 1; n += prim(c, uid) in ("X", "M")
    return n, tot
LONG_XM = {c: long_xm(c) for c in ("gpt", "gemini")}
FATE_LATER = [x for x in FATE if x["next_human"]]
FATE_D = {c: sum(int(x[c + "_has_D"]) for x in FATE_LATER) for c in ("gpt", "gemini")}
NEXT_AFTER_RUN = {c: Counter(e["next_" + c] for e in EP if e["next_human"]) for c in ("gpt", "gemini")}
N_EP_NEXT = sum(1 for e in EP if e["next_human"])
AI_D_UNITS = [i for i in U if kind(U[i]) == "AI-primary" and agreed(i, "D")]
HUM_NO_D = [i for i in U if kind(U[i]) == "human" and not agreed(i, "D")]
# exemplar and coded excerpt tables
def tagstr(c, uid):
    ts = tags(c, uid); p = prim(c, uid); others = sorted({ty(t) for t in ts if ty(t) != p})
    return p + (" (%s)" % ", ".join(others) if others else "")
EXCERPT = [("S01-U031", "Primary agent", "Reports 25 sources read in full and that sub-agent notes were not all re-checked."),
           ("S01-U032", "Human", "Argues that agents now give experts new knowledge, so knowledge should count as a contribution."),
           ("S01-U033", "Primary agent", "Announces that it will log the instruction and write the framework to file."),
           ("S01-U034", "Primary agent", "Delivers framework and codebook v0.1 with knowledge as a type and four primary types."),
           ("S01-U035", "Human", "Accepts that evaluation and choice are hard to separate and sets the coding unit to one round.")]
T_COD = [["Unit", "Actor", "Content (abridged)", "Coder A", "Coder B"]] + [[u, a, t, tagstr("gpt", u), tagstr("gemini", u)] for u, a, t in EXCERPT]
EXEMPLARS = [("human", "K", "S01-U005", "Execution carries little cognition because it follows a prepared blueprint"),
             ("human", "P", "S01-U014", "A split of cognitive contribution into decision, knowledge and expression or design"),
             ("human", "D", "S01-U005", "Only the project\u2019s own sessions serve as data"),
             ("human", "M", "S01-U017", "Survey the related research before designing the scheme"),
             ("AI-primary", "K", "S01-U004", "Reading of the call for papers, including the page limit"),
             ("AI-primary", "P", "S01-U066", "A process model linking Knowledge, Proposal, Decision and Metacognition"),
             ("AI-primary", "D", "S03-U001", "Assignment of a literature survey on forms of cognition to a sub-agent under the project rules"),
             ("AI-primary", "M", "S01-U031", "Report that only abstracts could be read for 12 sources"),
             ("AI-primary", "X", "S01-U051", "Launching both coders as instructed"),
             ("AI-subagent", "K", "S06-U005", "Reading note that a revised taxonomy is a two-dimensional table"),
             ("AI-subagent", "M", "S08-U003", "Statement that only the main text of one source was read in full")]
BAD_EXEMPLARS = [(a, t, u) for a, t, u, _ in EXEMPLARS if not (kind(U[u]) == a and agreed(u, t))]
T_EX = [["Actor", "Type", "Exemplar unit"]] + [[names[a] if a != "AI-primary" else "Primary agent", tn[t], "%s (%s)" % (d, u)] for a, t, u, d in EXEMPLARS]
_order = {"human": 0, "AI-primary": 1, "AI-subagent": 2}
T_RUNS = [["Actor and type", "Kappa run 1", "Kappa run 2", "Change"]]
for k in sorted(common_pairs, key=lambda k: (_order[k[0]], "KPDMX".index(k[1]))):
    d = K2[k] - K1[k]
    T_RUNS.append(["%s, %s" % (names[k[0]], tn[k[1]]), f2(K1[k]), f2(K2[k]), ("+" if d > 0.005 else "") + ("%.2f" % d if abs(d) > 0.005 else "0").replace("0.", ".", 1).replace("-.", "-.")])
T_RUNS.append(["Coders agree on primary type (run 1 | run 2)", "%d of 146 (%d%%)" % (PRIM_146_R1, round(100 * PRIM_146_R1 / 146)), "%d of 146 (%d%%)" % (PRIM_146_R2, round(100 * PRIM_146_R2 / 146)), ""])
T_RUNS.append(["GPT against its own run 1 (primary type | set of types)", "%d%%" % RT["gpt"][0], "%d%%" % RT["gpt"][1], ""])
T_RUNS.append(["Gemini against its own run 1 (primary type | set of types)", "%d%%" % RT["gemini"][0], "%d%%" % RT["gemini"][1], ""])

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    print("units", N_UNITS, dict(N_BY), "prompts", N_PROMPT, "primary responses", N_PRIMARY_RESP, "sessions", N_SESSIONS, "new beyond 146:", N_NEW)
    print("T1:"); [print("  ", r) for r in T1]
    print("pct human", {t: pct("human", t) for t in "KPDMX"}, "primary", {t: pct("AI-primary", t) for t in "KPDMX"}, "sub", {t: pct("AI-subagent", t) for t in "KPDMX"})
    print("kappa main:", {(r["actor"], r["type"]): r["kappa"] for r in AGMAIN})
    print("kappa min/max over K P D M X rows", min(float(r["kappa"]) for r in AGMAIN), max(float(r["kappa"]) for r in AGMAIN))
    print("alpha vs kappa max abs diff", max(abs(float(r["alpha"]) - float(r["kappa"])) for r in AGMAIN))
    print("primary agreement all", PRIM_ALL, "/", N_UNITS, "| on 146 run1", PRIM_146_R1, "run2", PRIM_146_R2)
    print("confusions", [(k, v) for k, v in conf.most_common() if k[0] != k[1]][:6])
    print("kappa run1 vs run2 on the 146:", {k: (K1[k], K2[k]) for k in common_pairs})
    print("retest:", {c: (r["pct_primary"], r["pct_type_set"]) for c, r in retest.items()})
    print("MODES", MODES, "report and commit", REPORT_COMMIT, "total transitions", TRANS_TOTAL)
    for a in ("human", "AI-primary", "AI-subagent"): print("stage", a, stage_tot(a)[0], stage_tot(a)[1].most_common(4))
    print("episodes", N_EP, "units", EP_UNITS, "median", MEDIAN_RUN, "long", N_LONG, LONG_UNITS, "xm", LONG_XM, "next after run", dict(NEXT_AFTER_RUN["gpt"]), dict(NEXT_AFTER_RUN["gemini"]), N_EP_NEXT)
    print("fate", len(FATE), len(FATE_LATER), FATE_D, "AI D units", AI_D_UNITS, "human without D", len(HUM_NO_D))
    print("bad exemplars", BAD_EXEMPLARS)
    print("T_COD:"); [print("  ", r) for r in T_COD]
