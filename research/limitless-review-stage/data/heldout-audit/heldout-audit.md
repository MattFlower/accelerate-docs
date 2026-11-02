# Held-out CLEAN audit: review-124, review-130, review-133

Code was read read-only from the bare caches. Use `origin/main`: the local `main` ref in the limitless cache is stale. The heads of 124 and 130 are byte-identical to what landed (#456 = ddc85773, #490 = 21e81796; `git diff` between each head and its landed commit is empty). Every flagged pattern is still present unchanged on origin/main, apart from the general claim-ownership guard #616 added later.

## review-124 (#456: land base resolution), head 4cfeb5f

**Claim A: no claim/state recheck after the base lookup, so a cross-process cancel gets overwritten by `waiting_ci` (trial 0, queue.ts:305). Verdict: NOT-REAL as introduced.**
- The :306 write after `resolveBase` sets only `baseBranch/pushedSha/ciRerun` and never `state`, so it cannot revive a cancelled entry.
- Because it sets `pushedSha: null`, the worker always goes on to `mergeBase` + `checks()` (:316–317). That runs the full gate suite (minutes) before the `waiting_ci` write at :321.
- `heartbeatLandClaim` (store.ts:2298) succeeds only while the state is active and this owner holds the claim. A cancel therefore fails the next beat (≤10 s, queue.ts:273–277), and `process()` returns without writing once aborted (:284).
- So the stated trigger, "reaches waiting_ci before the next heartbeat", can't happen through the new await.
- The underlying window (unconditional `updateLandEntry ... WHERE id = ?` after an await) existed before this change on the same paths. #616's request says it "predates that PR", and #616 fixed it generally with `this.owned(...)`.

**Claim B: a retargeted PR is checked against its former base (trial 0, security-flagged, queue.ts:201). Verdict: REAL-MINOR.**
- Mechanically true. `resolveBase` returns the owner's `baseBranch` without asking GitHub (:201), and `merge()` (:532–559) does not validate the PR's current base.
- But the request explicitly ranks "the owning (non-round) run's base branch" first. Non-round lands at base already used `run.baseBranch` unchecked.
- Retargeting a factory PR's base is an unusual operator action the request does not ask to handle.
- origin/main still resolves owner-first. Not a trust-boundary break: gates come from the owner's recorded base, which the factory chose, never from the PR branch.

**Claim C: an already-merged legacy entry gets recorded as blocked (trial 1, queue.ts:306). Verdict: REAL-MINOR.**
- The trace is right:
  - At base, a resumed `merging` entry kept `pushedSha`, so `awaitCi` saw MERGED and recorded `landed`.
  - At head, :302–306 clears `pushedSha` for a base==head entry, so main gets merged in and the gates rerun.
  - `pushApproved` (:379–380) then finds the branch deleted (the factory merges with `--delete-branch`, repos.ts:1271) and throws "head moved after approval". The entry ends blocked although the PR merged.
- The trigger is narrow and one-time:
  - Base==head entries are only those queued, through a review-round run, before the deploy that ships this. `resolveBase` refuses base==head from then on.
  - It also needs the daemon to die between GitHub completing `gh pr merge` and `landed()` (merge() :542–559), or a human to merge such an entry by hand while it waits.
- For ordinary legacy entries in `queued`/`checking`/`waiting_ci` that haven't merged, the re-check is exactly what the request asks for ("resolve the real base when the entry runs"). For legacy entries `pushedSha` always equals `approvedSha`, because merging the branch into itself is a no-op, so the lease push succeeds. "Entries already queued keep working" therefore holds in the normal case.
- The result is visible (a blocked entry for a merged PR), not silent corruption.

**Label: CLEAN holds** (no REAL-MAJOR).

## review-130 (#490: environment-blocked rounds push their commit), head 40056f0

**Claim D: an evidence-comment failure after the push leaves a pushed head with no 🚧 comment, and the run isn't resumed (engine.ts:2029–2065; 5 duplicates). Verdict: REAL-MINOR.**
- The ordering is true: `markRoundDelivered` + `save("round-delivered")` (:2029–2030) come before the comment lookup and post (:2035, :2065).
- The cost is small:
  - gh calls go through `withGitHubRetry` (:2089), so only a failure that outlasts the retries counts.
  - `publish()` (:2305) has already stored `report.md` with the 🚧 blocked rows (report.ts:72, :112, :141), so the evidence is in run detail. Only the PR comment is missing.
  - `deliveryComplete` stays unset, so an explicit resume re-enters `deliver()` → deliveredSha path (:2000) → posts the comment without pushing again.
  - The pattern matches the existing first-delivery draft path, which also logs a draft failure and keeps the original reason (:340–349).
- Diagnostics/evidence-only cost on a run that is needs_human anyway.

**Claim E: delivery errors are hidden behind the environment-blocked reason (engine.ts:348; 2 duplicates). Verdict: REAL-MINOR.**
- True: :348–349 only adopts `NeedsHumanError` messages and logs other errors as a warn event, and :352–363 keep `ENVIRONMENT_BLOCKED` as the run error.
- This is the pre-existing handling for every draft-delivery failure. The warning is in the run's event log and the run is needs_human (a human looks) either way.
- `headSha` is recorded at :2244 before the push. A failed push can therefore leave run detail naming an unpushed head, but approve and land re-check the real PR head, so nothing lands wrongly.

**Claim F: an environment-blocked conflict round can't update a draft PR (engine.ts:2004; 5 duplicates, one rated minor). Verdict: REAL-MINOR.**
- The guard `if (review.kind === "conflict" && pr.isDraft) throw` predates this change and also refuses successful conflict rounds.
- Conflict rounds are never created for a draft PR: store.ts `pendingRoundTriggers` skips with "PR is draft", and also skips owners in `needs_human`. So the trial-1 "PR is already draft" scenario can't occur.
- What remains is the owner converting the PR to draft during the round's minutes. That is contrived operator timing, and refusing to push to a PR the owner just drafted is arguably intended.

**Claim G: auto-merge isn't disabled before a blocked review round pushes (engine.ts:2005). Verdict: REAL-MINOR.**
- True that :2005–2006 disables auto-merge only for conflict/ci rounds.
- But review-round creation disables it when changes are requested (review-round.ts:198), and the land queue never arms it (queue.ts merge comment).
- The trigger needs a human to re-enable auto-merge on the PR during the round. That is an operator choice the request doesn't ask to handle. The same gap exists for successful review rounds.

**Claim H: an arbitrary PR comment containing the marker suppresses the evidence comment (security-flagged, engine.ts:2037). Verdict: REAL-MINOR.**
- True that the check is an unauthenticated substring match.
- The same unauthenticated marker check already existed for conflict/ci rounds before this change.
- The attacker needs the round run id, which first becomes public in the pushed commit message (`Run: <id>`, :2241), so the window is roughly the push-to-lookup gap (:2019–2035).
- The harm is only a missing comment: no merge, approval or gate is affected, and the evidence remains in the run report. Still present unchanged on origin/main (`deliveryMarker` + `hasMarker`).

**Label: CLEAN holds** (no REAL-MAJOR). I also checked requirement 2: the head's tests assert the feed item and run detail carry the pushed `headSha` (review-rounds.test.ts).

## review-133 (sandbox #14: textkit `dedupe`), head 4e4676e

**Claim I: newline-terminated input gains an extra blank output line (all 4 findings, text.ts:97 + cli.ts:89). Verdict: REAL-MINOR (borderline NOT-REAL).**
- The bytes are right: `dedupe("a\nb\na\n")` returns `"a\nb\n"` and `console.log` appends `\n`.
- But it is deliberate, documented and consistent with the repo:
  1. The head's own test pins `["a\nb\n\n", "a\nb\n"]` (test/text.test.ts), and the README says "an empty line is retained once".
  2. Input is a CLI argument, not stdin, and every existing command (`uppercase`, `title`, `reverse`) passes a trailing newline through to `console.log` the same way. That is the "existing command conventions" the request said to follow. `textStats` uses the same split.
  3. Triggering it takes an explicit `$'…\n'` argument; `"$(cat f)"` strips trailing newlines.
- The request doesn't specify uniq-style terminator semantics. No later round changed this: the only other dedupe branch, conflict-round-1 a9d2dd2, uses the same split.

**Label: CLEAN holds.**

## Summary
| Case | REAL-MAJOR | REAL-MINOR | NOT-REAL | CLEAN holds? |
|---|---|---|---|---|
| 124 | 0 | B (retarget), C (merged legacy entry) | A (claim recheck) | yes |
| 130 | 0 | D, E, F, G, H | 0 | yes |
| 133 | 0 | I (trailing newline) | 0 | yes |

All three blocks are false blocks under the rubric. The verifier tends to rate pre-existing patterns or operator-timing triggers as high: 124-A, 130-E/F/H were pre-existing, and 124-B, 130-F/G need an operator action mid-flight.
