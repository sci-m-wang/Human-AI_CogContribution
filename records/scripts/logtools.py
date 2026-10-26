"""Append rows to the project logs with the real clock and the next free ID (avoids hand-typed timestamps and IDs, see E074).
Usage from a script:  from logtools import app, now ;  app('events.csv', dict(stage='paper', event_type='x', description='...', ...))
Missing columns are written empty. The ID column and timestamp are filled in by this module."""
import csv, datetime, io, os
ROOT = r"<project>"
LOGS = os.path.join(ROOT, "records", "logs")
SESSION = "ses_ea32c9901ffe7o77BUt54LtH2Q"
MODEL = "github-copilot/claude-sonnet-5.5"
IDCOL = {"events.csv": ("event_id", "E"), "interventions.csv": ("intervention_id", "I"), "verification.csv": ("verification_id", "V"), "artifacts.csv": ("artifact_id", "A")}
TSCOL = {"events.csv": "timestamp", "interventions.csv": "timestamp", "verification.csv": "timestamp", "artifacts.csv": "created_at"}
AGENTCOL = {"events.csv": "agent", "verification.csv": "agent_or_actor", "artifacts.csv": "created_by"}
SESCOL = {"events.csv": "session_id", "interventions.csv": "session_id", "verification.csv": "session_id", "artifacts.csv": "created_in_session"}
def now():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).strftime("%Y-%m-%dT%H:%M") + "+08:00"
def app(name, *rows):
    path = os.path.join(LOGS, name)
    with open(path, encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f); cols = rd.fieldnames; existing = list(rd)
    idc, pre = IDCOL[name]
    last = max(int(r[idc][1:]) for r in existing)
    out = []
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        for r in rows:
            last += 1
            d = dict(r); d[idc] = "%s%03d" % (pre, last); d[TSCOL[name]] = now()
            d.setdefault(SESCOL[name], SESSION)
            if name in AGENTCOL: d.setdefault(AGENTCOL[name], MODEL)
            bad = [k for k in d if k not in cols]
            assert not bad, bad
            w.writerow([d.get(c, "") for c in cols]); out.append(d[idc])
    return out
