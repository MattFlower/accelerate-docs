#!/usr/bin/env python3
"""Merge both vendors' adjudications of pooled claims -> phase1/pool_merged.json (same shape as merged.json, so
p1_sev.py prompts/score and p1_label.py logic apply). Extra entries "<id>b" (a claim split by an adjudicator) are kept
when either vendor reports them. duplicate_of G<n> marks a claim that restates existing gold.
Usage: p1_pool_merge.py"""
import json, os, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
P = os.path.expanduser("~/limitless-orch/review-research/phase1")
items = {i["key"]: i for i in json.load(open(f"{P}/pool_items.json"))}
exec(open(os.path.join(os.path.dirname(__file__), "p1_merge.py")).read().split("merged, counts = [], Counter()")[0]
     .replace('items = {i["key"]: i for i in json.load(open(f"{P}/items.json"))}', "")
     .replace('keys = list(items) if sys.argv[1] == "all" else json.load(open(sys.argv[1]))', ""))

merged, counts = [], Counter()
for key, item in items.items():
    oc, oo = load(f"pool-{key}", "codex"), load(f"pool-{key}", "opus")  # noqa: F821 (from p1_merge)
    ids = [c["fid"] for c in item["claims"]]
    ids += sorted({i for o in (oc or {}, oo or {}) for i in o if i.endswith("b") and i[:-1] in ids})
    claims = {c["fid"]: c for c in item["claims"]}
    for fid in ids:
        a = oc.get(fid) if oc else None
        b = oo.get(fid) if oo else None
        s = status(a, b)  # noqa: F821
        if fid.endswith("b") and (a is None or b is None):
            s = "split_one_side"
        counts[s] += 1
        base = claims.get(fid.rstrip("b")) or {}
        v0 = (base.get("variants") or [{}])[0]
        real_sides = [x for x in (a, b) if x and x.get("verdict") == "REAL"]
        gold_dup = bool(real_sides) and all(str(x.get("duplicate_of") or "").startswith("G") for x in real_sides)
        merged.append({"key": f"pool-{key}", "fid": fid, "case": key, "split": item["split"], "era": None,
                       "title": v0.get("title"), "file": v0.get("file"), "line": v0.get("line"),
                       "reported_times": base.get("reported_times"), "systems": base.get("systems"),
                       "status": s, "dup_of_gold": bool(gold_dup), "codex": a, "opus": b})
json.dump(merged, open(f"{P}/pool_merged.json", "w"), indent=1)
print(len(merged), dict(counts))
print("REAL by both, not a gold duplicate:",
      sum(1 for m in merged if m["status"] in ("agree_gold", "agree_minor", "sev_dispute") and not m["dup_of_gold"]))
