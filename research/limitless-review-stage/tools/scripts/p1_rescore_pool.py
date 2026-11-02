#!/usr/bin/env python3
"""Rescore the stored Phase 0 dev arms with the new pool gold (phase1/pool_labels.json, status new_gold).
A trial catches a pool group when one of its own findings is a member of the group with blocker/major severity.
Old gold uses Phase 0's final judged result (final_table.py, executed for its `res`). Dev only: pool gold never
decides held-out. Out: stdout table + phase1/rescore_pool.json"""
import contextlib, io, json, os, re
from collections import defaultdict
R = os.path.expanduser("~/limitless-orch/review-research/")
P = R + "phase1/"
with contextlib.redirect_stdout(io.StringIO()):
    ns = {}
    exec(open(R + "scripts/final_table.py").read(), ns)
res, rows, items = ns["res"], ns["rows"], ns["items"]
stored = json.load(open(P + "pool_stored.json"))
clusters = {c: json.load(open(f"{P}pool/{c}.clusters.json"))["clusters"] for c in stored if os.path.exists(f"{P}pool/{c}.clusters.json")}
groups = [g for g in json.load(open(P + "pool_labels.json"))["groups"] if g["split"] == "dev" and g["status"] == "new_gold"]
BLK = ("blocker", "major")

# (eval, system, case, trial) -> set of group indices caught with a blocking finding
caught = defaultdict(set)
for gi, g in enumerate(groups):
    case = g["case"]
    for claim in g["members"]:
        n = int(re.match(r"C(\d+)", claim.split("/")[1]).group(1))
        for m in clusters[case][n - 1]["members"]:
            f = stored[case][int(m[1:]) - 1]
            if f.get("severity") in BLK:
                caught[(f["_eval"], f["_system"], case, str(f["_trial"]))].add(gi)
by_case = defaultdict(list)
for gi, g in enumerate(groups):
    by_case[g["case"]].append(gi)

out = {}
print(f"{'arm':34} {'old gold':>14} {'pool gold':>14} {'combined':>14}  vs prod")
for split, ev, sysn, label in rows:
    if split != "dev":
        continue
    old = res[label]
    oc, on = sum(old.values()), len(old)
    trials = {(cid, trial) for cid, trial, _ in old}
    pc = pn = 0
    for cid, trial in trials:
        for gi in by_case.get(cid, []):
            pn += 1
            pc += gi in caught[(ev, sysn, cid, str(trial))]
    out[label] = {"old": [oc, on], "pool": [pc, pn], "combined": [oc + pc, on + pn]}
base = out["production sol@medium (E1)"]["combined"]
for label, v in out.items():
    f = lambda c, n: f"{c:3}/{n:3} {100 * c / max(1, n):5.1f}"
    d = 100 * v["combined"][0] / max(1, v["combined"][1]) - 100 * base[0] / base[1]
    print(f"{label:34} {f(*v['old']):>14} {f(*v['pool']):>14} {f(*v['combined']):>14}  {d:+5.1f}")
json.dump(out, open(P + "rescore_pool.json", "w"), indent=1)
