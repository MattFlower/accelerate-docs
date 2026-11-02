# review-124 (held-out, labelled CLEAN)

```json
{
 "id": "review-124",
 "repo": "MattFlower/limitless",
 "base": "b82747ba0a1789e69d651af2caf99c1b0f288597",
 "head": "4cfeb5fd66a50afc2dde94e79fb1456feed9d5d8",
 "source": "pr #456 fresh clean set 2026-10-16 @ 4cfeb5f",
 "prompt": "## Problem\nThe landing queue checks a PR against the wrong base when the land request resolves to a review-round run. `LandQueue.request` (`src/land/queue.ts`, around line 166) takes `baseBranch: run.baseBranch ?? repo.defaultBranch` from the run it was given. A review round's run delivers onto the PR's head branch, so its `baseBranch` is that same branch. The queue then \"merges the base\" by merging the PR branch into itself, a no-op, and runs the land check on the PR head **without** the PR's real base (`main`).\n\nSeen on 2026-10-10: land entry 13 for PR #446 (requested through the round run <run-id>) recorded `base_branch` = the PR's own branch, and its check ran a tree missing #447, which had been on `main` for hours (two tests failed on the old 10 s barrier #447 had removed). Entry 9 for #443 (also a round run) only checked the right tree because its head already contained `main`. GitHub's `pull_request` CI runs on the merge ref, which catches some of this, but the queue's own land check, the one that gates the merge, tested the wrong tree.\n\n## Change\n- A land entry's base branch is the PR's real base: the owning (non-round) run's base branch, or the base branch GitHub reports for the PR. Never a branch equal to the entry's head branch. Use one resolution for every way a land is requested (`limitless land <run|pr|url>`, `POST /api/land`, MCP `limitless_land`, review approval).\n- If the base can't be determined, block the entry with a clear reason instead of guessing.\n- Entries already queued keep working; when a stored `base_branch` equals its `head_branch`, resolve the real base when the entry runs.\n\n## Tests (fake `gh`, a local bare repository)\n- Requesting a land through a review-round run records `main` as the base and merges current `main` into the approved head before the check.\n- An entry stored with `base_branch` = `head_branch` is resolved to the real base when it runs.\n- An undeterminable base blocks with a clear reason.\n- Each test fails without the change.\n\n## Budget\nSmall to medium.\n\n## Out of scope\n- Conflict rounds (#46)."
}
```

# Blocking findings (verifier high/critical or security), both trials

## trial 0: Recheck the claim after resolving a stored entry’s base
```json
{
 "severity": "major",
 "security": false,
 "file": "src/land/queue.ts",
 "line": 305,
 "title": "Recheck the claim after resolving a stored entry’s base",
 "detail": "Base resolution can wait on GitHub, but the subsequent update and landing work do not verify that the entry is still active and owned by this worker. Cancellation through another queue process cannot abort this process’s in-memory controller. The worker can therefore continue after cancellation and later write `waiting_ci`, reviving the entry and potentially merging it.",
 "suggestion": "After the lookup, conditionally update the entry only if its claim is still owned and its state remains active; stop processing if the conditional update fails.",
 "failure_scenario": "A resumed legacy entry has `base_branch == head_branch` and needs a GitHub lookup. While that lookup is pending, another daemon or CLI-backed queue cancels it. The lookup returns before the next heartbeat, and the original worker continues checking and writes `waiting_ci` over `cancelled`.",
 "category": "concurrency",
 "confidence": 0.94,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "PLAUSIBLE",
  "evidence": "src/land/queue.ts:303–306: `const baseBranch = await this.resolveBase(...); signal.throwIfAborted(); ... this.store.updateLandEntry(entry.id, { baseBranch, pushedSha: null, ciRerun: null });`. Cross-process cancellation is detected only by the heartbeat at :274–277, scheduled every `CLAIM_STALE_MS / 3` (10 seconds). At :321 the worker writes `{ pushedSha: head, state: \"waiting_ci\" }`. src/db/store.ts:2328 updates with only `WHERE id = ?`, without checking state or claim ownership.",
  "trigger": "Another process cancels a legacy entry during its base lookup. If subsequent work reaches the waiting_ci write before the next heartbeat, the worker overwrites cancelled and continues processing.",
  "severity": "high",
  "category": "concurrency"
 },
 "agreement": 1,
 "duplicates": []
}
```

## trial 0: A retargeted PR can be checked against its former base
```json
{
 "severity": "major",
 "security": true,
 "file": "src/land/queue.ts",
 "line": 201,
 "title": "A retargeted PR can be checked against its former base",
 "detail": "The resolver accepts the owning run's recorded base without checking the PR's current base. If the PR was retargeted after the run was created, a review-round land checks and loads gate configuration from the former base, then GitHub merges into the new base. The check therefore does not cover the tree or trusted policy of the branch receiving the change.",
 "suggestion": "Resolve the current PR base from GitHub when requesting or processing the land, and block if it cannot be confirmed. Ensure the base remains the one checked before merging.",
 "failure_scenario": "A run opened a PR against main, the PR is retargeted to release, and a review round requests landing. The queue records main, merges and runs main's gates, while GitHub merges the PR into release.",
 "category": "security",
 "confidence": 0.97,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "src/land/queue.ts:201: `if (owner?.sourceRef?.kind !== \"review-round\" && valid(owner?.baseBranch)) return owner.baseBranch;` precedes the GitHub lookup at :203. At :302, stored bases are reconsidered only when empty or equal to the head. At :313–317, `entry.baseBranch` supplies the fetched base and checks. The merge call at :542–554 passes the PR URL and head SHA without validating its current base.",
  "trigger": "The owner records main, but the PR is retargeted to release before a review round requests landing. Resolution returns main without querying GitHub; the queue checks main's merged tree and gates while GitHub targets release.",
  "severity": "medium",
  "category": "correctness"
 },
 "agreement": 1,
 "duplicates": []
}
```

## trial 1: Preserve recovery for an already merged legacy entry
```json
{
 "severity": "major",
 "security": false,
 "file": "src/land/queue.ts",
 "line": 306,
 "title": "Preserve recovery for an already merged legacy entry",
 "detail": "Resolving a legacy entry clears its durable pushed SHA before checking whether its PR has already merged. If the previous daemon successfully merged the PR but stopped before recording `landed`, the resumed worker now rechecks and attempts to push before reaching the existing already-merged observation path. If GitHub deleted the head branch after the merge, that push is blocked as a moved head, leaving a successfully merged PR recorded as blocked. A restart after this update also loses the checkpoint needed to recognize that prior progress.",
 "suggestion": "Check and record an already merged PR before resetting legacy check progress, and preserve enough durable state to recover across a restart during base resolution.",
 "failure_scenario": "A legacy entry has base_branch equal to head_branch and state `merging`; GitHub completed the squash merge and deleted the PR branch, but the daemon stopped before recording `landed`. On restart, the entry is rechecked and then blocks when it cannot push to the deleted branch.",
 "category": "compatibility",
 "confidence": 0.98,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "src/land/queue.ts:302–306 repairs a legacy base and clears progress: `entry = this.store.updateLandEntry(entry.id, { baseBranch, pushedSha: null, ciRerun: null });`. Lines 315–319 consequently rerun the merge/check/push path before line 325 checks whether the PR already merged. At lines 379–380, `const remote = await remoteBranchSha(repo, cwd, entry.headBranch, signal); if (remote !== entry.approvedSha) throw new LandBlocked(\"head moved after approval\");`. The process catch at line 285 calls `this.block(entry.id, (error as Error).message)`.",
  "trigger": "Restart with a legacy entry in `merging`, baseBranch equal to headBranch, after GitHub completed the squash merge and deleted the head branch. Repair clears pushedSha; the updated base requires a merge commit, and the deleted remote branch fails the push guard before merged-state recovery runs. The completed land is incorrectly recorded as blocked.",
  "severity": "high",
  "category": "reliability"
 },
 "agreement": 1,
 "duplicates": []
}
```
