"""Verbatim archive of the human side of the record.
1. records/verbatim/human_messages_verbatim.csv : every user message of every non-coder session, full text, UTF-8, read from the raw
   session exports (records/raw_sessions). Human messages in the main sessions, primary-agent prompts in the sub-agent sessions.
2. records/verbatim/logs_snapshot_<timestamp>/ : copies of the four logs and the registry with SHA256SUMS.txt.
Nothing in records/raw_sessions or records/logs is modified. The files contain identifying details and stay private."""
import csv, datetime, hashlib, io, json, os, shutil
ROOT = r"<project>"
REC = os.path.join(ROOT, "records"); OUT = os.path.join(REC, "verbatim"); os.makedirs(OUT, exist_ok=True)
reg = list(csv.DictReader(open(os.path.join(REC, "session_registry.csv"), encoding="utf-8-sig")))
tz = datetime.timezone(datetime.timedelta(hours=8))
rows = []
for s in reg:
    if (s["title"] or "").startswith("coder-"): continue
    j = json.load(open(os.path.join(REC, s["raw_file"]), encoding="utf-8"))
    n = 0
    for m in j["messages"]:
        if m["info"]["role"] != "user": continue
        n += 1
        txt = "\n".join(p.get("text", "") for p in m["parts"] if p.get("type") == "text")
        t = m["info"]["time"]["created"]
        rows.append(dict(session_id=s["session_id"], session_title=s["title"], is_subagent_prompt=int(bool(s["parent_session_id"])), seq=n, message_id=m["info"]["id"],
                         time=datetime.datetime.fromtimestamp(t / 1000, tz).strftime("%Y-%m-%dT%H:%M:%S+08:00"), chars=len(txt), text=txt))
rows.sort(key=lambda r: (r["time"], r["session_id"]))
with open(os.path.join(OUT, "human_messages_verbatim.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
hum = [r for r in rows if not r["is_subagent_prompt"]]
print("user messages", len(rows), "human messages", len(hum), "sessions", len({r["session_id"] for r in rows}))
stamp = datetime.datetime.now(tz).strftime("%Y%m%dT%H%M")
snap = os.path.join(OUT, "logs_snapshot_" + stamp); os.makedirs(snap, exist_ok=True)
files = [os.path.join(REC, "logs", n) for n in ("interventions.csv", "events.csv", "verification.csv", "artifacts.csv")] + [os.path.join(REC, "session_registry.csv"), os.path.join(OUT, "human_messages_verbatim.csv")]
sums = []
for p in files:
    d = os.path.join(snap, os.path.basename(p))
    if os.path.abspath(p) != os.path.abspath(d): shutil.copy2(p, d)
    sums.append("%s  %s" % (hashlib.sha256(open(p, "rb").read()).hexdigest(), os.path.basename(p)))
open(os.path.join(snap, "SHA256SUMS.txt"), "w", encoding="utf-8").write("\n".join(sums) + "\n")
open(os.path.join(OUT, "README_verbatim.md"), "w", encoding="utf-8").write(
 "# Verbatim record (private)\n\nThis folder holds the original wording of the human side of the project, unedited and in correct UTF-8.\n\n"
 "- `human_messages_verbatim.csv`: every user message of every non-coder session, read from `records/raw_sessions`. Rows with `is_subagent_prompt=1` are prompts that the primary agent wrote to sub-agents.\n"
 "- `logs_snapshot_*/`: copies of the four append-only logs and the session registry with SHA-256 sums.\n\n"
 "The files contain identifying details (names, resource names, local paths) and must not be published without redaction. Released copies are made by `submission/build_release.py`, which masks them and keeps the masking map out of the release.\n\n"
 "Known defect in the logs: the summaries of I022, I033 and I035 were written to the CSV in a garbled encoding. The correct original of each is the human message in `human_messages_verbatim.csv` at the same time.\n")
print("snapshot", snap)
for p in sums: print(p)
