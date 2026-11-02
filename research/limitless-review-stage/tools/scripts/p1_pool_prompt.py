#!/usr/bin/env python3
"""Write phase1/adj/pool-<case>.prompt for pooled claims (stored-trial findings no judge matched to gold).
Usage: p1_pool_prompt.py [case ...]   (default: all in pool_items.json); prints checkout lines for p1_checkout.sh"""
import json, os, sys
P = os.path.expanduser("~/limitless-orch/review-research/phase1")
sys.path.insert(0, os.path.dirname(__file__))
from p1_prompt import TEMPLATE  # noqa: E402

items = {i["key"]: i for i in json.load(open(f"{P}/pool_items.json"))}
GOLD_NOTE = """
# Defects already known for this change (gold)
A claim that describes the same mechanism as one of these is verdict REAL with duplicate_of set to that gold id
(G1, G2, ...); still give its severity and scenario.
```json
{gold}
```
"""

for key in (sys.argv[1:] or list(items)):
    i = items[key]
    prompt = i["prompt"] if len(i["prompt"]) <= 24000 else i["prompt"][:24000] + "\n[... request truncated ...]"
    claims = [{"id": c["fid"], "reported_times": c["reported_times"], "variants": c["variants"]} for c in i["claims"]]
    text = TEMPLATE.format(base=i["base"], head=i["head"], fix="(none)", prompt=prompt, claims=json.dumps(claims, indent=1))
    # No later fix commit for these: drop the fix step and the fix_status field's meaning.
    text = text.replace(
        "A later commit, (none), is the factory's response to the review; it is in the repository but NOT checked out.\n", "")
    text = text.replace(
        f"Step 2: only after step 1, inspect `git diff {i['head']}..(none)` and say whether that later commit addresses this claim's\n"
        "mechanism (yes / partial / no / unrelated). A fix existing does not by itself make a claim real.\n",
        "Each claim may have several wordings (variants) from different reviewer runs; judge the claim they share. If the\n"
        "variants describe different mechanisms, judge the first variant and add an extra entry with id \"<id>b\" for the other.\n")
    text = text.replace('"fix_status": "yes|partial|no|unrelated", ', "")
    gold = [{"id": f"G{n+1}", **g} for n, g in enumerate(i["gold"])]
    text = text.replace("# Claims\n", GOLD_NOTE.format(gold=json.dumps(gold, indent=1)) + "\n# Claims\n", 1)
    open(f"{P}/adj/pool-{key}.prompt", "w").write(text)
    print(f"pool-{key} {i['repo'].split('/')[1]} {i['head']}")
