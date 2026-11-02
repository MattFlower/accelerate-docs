#!/usr/bin/env python3
"""Merge the two vendors' adjudications per finding.
Usage: p1_merge.py <keys.json|all>  -> phase1/merged.json + summary on stdout.
Status per finding:
  agree_gold      both REAL, both blocker/major
  agree_minor     both REAL, both minor/nit
  agree_reject    neither REAL (NOT_REAL / NOT_CODE)
  sev_dispute     both REAL, one major+ and one minor-
  verdict_dispute one REAL, the other not (or UNCLEAR involved)
  missing         an output is missing or unparseable
"""
import json, os, re, sys
from collections import Counter
P = os.path.expanduser("~/limitless-orch/review-research/phase1")
items = {i["key"]: i for i in json.load(open(f"{P}/items.json"))}
keys = list(items) if sys.argv[1] == "all" else json.load(open(sys.argv[1]))
BLOCKING = {"blocker", "major"}


def load(key, vendor):
    path = f"{P}/adj/{key}.{vendor}.out"
    if not os.path.exists(path):
        return None
    text = open(path).read()
    # Opus may wrap the JSON in a fence or prose; take the outermost {"verdicts": ...} object.
    start = text.find('{"verdicts"')
    if start < 0:
        start = text.find("{")
    end = text.rfind("}")
    try:
        data = json.loads(text[start:end + 1])
    except Exception:
        m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.S)
        if not m:
            return None
        data = json.loads(m.group(1))
    return {v["id"]: v for v in data.get("verdicts", [])}


def status(a, b):
    if a is None or b is None:
        return "missing"
    ra, rb = a.get("verdict") == "REAL", b.get("verdict") == "REAL"
    if ra and rb:
        ga, gb = a.get("severity") in BLOCKING, b.get("severity") in BLOCKING
        return "agree_gold" if ga and gb else "agree_minor" if not ga and not gb else "sev_dispute"
    if not ra and not rb and a.get("verdict") != "UNCLEAR" and b.get("verdict") != "UNCLEAR":
        return "agree_reject"
    return "verdict_dispute"


merged, counts = [], Counter()
for key in keys:
    item = items[key]
    oc, oo = load(key, "codex"), load(key, "opus")
    for f in item["findings"]:
        a = oc.get(f["fid"]) if oc else None
        b = oo.get(f["fid"]) if oo else None
        s = status(a, b)
        counts[s] += 1
        merged.append({"key": key, "fid": f["fid"], "finding_key": f["key"], "split": item["split"], "era": item["era"],
                       "title": f["title"], "file": f["file"], "line": f["line"], "status": s, "codex": a, "opus": b})
json.dump(merged, open(f"{P}/merged.json", "w"), indent=1)
print(len(merged), dict(counts))
fix = Counter((m["codex"] or {}).get("fix_status") for m in merged if m["status"] == "agree_gold")
print("agree_gold fix_status (codex):", dict(fix))
print("origin (codex, gold):", dict(Counter((m["codex"] or {}).get("origin") for m in merged if m["status"] == "agree_gold")))
