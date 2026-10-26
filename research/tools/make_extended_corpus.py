"""Extended corpus for the recode of 26 October 2026 (rule: recode at each major revision, S01-U045).
Reads units_all.csv (rebuilt from the synced exports), keeps the 146 frozen units unchanged, adds later units up to the cutoff
(the last human message before the recode request), removes harness artefacts, writes units_ext.csv, packet_ext.md and exclusions.csv."""
import csv, io, re, sys, datetime, collections, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
R = r"research/coding/"
old = list(csv.DictReader(open(R + "units_all_v1_146.csv", encoding="utf-8-sig")))
new = list(csv.DictReader(open(R + "units_all.csv", encoding="utf-8-sig")))
oldids = {u["unit_id"] for u in old}
byid = {u["unit_id"]: u for u in new}
assert all(byid[u["unit_id"]]["message_id"] == u["message_id"] and byid[u["unit_id"]]["text"] == u["text"] for u in old)
hum = [u for u in new if u["session"] == "S01" and u["actor_hint"] == "human"]
cut = int(hum[-1]["time"]); cut_id = hum[-1]["unit_id"]
def ts(u): return datetime.datetime.fromtimestamp(int(u["time"]) / 1000, datetime.timezone(datetime.timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")
excl = []   # (unit_id, rule, note)
def rules(prev_real_human_text, u, prev):
    t = u["text"].strip()
    if u["actor_hint"] == "human" and t == "":
        return "R1 empty user message"
    if u["actor_hint"] == "human" and t.startswith("Continue if you have next steps"):
        return "R2 harness continuation prompt"
    if u["actor_hint"].startswith("AI-primary") and t.startswith("## Objective") and "Co-write an ICIS 2026 PDW" in t:
        return "R3 context-compaction summary"
    if u["actor_hint"] == "human" and prev_real_human_text is not None and t == prev_real_human_text:
        return "R4 replay of the previous human message after compaction"
    return None
keep = []; last_real = {}
for u in new:
    uid = u["unit_id"]
    if int(u["time"]) >= cut: excl.append((uid, "R0 after cutoff", "the human message that requested the recode and everything after it")); continue
    if uid in oldids: keep.append(u)
    else:
        r = rules(last_real.get(u["session"]), u, None)
        if r: excl.append((uid, r, ts(u))); continue
        keep.append(u)
    if u["actor_hint"] == "human" and u["text"].strip() and not u["text"].startswith("Continue if you have next steps"):
        last_real[u["session"]] = u["text"].strip()
# the frozen 146 must not trip any rule
for u in old:
    pass
trip = [u["unit_id"] for u in old if rules(None, u, None) and not rules(None, u, None).startswith("R4") ]
print("frozen units tripping rules R1-R3:", trip)
print("units total", len(new), "kept", len(keep), "excluded", len(excl), dict(collections.Counter(e[1] for e in excl)))
print("kept by session", dict(sorted(collections.Counter(u["session"] for u in keep).items())))
nk = [u for u in keep if u["unit_id"] not in oldids]
print("new units to code", len(nk), dict(collections.Counter(u["session"] for u in nk)), "human", sum(u["actor_hint"] == "human" for u in nk), "ai", sum(u["actor_hint"] != "human" for u in nk))
print("kept human", sum(u["actor_hint"] == "human" for u in keep), "primary", sum(u["actor_hint"].startswith("AI-primary") for u in keep), "sub", sum(u["actor_hint"] == "AI-subagent" for u in keep))
fn = list(new[0].keys())
with open(R + "units_ext.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=fn); w.writeheader(); w.writerows(keep)
with open(R + "exclusions.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["unit_id", "rule", "note"]); w.writerows(excl)
ids = {u["unit_id"] for u in keep}
pk = io.open(R + "packet_all.md", encoding="utf-8").read()
parts = [p for p in re.split(r"(?m)^(?=### UNIT )", pk) if p.strip()]
sel = [p for p in parts if re.match(r"### UNIT (\S+)", p).group(1) in ids]
assert len(sel) == len(keep)
io.open(R + "packet_ext.md", "w", encoding="utf-8", newline="").write("".join(sel))
# two halves per coder to shorten the wall-clock time
h = len(sel) // 2
io.open(R + "packet_ext_a.md", "w", encoding="utf-8", newline="").write("".join(sel[:h]))
io.open(R + "packet_ext_b.md", "w", encoding="utf-8", newline="").write("".join(sel[h:]))
print("halves", h, len(sel) - h, "| first of b:", re.match(r"### UNIT (\S+)", sel[h]).group(1))
print("packet sha256", hashlib.sha256(open(R + "packet_ext.md", "rb").read()).hexdigest()[:16], "| cut", cut_id)
