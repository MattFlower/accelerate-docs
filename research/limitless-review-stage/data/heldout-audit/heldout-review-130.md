# review-130 (held-out, labelled CLEAN)

```json
{
 "id": "review-130",
 "repo": "MattFlower/limitless",
 "base": "af76c2be1c63479c33d43ebb9beb184c7651a71e",
 "head": "40056f0df80b7ef6812fcdf4b96c9ce31a576d88",
 "source": "pr #490 fresh clean set 2026-10-16 @ 40056f0",
 "prompt": "## What's wrong\nWhen the verifier can only report environment blocks (`verification blocked by the environment`), the run ends `needs_human`. The two delivery paths handle that differently:\n- **A first delivery** pushes and opens a **draft** PR with the 🚧 evidence. The guide's advice (\"verify those criteria yourself and mark the PR ready\", GUIDE §8) depends on that push.\n- **A review, conflict or CI-fix round** returns `PR update needs human review; no push` (`src/pipeline/engine.ts`, `deliverReviewRound` is skipped when `!success`). The round's commit stays in the factory's repository cache. The PR still shows the previous head, and nothing the owner can open or land contains the fixes.\n\nSeen on 2026-10-10. Review round <run-id> on #483:\n- the gates passed and review approved;\n- verify met 11 of 15 criteria and blocked the other 4, because real-Seatbelt tests skip inside confined gates;\n- the round's commit was never pushed.\n\nThe orchestrator had to fetch it from the cache by SHA to review it. The blocked criteria pass unconfined.\n\n## Change\n1. **A round that ends blocked only by its environment pushes its commit,** the same way a first delivery does, as long as gates, the audit and review would have let it deliver.\n   - It updates the PR branch with an explicit pinned refspec.\n   - It posts the round comment with the 🚧 evidence, and marks the PR as a draft or leaves it unchanged; whichever the first-delivery path does, match it.\n   - It doesn't mark the round approved.\n   - The run still ends `needs_human`, with the same reason.\n2. **Feed and run detail** name the pushed head, so `limitless review <run> --approve --sha <head>` and `limitless land <pr> --sha <head>` work on it without a cache lookup.\n3. **Every other `!success` outcome stays as it is,** with no push: a real verify failure, an audit or gate block, or exhausted rounds.\n\n## Tests (fake `gh`, no network)\n- A review round whose verify returns only `blocked` criteria pushes its head to the PR branch, posts the evidence and ends `needs_human`.\n- A review round whose verify has an `unmet` criterion doesn't push.\n- Restarting after the push doesn't push again (an existing durable checkpoint, or a new one).\n- A conflict round and a CI-fix round behave like a review round.\n\n## Budget\nAbout 60 changed source lines plus tests.\n\n## Out of scope\nMaking Seatbelt tests runnable inside confined gates, and changing the verifier's gate-substitution rule."
}
```

# Blocking findings (verifier high/critical or security), both trials

## trial 0: A comment failure leaves a pushed head without its evidence
```json
{
 "severity": "major",
 "security": false,
 "file": "src/pipeline/engine.ts",
 "line": 2065,
 "title": "A comment failure leaves a pushed head without its evidence",
 "detail": "The push and delivered-SHA checkpoint occur before the evidence comment. If the comment lookup or posting fails with an ordinary error, the outer handler logs it and terminates the run as needs_human with the original environment-blocked reason. It does not retry delivery or expose the publication failure in the run error, so the PR can contain the new head without the required evidence.",
 "suggestion": "Persist an incomplete delivery state and make comment publication recoverable, or surface its failure as the terminal reason so it can be acted on.",
 "failure_scenario": "The branch push succeeds, then GitHub returns an error for the PR comments lookup or comment creation. The run finishes needs_human, and the PR has the new commit but no blocked-criteria comment.",
 "category": "reliability",
 "confidence": 0.98,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "src/pipeline/engine.ts:2029–2035 records `markRoundDelivered(ctx.run.id, head)` and saves `\"round-delivered\"` before fetching comments. Line 2065 then awaits `gh([\"pr\", \"comment\", prUrl, \"--body-file\", \"-\"], ...)`. Lines 348–349 catch delivery errors, update the message only for `NeedsHumanError`, and otherwise log a warning; lines 362–364 finalize the run.",
  "trigger": "The push succeeds, but the comments lookup or creation fails after applicable retries. Delivery stops and the run ends needs_human with the new PR head missing its required blocked-criteria evidence.",
  "severity": "high",
  "category": "reliability"
 },
 "agreement": 1,
 "duplicates": []
}
```

## trial 0: An environment-blocked conflict round cannot update a draft PR
```json
{
 "severity": "major",
 "security": false,
 "file": "src/pipeline/engine.ts",
 "line": 330,
 "title": "An environment-blocked conflict round cannot update a draft PR",
 "detail": "The new conflict-round delivery path reaches deliverReviewRound, but its existing draft guard rejects conflict deliveries before the push. A PR can become draft while the round is running, and the requested behavior permits leaving its draft state unchanged. In that case the checked resolution remains in the cache and no evidence is posted.",
 "suggestion": "Allow the environment-blocked conflict delivery to update an otherwise valid draft PR while preserving its draft state.",
 "failure_scenario": "A conflict round starts while its PR is ready; the owner converts it to draft before verification finishes; verification then reports only environment-blocked criteria. Delivery throws \"the PR is draft\" and does not push.",
 "category": "correctness",
 "confidence": 0.96,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "src/pipeline/engine.ts:2004: `if (review.kind === \"conflict\" && pr.isDraft) throw new Error(\"the PR is draft\");`. This precedes `pushExistingBranch(...)` at line 2019 and has no exception for `environmentBlockedRound(ctx)`.",
  "trigger": "An owner converts a ready PR to draft during a conflict round. Environment-only verification blocks then reach delivery, which rejects the draft PR and leaves the resolved commit unpushed.",
  "severity": "high",
  "category": "correctness"
 },
 "agreement": 1,
 "duplicates": []
}
```

## trial 0: Delivery errors are hidden behind the environment-blocked reason
```json
{
 "severity": "major",
 "security": false,
 "file": "src/pipeline/engine.ts",
 "line": 348,
 "title": "Delivery errors are hidden behind the environment-blocked reason",
 "detail": "The new blocked-round delivery runs inside a catch handler that preserves the original verification reason for ordinary errors. If the push or evidence comment fails, the run still ends needs_human with only the environment-blocked reason, even though the requested delivery was incomplete. A comment failure after the push also leaves the delivered checkpoint recorded without a subsequent retry.",
 "suggestion": "Persist and surface the delivery failure, and leave incomplete publication resumable until the evidence comment is posted.",
 "failure_scenario": "Verification is blocked only by the environment, but GitHub rejects the push or the comment request fails. The run reports only 'verification blocked by the environment'; in the comment failure case the PR head is updated without the required evidence comment.",
 "category": "reliability",
 "confidence": 0.99,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "src/pipeline/engine.ts:348–349: `if (err instanceof NeedsHumanError) message = err.message;` followed by `ctx.log(...)`. Lines 353–359 replace persisted reasons only when `!message.startsWith(ENVIRONMENT_BLOCKED)`. Line 363 stores `error: message.slice(0, 2000)`.",
  "trigger": "An environment-blocked round encounters an ordinary push or comment error after applicable retries. The error is logged, but the final run error and persisted reason retain only the environment block, concealing incomplete delivery; a failed comment leaves the pushed head without evidence.",
  "severity": "high",
  "category": "reliability"
 },
 "agreement": 1,
 "duplicates": []
}
```

## trial 0: Blocked conflict rounds cannot update a PR that becomes draft
```json
{
 "severity": "major",
 "security": false,
 "file": "src/pipeline/engine.ts",
 "line": 2004,
 "title": "Blocked conflict rounds cannot update a PR that becomes draft",
 "detail": "The existing conflict delivery guard rejects a draft PR, and the new environment-blocked path reaches that guard unchanged. The request permits leaving the PR's draft state unchanged, so a conflict round whose PR is made draft while the round runs cannot publish its checked head.",
 "suggestion": "Allow an environment-blocked conflict round to update the existing draft without changing its draft state, while retaining the other delivery checks.",
 "failure_scenario": "A conflict round starts on a ready PR, its owner marks the PR draft during the round, and verification ends with only environment blocks. Delivery throws 'the PR is draft' and the resolved commit remains unpushed.",
 "category": "correctness",
 "confidence": 0.96,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "src/pipeline/engine.ts:1998 reads the current PR with `readPrHead(...)`; line 2004 immediately rejects conflict delivery when `pr.isDraft`, before the push at line 2019. The guard applies equally to environment-blocked rounds.",
  "trigger": "The PR becomes draft while its conflict round is running. Although verification ends with environment blocks only, delivery refuses to push the resolved head.",
  "severity": "high",
  "category": "correctness"
 },
 "agreement": 1,
 "duplicates": []
}
```

## trial 0: A failed evidence comment leaves the pushed round permanently incomplete
```json
{
 "severity": "major",
 "security": false,
 "file": "src/pipeline/engine.ts",
 "line": 2066,
 "title": "A failed evidence comment leaves the pushed round permanently incomplete",
 "detail": "The branch is pushed and marked delivered before the evidence comment is posted. If the GitHub comment request fails with an ordinary error, the outer delivery handler logs it and finishes the run as needs_human with the original environment-blocked reason. No retry is scheduled, so the PR has the new head but lacks the required blocked-verification evidence.",
 "suggestion": "Keep the delivery resumable until the comment is confirmed, or surface the comment failure as the terminal reason and provide a durable retry path.",
 "failure_scenario": "The pinned branch push succeeds, then `gh pr comment` fails due to a transient GitHub error. The run ends needs_human and the PR never receives the 🚧 evidence.",
 "category": "reliability",
 "confidence": 0.98,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "src/pipeline/engine.ts:2065 awaits the evidence comment after recording delivery at lines 2029–2030. Lines 348–364 swallow ordinary delivery errors into a warning and finalize `needs_human`. The GitHub wrapper at lines 2088–2089 uses `withGitHubRetry(...)`, but no further recovery is scheduled by this catch.",
  "trigger": "The push succeeds and the comment request continues failing until the retry policy stops. The run becomes terminal needs_human without the evidence comment; automatic completion is not scheduled.",
  "severity": "high",
  "category": "reliability"
 },
 "agreement": 1,
 "duplicates": []
}
```

## trial 0: A conflict round refuses delivery if the PR becomes a draft
```json
{
 "severity": "minor",
 "security": false,
 "file": "src/pipeline/engine.ts",
 "line": 2004,
 "title": "A conflict round refuses delivery if the PR becomes a draft",
 "detail": "The request says that a conflict round should behave like a review round and that delivery should mark the PR as a draft or leave it unchanged. This existing conflict-only guard also applies to the new environment-blocked delivery path, so it refuses to push when the PR is already a draft. Review rounds can publish in that state.",
 "suggestion": "Allow the environment-blocked conflict delivery to proceed when the PR is a draft, while preserving any draft restriction needed for other conflict deliveries.",
 "failure_scenario": "An environment-blocked conflict round reaches delivery after the owner has converted the PR to a draft. The guard throws before the pinned push, leaving the checked commit in the cache and the PR at its previous head.",
 "category": "correctness",
 "confidence": 0.94,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "src/pipeline/engine.ts:2306-2308 allows environment-blocked rounds through: `if (!success && !blocked) return ...;` then `if (review) await deliverReviewRound(...)`. Inside that function, src/pipeline/engine.ts:2004 unconditionally rejects draft conflict PRs: `if (review.kind === \"conflict\" && pr.isDraft) throw new Error(\"the PR is draft\");`, before the pinned push at line 2019.",
  "trigger": "The owner converts an active conflict round's PR to draft before delivery. Even with passing gates, audit and review and only environment-blocked verification, delivery throws before pushing; the PR retains its previous head and the checked fixes remain in the cache.",
  "severity": "high",
  "category": "correctness"
 },
 "agreement": 1,
 "duplicates": []
}
```

## trial 1: Allow blocked conflict rounds to update an existing draft PR
```json
{
 "severity": "major",
 "security": false,
 "file": "src/pipeline/engine.ts",
 "line": 2004,
 "title": "Allow blocked conflict rounds to update an existing draft PR",
 "detail": "The existing draft guard rejects every conflict round before the new blocked delivery can push. The requested behavior allows the PR's draft state to remain unchanged and requires conflict rounds to behave like review rounds, including when the PR is already draft.",
 "suggestion": "Permit an environment-blocked conflict round to push to an existing draft PR while leaving its draft state unchanged.",
 "failure_scenario": "A conflict-resolution round has passing gates, audit and review and only environment-blocked verification, but its PR is already draft; delivery throws before pushing and the fixes remain in the cache.",
 "category": "correctness",
 "confidence": 0.99,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "src/pipeline/engine.ts:2004: \"if (review.kind === \\\"conflict\\\" && pr.isDraft) throw new Error(\\\"the PR is draft\\\");\" precedes the push at :2019. This guard has no exception for environment-blocked rounds.",
  "trigger": "A conflict round starts on a ready PR, which becomes draft before delivery. Despite passing delivery checks and only environment-blocked verification, delivery throws and leaves the fixes unpushed.",
  "severity": "high",
  "category": "correctness"
 },
 "agreement": 1,
 "duplicates": []
}
```

## trial 1: Preserve a resumable delivery when posting blocked evidence fails
```json
{
 "severity": "major",
 "security": false,
 "file": "src/pipeline/engine.ts",
 "line": 2035,
 "title": "Preserve a resumable delivery when posting blocked evidence fails",
 "detail": "The push and delivered checkpoint happen before the comment lookup and post. If either GitHub call fails, the outer error handler logs the delivery failure and finishes the run as needs_human; it does not resume the incomplete comment step. The PR then contains the new head without the required blocked-verification evidence.",
 "suggestion": "Keep the delivery resumable until the evidence comment is confirmed, and surface a comment failure instead of treating the original environment block as fully delivered.",
 "failure_scenario": "The pinned push succeeds, then `gh pr view --json comments` or `gh pr comment` fails transiently; the run terminates needs_human and no evidence comment is posted.",
 "category": "reliability",
 "confidence": 0.98,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "src/pipeline/engine.ts:2029-2035 records \"ctx.store.markRoundDelivered(ctx.run.id, head)\" and \"await ctx.save(\\\"round-delivered\\\")\" before fetching comments; :2065 posts the comment. Errors reach :348-349, which only replace the message for NeedsHumanError and otherwise log a warning; :362-364 persist a terminal status and return.",
  "trigger": "After a successful push, a comment lookup or posting failure exhausts retries. The round terminates needs_human without its evidence comment or automatic continuation. The push checkpoint prevents duplicate pushes on a separately initiated resume, but does not schedule that resume.",
  "severity": "high",
  "category": "reliability"
 },
 "agreement": 1,
 "duplicates": []
}
```

## trial 1: Delivery errors are hidden behind the environment-blocked reason
```json
{
 "severity": "major",
 "security": false,
 "file": "src/pipeline/engine.ts",
 "line": 348,
 "title": "Delivery errors are hidden behind the environment-blocked reason",
 "detail": "A normal error from the newly added push or comment path is only logged. The run then finishes with the original verification-blocked reason, even if the branch was never pushed or the evidence comment was never posted. If the push succeeded before the comment failed, the terminal run also leaves the PR head updated without the requested evidence.",
 "suggestion": "Persist and surface delivery failures distinctly, and retain a resumable path for completing the comment after a successful push.",
 "failure_scenario": "The push succeeds but `gh pr comment` fails after its retry budget is exhausted. The run ends `needs_human` reporting only the environment block, with no evidence comment and no automatic continuation.",
 "category": "reliability",
 "confidence": 0.99,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "src/pipeline/engine.ts:348-349: \"if (err instanceof NeedsHumanError) message = err.message;\" and \"ctx.log(`Could not open draft PR: ${(err as Error).message}`, \\\"warn\\\");\". At :363 the final run error is \"error: message.slice(0, 2000)\".",
  "trigger": "The pinned push succeeds, then posting the evidence comment fails after retries with an ordinary command error. The final run error retains only the environment-blocked reason, concealing the incomplete delivery from that status.",
  "severity": "high",
  "category": "correctness"
 },
 "agreement": 1,
 "duplicates": []
}
```

## trial 1: A blocked conflict round cannot update a draft PR
```json
{
 "severity": "major",
 "security": false,
 "file": "src/pipeline/engine.ts",
 "line": 2004,
 "title": "A blocked conflict round cannot update a draft PR",
 "detail": "The newly enabled blocked conflict delivery enters the existing draft-PR rejection. This prevents publication even though the request permits leaving the PR's draft state unchanged and requires conflict rounds to behave like review rounds. The rejection is also swallowed by the surrounding draft-delivery catch.",
 "suggestion": "Allow an environment-blocked conflict round to deliver to an otherwise eligible draft PR while preserving its draft state.",
 "failure_scenario": "A PR becomes draft while its conflict-resolution round is running, and verification reports only environment blocks. Delivery throws `the PR is draft`, so the checked commit remains in the cache.",
 "category": "correctness",
 "confidence": 0.98,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "src/pipeline/engine.ts:1998 reads the current PR; :2004 immediately rejects \"review.kind === \\\"conflict\\\" && pr.isDraft\" with \"the PR is draft\", before \"await pushExistingBranch(...)\" at :2019.",
  "trigger": "The PR becomes draft while an otherwise deliverable conflict round runs. Environment-blocked verification enters delivery, but the draft guard prevents publishing the checked commit.",
  "severity": "high",
  "category": "correctness"
 },
 "agreement": 1,
 "duplicates": []
}
```

## trial 1: Disable auto-merge before publishing a blocked review round
```json
{
 "severity": "major",
 "security": false,
 "file": "src/pipeline/engine.ts",
 "line": 2005,
 "title": "Disable auto-merge before publishing a blocked review round",
 "detail": "Auto-merge is disabled at delivery for conflict and CI rounds, but not for review rounds. Although review-round creation disables it, it can be enabled again while the round is running. Pushing an environment-blocked head can then allow GitHub to merge it once its checks pass, before a human verifies the blocked criteria.",
 "suggestion": "Disable auto-merge for an environment-blocked review round before pushing, and cover auto-merge being re-enabled during the round.",
 "failure_scenario": "A review round starts with auto-merge disabled; a user enables it while verification is running; verification reports only blocked criteria and the new head is pushed to a ready PR whose required checks subsequently pass.",
 "category": "concurrency",
 "confidence": 0.96,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "src/pipeline/engine.ts:2005-2006 disables auto-merge only for other round kinds: `if ((review.kind === \"conflict\" || review.kind === \"ci\") && pr.autoMerge) await gh([\"pr\", \"merge\", prUrl, \"--disable-auto\"], ctx.signal);`. A review round proceeds to `await pushExistingBranch(...)` at :2019. src/pipeline/review-round.ts:198 disables auto-merge when changes are initially requested, but provides no protection against enabling it later.",
  "trigger": "A user enables auto-merge during an environment-blocked review round. Delivery pushes the blocked head without disabling auto-merge or converting the ready PR to draft; passing required checks can then merge work still awaiting human verification.",
  "severity": "high",
  "category": "concurrency"
 },
 "agreement": 1,
 "duplicates": []
}
```

## trial 1: Do not trust arbitrary PR comments as proof that evidence was posted
```json
{
 "severity": "major",
 "security": true,
 "file": "src/pipeline/engine.ts",
 "line": 2037,
 "title": "Do not trust arbitrary PR comments as proof that evidence was posted",
 "detail": "The new blocked-review comment is skipped if any PR comment contains the predictable round marker. PR comments are untrusted, so a commenter can insert that marker without the blocked evidence and suppress the factory's own comment. The head is already pushed and recorded as delivered at this point.",
 "suggestion": "Authenticate the marker against a factory-authored comment or use a durable publication record that cannot be supplied by an arbitrary commenter.",
 "failure_scenario": "A commenter posts a comment containing the review round's marker before delivery checks comments; the blocked head is pushed, but the required 🚧 evidence is never posted.",
 "category": "security",
 "confidence": 0.94,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "src/pipeline/engine.ts:2034-2037 constructs `<!-- limitless-${review.kind}-round:${ctx.run.id} -->`, reads comments as `{ body?: string }[]`, and gates posting solely on `!comments?.some((comment) => comment.body?.includes(marker))`. The blocked evidence is constructed at :2047-2062 and posted at :2065 only inside that condition.",
  "trigger": "Any commenter includes the round's marker in a comment before delivery reads comments. Delivery treats it as an existing evidence comment, skips posting the required 🚧 evidence, and records delivery complete.",
  "severity": "medium",
  "category": "correctness"
 },
 "agreement": 1,
 "duplicates": []
}
```
