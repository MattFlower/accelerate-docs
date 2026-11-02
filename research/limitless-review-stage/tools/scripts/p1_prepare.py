#!/usr/bin/env python3
"""Phase 1: build one blind adjudication item per included escape round.
Out: phase1/items.json  [{key, case_id, repo, pr, round, base, head, fix, era, split, findings:[{fid, file, line, title, detail}]}]
Severity is withheld from adjudicators. Era: 'opus' if the round predates 2026-10-23, else 'sol'."""
import json, re, sqlite3, os
P = os.path.expanduser("~/limitless-orch/review-research/phase1")
cases = json.load(open(f"{P}/candidate_cases.json"))
props = json.load(open(f"{P}/proposals.json"))
db = sqlite3.connect(f"file:{P}/limitless.db?mode=ro", uri=True)
items = []
for c in cases:
    m = re.match(r"pr #(\d+) review round-(\d+) @ \w+ fixed in (\w+)", c["source"])
    pr, rnd = int(m[1]), int(m[2])
    prefix = f"{c['repo']}#{pr}/round-{rnd}/"
    url = f"https://github.com/{c['repo']}/pull/{pr}"
    row = db.execute(
        "SELECT created_at, delivered_sha FROM review_rounds WHERE pr_url=? AND round=? AND kind='review' AND reviewed_sha=?",
        (url, rnd, c["head"]),
    ).fetchone()
    created, fix = row
    fs = sorted((k for k in props if k.startswith(prefix)), key=lambda k: int(k.rsplit("/", 1)[1]))
    findings = []
    for k in fs:
        o = props[k]["original"]
        findings.append({"fid": f"F{int(k.rsplit('/',1)[1])+1}", "key": k, "file": o["file"], "line": o["line"],
                         "title": o["title"], "detail": o["detail"]})
    items.append({
        "key": f"{c['repo'].split('/')[1]}-{pr}-r{rnd}", "case_id": c["id"], "repo": c["repo"], "pr": pr, "round": rnd,
        "base": c["base"], "head": c["head"], "fix": fix, "created": created,
        "era": "opus" if created < 1792713600000 else "sol",  # 2026-10-23T00:00Z
        "split": c["split"], "prompt": c["input"]["prompt"], "findings": findings,
    })
json.dump(items, open(f"{P}/items.json", "w"), indent=1)
from collections import Counter
print(len(items), sum(len(i["findings"]) for i in items))
print(Counter((i["split"], i["era"]) for i in items))
