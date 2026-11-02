#!/usr/bin/env python3
"""Final proposed labels from adjudications (merged.json), severity raters (sev_scored.json) and my rulings.
Usage: p1_label.py <out.json> [sheet.md N seed]
Rules: reality = both adjudicators REAL, or my ruling on a verdict dispute; severity = my ruling, else rater consensus
(both raters agree on blocking-or-not; a blocking consensus with different levels takes major), else unresolved.
Gold = REAL, blocker/major, not a duplicate, origin not 'preexisting' by both adjudicators."""
import json, os, random, sys
from collections import Counter
P = os.path.expanduser("~/limitless-orch/review-research/phase1")
merged = json.load(open(f"{P}/merged.json"))
SEV = os.environ.get("SEV", f"{P}/sev3_scored.json")
sev = json.load(open(SEV)) if os.path.exists(SEV) else {}
mine = json.load(open(f"{P}/my_sev_rulings.json"))
items = {i["key"]: i for i in json.load(open(f"{P}/items.json"))}

labels = []
for m in merged:
    k = f"{m['key']}/{m['fid']}"
    c, o = m["codex"] or {}, m["opus"] or {}
    real = None
    if m["status"] == "agree_reject":
        real = False
    elif m["status"] in ("agree_gold", "agree_minor", "sev_dispute"):
        real = True
    elif k in mine:
        real = mine[k] not in ("not_real", "unsure") if mine[k] != "unsure" else None
    severity, how = None, None
    if real:
        if k in mine and mine[k] not in ("unsure", "not_real"):
            severity, how = mine[k], "orchestrator"
        elif k in sev and sev[k]["status"] == "agree":
            s = sev[k]["sev"]
            severity = s["sonnet"] if s["sonnet"] == s["terra"] else ("major" if s["sonnet"] in ("blocker", "major") else "minor")
            how = "raters"
    dup = c.get("duplicate_of") and o.get("duplicate_of")
    pre = c.get("origin") == "preexisting" and o.get("origin") == "preexisting"
    gold = bool(real and severity in ("blocker", "major") and not dup and not pre)
    best = c if c.get("verdict") == "REAL" and isinstance(c.get("reproduction"), dict) else o if o.get("verdict") == "REAL" else c
    labels.append({"finding": k, "pr": items[m["key"]]["pr"], "round": items[m["key"]]["round"], "split": m["split"],
                   "era": m["era"], "title": m["title"], "real": real, "severity": severity, "severity_by": how,
                   "gold": gold if real is not None and (severity or real is False) else None,
                   "duplicate": bool(dup), "preexisting": pre,
                   "scenario": best.get("failure_scenario"), "reproduced": isinstance(best.get("reproduction"), dict),
                   "repro": best.get("reproduction"), "criterion": best.get("criterion"),
                   "fixed_later": c.get("fix_status") or o.get("fix_status"),
                   "why_not_real": (c.get("reason") if c.get("verdict") != "REAL" else o.get("reason")) if real is False else None})
json.dump(labels, open(sys.argv[1], "w"), indent=1)
print(len(labels), Counter("unresolved" if l["gold"] is None else "gold" if l["gold"] else "not gold" for l in labels))
print("severity_by", Counter(l["severity_by"] for l in labels if l["real"]))

if len(sys.argv) > 2:
    n, seed = int(sys.argv[3]), sys.argv[4]
    pick = random.Random(seed).sample(labels, min(n, len(labels)))
    out = ["# Spot-check batch: escape-corpus pilot (20 random of %d labels)\n" % len(labels),
           "For each item: does the label follow from the scenario and the evidence? Reply with the numbers you",
           "disagree with and why (logic only; no TypeScript needed). \"Gold\" means a review must catch it.\n"]
    for i, l in enumerate(pick, 1):
        label = ("GOLD (%s)" % l["severity"]) if l["gold"] else ("not gold: %s" % (
            "not a real defect" if l["real"] is False else "duplicate" if l["duplicate"] else
            "already in main" if l["preexisting"] else (l["severity"] or "?"))) if l["gold"] is not None else "UNRESOLVED"
        repro = l["repro"]
        ev = ("reproduced: `%s`" % (repro.get("output") or "")[:220].replace("\n", " ").replace("`", "'")) if l["reproduced"] \
            else (str(repro)[:200] if repro else "no reproduction")
        out += [f"**{i}. PR #{l['pr']} round {l['round']}: {l['title']}**",
                f"- Label: **{label}**" + (f" (adjudicator's reading: {l['criterion']})" if l["gold"] and l["criterion"] else "")
                + (f" (severity set by {l['severity_by']})" if l["severity_by"] else ""),
                f"- Scenario: {l['scenario'] or l['why_not_real']}",
                f"- Evidence: {ev}",
                f"- Fixed in the next round: {l['fixed_later']}\n"]
    open(sys.argv[2], "w").write("\n".join(out))
    print("sheet", sys.argv[2])
