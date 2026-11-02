#!/usr/bin/env python3
"""Pool claims -> proposed new gold, per dedup group.
Usage: p1_pool_label.py labels   -> phase1/pool_labels.json + summary
       p1_pool_label.py todo     -> phase1/pool_todo.txt: claims whose ruling can still change a dev group's gold status
Rulings: phase1/pool_mine.json {"pool-review-NNN/Cn": {"sev": "blocker|major|minor|nit|not_real", "why": "..."}};
pool_val_mine.json and pool_val2_mine.json (validation rulings) are read too.
Gold = real, blocker/major, not a duplicate of existing gold (adjudicators or dedup same_as), origin not preexisting by
every REAL side, and not a requirement gap the request doesn't state (Q3 not_explicit)."""
import json, os, sys
from collections import Counter
P = os.path.expanduser("~/limitless-orch/review-research/phase1")
merged = json.load(open(f"{P}/pool_merged.json"))
sev = json.load(open(f"{P}/pool_sev3_scored.json"))
mine = {}
for f in ("pool_val_mine.json", "pool_val2_mine.json", "pool_mine.json"):
    if os.path.exists(f"{P}/{f}"):
        mine.update(json.load(open(f"{P}/{f}")))
mine = {k: v for k, v in mine.items() if not k.startswith("_")}


def load_dir(d):
    out = {}
    for f in os.listdir(f"{P}/{d}"):
        if f.endswith(".json"):
            out[f[:-5]] = json.load(open(f"{P}/{d}/{f}"))
    return out


dedup, q3 = load_dir("pool_dedup"), load_dir("pool_q3")
BLOCKING = ("blocker", "major")


def label(m):
    k = f"{m['key']}/{m['fid']}"
    sides = [s for s in (m["codex"], m["opus"]) if s]
    real_sides = [s for s in sides if s.get("verdict") == "REAL"]
    ruling = mine.get(k, {}).get("sev")
    if ruling == "not_real":
        real = False
    elif ruling:
        real = True
    elif m["status"] == "agree_reject" or not real_sides:
        real = False
    elif len(real_sides) == 2:
        real = True
    else:
        real = None
    s = ruling if ruling and ruling != "not_real" else (sev.get(k, {}).get("final") if real else None)
    if s == "blocking":
        s = "major"
    q3v = {i["id"]: i["verdict"] for i in q3.get(m["case"], {}).get("items", [])}
    gap = bool(real_sides) and all(x.get("origin") == "requirement_gap" for x in real_sides)
    return {"claim": k, "case": m["case"], "split": m["split"], "title": m["title"], "real": real, "severity": s,
            "severity_by": "orchestrator" if ruling else "raters" if s else None,
            "dup_gold": bool(m.get("dup_of_gold")),
            "preexisting": bool(real_sides) and all(x.get("origin") == "preexisting" for x in real_sides),
            "q3_excluded": gap and q3v.get(m["fid"]) == "not_explicit"}


def groups():
    labels = {l["claim"]: l for l in map(label, merged)}
    out = []
    for case, d in sorted(dedup.items()):
        for g in d["groups"]:
            members = [labels[f"pool-{case}/{c}"] for c in g["members"] if f"pool-{case}/{c}" in labels]
            if not members:
                continue
            same_gold = bool(g.get("same_as")) or any(x["dup_gold"] for x in members)
            excl = lambda x: x["preexisting"] or x["q3_excluded"]
            gold_members = [x for x in members if x["real"] and x["severity"] in BLOCKING and not excl(x)]
            open_members = [x for x in members if not excl(x) and (x["real"] is None or (x["real"] and not x["severity"]))]
            status = ("existing_gold" if same_gold else "new_gold" if gold_members else
                      "unresolved" if open_members else "not_gold")
            sevs = [x["severity"] for x in gold_members]
            out.append({"case": case, "split": members[0]["split"], "members": [x["claim"] for x in members],
                        "root_cause": g.get("root_cause"), "status": status,
                        "severity": "blocker" if "blocker" in sevs else "major" if sevs else None,
                        "open": [x["claim"] for x in open_members] if status == "unresolved" else []})
    return labels, out


if __name__ == "__main__":
    labels, gs = groups()
    if sys.argv[1] == "labels":
        json.dump({"claims": labels, "groups": gs}, open(f"{P}/pool_labels.json", "w"), indent=1)
        for split in ("dev", "heldout"):
            print(split, Counter(g["status"] for g in gs if g["split"] == split))
        print("new gold by severity (dev)", Counter(g["severity"] for g in gs if g["split"] == "dev" and g["status"] == "new_gold"))
    else:
        todo = [c for g in gs if g["split"] == "dev" and g["status"] == "unresolved" for c in g["open"]]
        open(f"{P}/pool_todo.txt", "w").write("\n".join(todo) + "\n")
        print(len(todo), "claims to rule in", sum(1 for g in gs if g["split"] == "dev" and g["status"] == "unresolved"), "dev groups")
